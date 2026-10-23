#!/usr/bin/env python3
"""Add, verify and publish immutable Aura patches. No downloaded scripts are executed."""
import argparse
import base64
import hashlib
import io
import json
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_KEY = "MCowBQYDK2VwAyEAMCq0X0JPLYvjhCXFQFrMuzUAMVqLFswBZmWTofWPjCM="
CATEGORIES = {"compatibility", "fix", "widescreen", "mod", "tool"}
SLUG = re.compile(r"[a-z0-9-]{1,80}\Z")
VERSION = re.compile(r"[a-zA-Z0-9.-]{1,50}\Z")
SHA = re.compile(r"[0-9a-f]{64}\Z")
MAX_PACKAGE = 64 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def path_ok(name):
    require(isinstance(name, str) and 0 < len(name) <= 2048, "Invalid path")
    parts = name.split("/")
    reserved = {"CON", "PRN", "AUX", "NUL"} | {f"{p}{n}" for p in ("COM", "LPT") for n in range(1, 10)}
    require(len(parts) <= 25 and all(p and p.strip() and p not in (".", "..") and
        not p.endswith((".", " ")) and not p.lower().startswith((".aura-", ".winlator-")) and
        p.split(".")[0].upper() not in reserved and not any(ord(c) < 32 or c in '\\:*?"<>|' for c in p)
        for p in parts), "Unsafe relative path: " + name)


def contained(root, name):
    path_ok(name)
    file = root / name
    require(file.resolve().is_relative_to(root.resolve()), "Path escapes repository")
    require(not any(p.is_symlink() for p in [file, *file.parents] if p.is_relative_to(root)), "Symlink input")
    return file


def stamp(value):
    require(set(value) == {"bytes", "sha256"}, "Invalid baseline fields")
    require(type(value["bytes"]) is int and 0 <= value["bytes"] <= 512 * 1024 * 1024 and
            isinstance(value["sha256"], str) and SHA.fullmatch(value["sha256"]), "Invalid baseline")


def validate_entry(entry, classified=True):
    allowed = {"id", "version", "title", "description", "executables", "path", "bytes", "sha256", "kind", "policy",
               "game", "category", "autoInstall", "minAppVersionCode"}
    require(set(entry) <= allowed, "Unknown entry fields; update the app protocol first")
    require(type(entry.get("minAppVersionCode", 1)) is int and 0 < entry.get("minAppVersionCode", 1) <= 2147483647, "Invalid minimum App version")
    require(SLUG.fullmatch(entry["id"]) and VERSION.fullmatch(entry["version"]), "Invalid ID/version")
    require(0 < len(entry["title"]) <= 160 and len(entry["description"]) <= 6000, "Invalid text size")
    exes = entry["executables"]
    require(0 < len(exes) <= 16 and all(re.fullmatch(r"[a-zA-Z0-9 _.'-]{1,100}\.exe", x, re.I) for x in exes), "Invalid executable")
    require(entry["path"] == f'packages/{entry["id"]}/{entry["version"]}.zip', "Invalid package path")
    require(type(entry["bytes"]) is int and 0 < entry["bytes"] <= MAX_PACKAGE and SHA.fullmatch(entry["sha256"]), "Invalid package size/hash")
    kind, policy = entry["kind"], entry.get("policy", "")
    require(kind in {"profile", "binary", "files", "tool"}, "Unsupported kind")
    policies = {"bf3-single-player": ("profile", "bf3.exe"), "mgs-startup": ("profile", "mgsgroundzeroes.exe"),
                "winmm-native": ("files", "mgsgroundzeroes.exe"), "crysis2-dx9": ("profile", "crysis2.exe")}
    if policy:
        require(policy in policies and policies[policy][0] == kind and
                all(x.lower() == policies[policy][1] for x in exes), "Unsupported app launch policy")
    else:
        require(kind != "profile", "A profile requires an app-supported policy")
    if policy == "crysis2-dx9":
        require(entry["id"] == "crysis2-dx9" and entry.get("minAppVersionCode", 1) >= 123,
                "Crysis 2 DX9 requires its fixed identity and App code 123 or later")
    if classified:
        require(SLUG.fullmatch(entry["game"]) and entry["category"] in CATEGORIES, "Missing game/category")
    auto = entry.get("autoInstall")
    if auto is not None:
        require(set(auto) <= {"minAppVersionCode", "executable", "targets"}, "Unknown automatic fields")
        require(type(auto["minAppVersionCode"]) is int and
                max(123, entry.get("minAppVersionCode", 1)) <= auto["minAppVersionCode"] <= 2147483647 and entry["category"] in {"compatibility", "fix"} and
                kind != "tool" and policy not in {"bf3-single-player", "smapi", "winmm-native", "crysis2-dx9"} and
                entry["id"] != "stardew-fps-experimental", "This patch must remain manual")
        stamp(auto["executable"])
        require(auto["executable"]["bytes"] > 0, "Empty executable baseline")
        targets = auto.get("targets", [])
        require(len(targets) <= 255 and len({x["path"].lower() for x in targets}) == len(targets), "Duplicate automatic targets")
        require(bool(targets) == (kind == "files"), "Automatic file baseline must cover every target")
        for target in targets:
            require(set(target) <= {"path", "before"}, "Unknown target fields")
            path_ok(target["path"])
            if target.get("before") is not None:
                stamp(target["before"])


def validate_package(entry, data):
    require(len(data) == entry["bytes"] and digest(data) == entry["sha256"], "Package hash/size mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        require(0 < len(infos) <= 256 and sum(x.file_size for x in infos) <= 256 * 1024 * 1024, "Archive too large")
        names = [x.filename for x in infos]
        require(len({x.lower() for x in names}) == len(names), "Duplicate ZIP paths")
        for info in infos:
            path_ok(info.filename)
            require(not info.is_dir() and (info.external_attr >> 16) & 0o170000 != 0o120000, "Link/directory in archive")
        require(archive.getinfo("manifest.json").file_size <= 1024 * 1024, "Manifest too large")
        manifest = json.loads(archive.read("manifest.json"))
        require(set(manifest) <= {"schema", "id", "version", "kind", "policy", "files", "binary"}, "Unknown manifest fields")
        require(manifest["schema"] == 1 and all(manifest.get(k, "") == entry.get(k, "") for k in ("id", "version", "kind", "policy")), "Manifest mismatch")
        files = manifest.get("files", [])
        require(set(names) == {"manifest.json"} | {x["source"] for x in files}, "Undeclared ZIP contents")
        require(len({x["target"].lower() for x in files}) == len(files), "Duplicate target")
        for item in files:
            require(set(item) == {"source", "target", "sha256"}, "Unknown file fields")
            path_ok(item["target"])
            require(item["source"].startswith("files/") and digest(archive.read(item["source"])) == item["sha256"], "File checksum mismatch")
        kind = manifest["kind"]
        binary = manifest.get("binary")
        if kind == "binary":
            require(not files and binary is not None and set(binary) == {"bytes", "before", "after", "edits"}, "Invalid binary recipe")
            require(0 < binary["bytes"] <= 512 * 1024 * 1024 and SHA.fullmatch(binary["before"]) and SHA.fullmatch(binary["after"]), "Invalid executable identity")
            require(0 < len(binary["edits"]) <= 256, "Invalid edit count")
            end = 0
            for edit in sorted(binary["edits"], key=lambda x: x["offset"]):
                require(set(edit) == {"offset", "before", "after"}, "Unknown edit fields")
                for side in ("before", "after"):
                    require(re.fullmatch(r"[0-9a-f]{2,2048}", edit[side]) and len(edit[side]) % 2 == 0, "Invalid patch bytes")
                require(len(edit["before"]) == len(edit["after"]) and end <= edit["offset"] <= binary["bytes"] - len(edit["before"]) // 2, "Overlapping/outside edits")
                end = edit["offset"] + len(edit["before"]) // 2
            if entry.get("autoInstall"):
                require(entry["autoInstall"]["executable"] == {"bytes": binary["bytes"], "sha256": binary["before"]}, "Auto/binary baseline differs")
        elif kind == "profile":
            require(not files and binary is None, "Profile must not contain files")
        else:
            require(files and binary is None, "File/tool package is empty")
        if entry.get("autoInstall") and kind == "files":
            require({x["target"].lower() for x in files} == {x["path"].lower() for x in entry["autoInstall"]["targets"]}, "Missing automatic target baseline")


def verify_signature(root, stem):
    key = root / "catalog-public-key.pem"
    public = subprocess.check_output(["openssl", "pkey", "-pubin", "-in", str(key), "-outform", "DER"])
    require(base64.b64encode(public).decode() == PUBLIC_KEY, "Unapproved catalogue key rotation")
    with tempfile.TemporaryDirectory() as temporary:
        signature = Path(temporary) / "sig"
        signature.write_bytes(base64.b64decode((root / (stem + ".sig")).read_text().strip(), validate=True))
        subprocess.run(["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", str(key), "-rawin", "-in",
                        str(root / (stem + ".json")), "-sigfile", str(signature)], check=True, stdout=subprocess.DEVNULL)


def check(root):
    catalogs = []
    for stem in ("catalog", "catalog-v2"):
        if not (root / (stem + ".json")).exists():
            require(stem != "catalog", "Missing legacy catalogue")
            continue
        verify_signature(root, stem)
        catalog = json.loads((root / (stem + ".json")).read_bytes())
        require(catalog["schema"] == (1 if stem == "catalog" else 2), "Unexpected schema")
        entries = catalog["patches"]
        require(len(entries) <= 500 and len({x["id"] for x in entries}) == len(entries), "Duplicate patch IDs")
        for entry in entries:
            validate_entry(entry, classified=stem != "catalog")
            validate_package(entry, contained(root, entry["path"]).read_bytes())
        catalogs.append(catalog)
    # Verify all archived versions and corresponding-source archives, not just current entries.
    recorded = set()
    for line in (root / "SHA256SUMS").read_text().splitlines():
        sha, name = line.split("  ", 1)
        require(name not in recorded, "Duplicate checksum path")
        recorded.add(name)
        require(SHA.fullmatch(sha) and digest(contained(root, name).read_bytes()) == sha, "SHA256SUMS mismatch: " + name)
    all_files = {p.relative_to(root).as_posix() for folder in ("packages", "sources", "upstream")
                 for p in (root / folder).rglob("*") if p.is_file()}
    require(recorded == all_files, "Checksum list must cover every retained package/source/upstream file")
    if catalogs[-1]["schema"] == 2:
        expected = {}
        for entry in catalogs[-1]["patches"]:
            expected.setdefault(entry["game"], {}).setdefault(entry["category"], []).append(entry["id"])
        require(json.loads((root / "games/index.json").read_bytes()) == expected, "Game classification index is stale")
    return catalogs[-1]


def write_catalog(root, entries, key):
    require(not key.resolve().is_relative_to(root.resolve()), "Keep the private signing key outside the public repo")
    public = subprocess.check_output(["openssl", "pkey", "-in", str(key), "-pubout", "-outform", "DER"])
    require(base64.b64encode(public).decode() == PUBLIC_KEY, "Wrong signing key; do not rotate automatically")
    data = encoded({"schema": 2, "patches": entries})
    with tempfile.TemporaryDirectory() as temporary:
        source, signature = Path(temporary) / "catalog", Path(temporary) / "signature"
        source.write_bytes(data)
        subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", str(key), "-rawin", "-in", str(source), "-out", str(signature)], check=True)
        (root / "catalog-v2.json").write_bytes(data)
        (root / "catalog-v2.sig").write_bytes(base64.b64encode(signature.read_bytes()) + b"\n")
    write_index(root, entries)
    sums = []
    for folder in ("packages", "upstream", "sources"):
        for file in sorted((root / folder).rglob("*")):
            if file.is_file():
                require(not file.is_symlink(), "Symlink in release")
                sums.append(digest(file.read_bytes()) + "  " + file.relative_to(root).as_posix())
    (root / "SHA256SUMS").write_text("\n".join(sums) + ("\n" if sums else ""))


def write_index(root, entries):
    games = {}
    for entry in entries:
        games.setdefault(entry["game"], {}).setdefault(entry["category"], []).append(entry["id"])
    folder = root / "games"
    folder.mkdir(exist_ok=True)
    (folder / "index.json").write_bytes(encoded(games))
    rows = ["# 游戏补丁分类", "", "自动安装只适用于签名目录中明确声明 autoInstall 且符合原文件基线的新修复。", "",
            "| 游戏 | 分类 | 补丁 | 安装策略 |", "| --- | --- | --- | --- |"]
    for p in sorted(entries, key=lambda p: (p["game"], p["category"], p["id"])):
        rows.append(f'| {p["game"]} | {p["category"]} | [{p["id"]} {p["version"]}](../{p["path"]}) | '
                    + (f'精确版本自动安装；App code ≥ {p["autoInstall"]["minAppVersionCode"]}' if p.get("autoInstall") else "用户手动选择") + " |")
    (folder / "README.md").write_text("\n".join(rows) + "\n")


def add(root, recipe_path, key):
    catalog = check(root)
    require(catalog["schema"] == 2, "Initialize the classified v2 catalogue first")
    recipe = json.loads(recipe_path.read_bytes())
    require(set(recipe) <= {"schema", "entry", "files", "binary", "provenance"} and recipe["schema"] == 1, "Invalid recipe")
    entry = dict(recipe["entry"])
    require(not {"bytes", "sha256", "path"} & entry.keys(), "Generated fields must not be supplied")
    expected = f'recipes/{entry["game"]}/{entry["category"]}/{entry["id"]}/{entry["version"]}/recipe.json'
    require(recipe_path.resolve() == contained(root, expected).resolve(), "Recipe is not in its game/category/version folder")
    provenance = recipe["provenance"]
    require(provenance.get("upstream", "").startswith("https://"), "Record source provenance")
    for field in ("license", "validation"):
        require(contained(root, provenance[field]).is_file(), "Missing provenance file: " + field)
    if entry.get("autoInstall"):
        evidence = json.loads(contained(root, provenance["validation"]).read_bytes())
        for test in ("installRestoreTested", "versionMismatchTested", "activationTested"):
            require(evidence.get(test) is True, "Missing automatic integration evidence: " + test)
        require(re.fullmatch("[0-9a-f]{40}", evidence.get("appCommit", "")), "Pin tested app source commit")
    manifest = dict(schema=1, **{k: entry[k] for k in ("id", "version", "kind")}, policy=entry.get("policy", ""), files=[])
    payloads = {}
    require(len(recipe.get("files", [])) <= 255, "Too many input files")
    expanded = 0
    for item in recipe.get("files", []):
        require(set(item) == {"source", "target"}, "Invalid recipe file")
        path_ok(item["target"])
        source = contained(recipe_path.parent, item["source"])
        expanded += source.stat().st_size
        require(expanded <= 255 * 1024 * 1024, "Inputs too large")
        data = source.read_bytes()
        name = "files/" + item["target"]
        require(name not in payloads, "Duplicate target")
        payloads[name] = data
        manifest["files"].append(dict(source=name, target=item["target"], sha256=digest(data)))
    if "binary" in recipe:
        manifest["binary"] = recipe["binary"]
    payloads["manifest.json"] = encoded(manifest)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, 0o100644 << 16
            archive.writestr(info, data)
    data = buffer.getvalue()
    entry.update(path=f'packages/{entry["id"]}/{entry["version"]}.zip', bytes=len(data), sha256=digest(data))
    validate_entry(entry)
    validate_package(entry, data)
    destination = contained(root, entry["path"])
    require(not destination.exists() or destination.read_bytes() == data, "Published package version is immutable; increment version")
    entries = [x for x in catalog["patches"] if x["id"] != entry["id"]] + [entry]
    # Validate key before adding any package to the working tree.
    public = subprocess.check_output(["openssl", "pkey", "-in", str(key), "-pubout", "-outform", "DER"])
    require(base64.b64encode(public).decode() == PUBLIC_KEY and not key.resolve().is_relative_to(root.resolve()), "Wrong/private-in-repo signing key")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    write_catalog(root, entries, key)
    check(root)
    print("Prepared", entry["id"], entry["version"], entry["sha256"])


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()


def readback(root, commit, paths=None):
    require(re.fullmatch(r"[0-9a-f]{40}", commit), "Use the complete publication commit SHA")
    if paths is None:
        paths = git(root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit).splitlines()
    for name in sorted(paths):
        path_ok(name)
        # Compare against the committed blob, not a potentially changed working tree.
        expected = subprocess.check_output(["git", "-C", str(root), "show", f"{commit}:{name}"])
        url = "https://raw.githubusercontent.com/topoftree/auragamepatch/" + commit + "/" + urllib.parse.quote(name)
        with urllib.request.urlopen(url, timeout=60) as response:
            remote_bytes = response.read(len(expected) + 1)
        require(digest(remote_bytes) == digest(expected), "Remote readback mismatch: " + name)
    print("Read back", commit, len(paths), "files")


def publish(root, message):
    check(root)
    remote = git(root, "remote", "get-url", "origin")
    require(remote in {"https://github.com/topoftree/auragamepatch.git", "git@github.com:topoftree/auragamepatch.git"}, "Wrong publication repository")
    require(git(root, "branch", "--show-current") == "main", "Publish from reviewed main only")
    subprocess.run(["git", "-C", str(root), "fetch", "origin", "main"], check=True)
    base = git(root, "rev-parse", "origin/main")
    subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", base, "HEAD"], check=True)
    paths = set(git(root, "diff", "--name-only", base).splitlines()) | set(git(root, "ls-files", "--others", "--exclude-standard").splitlines())
    allowed = {"README.md", "AGENTS.md", "LICENSE", "CHANGELOG.md", ".gitignore", "catalog-v2.json", "catalog-v2.sig", "SHA256SUMS"}
    prefixes = ("packages/", "recipes/", "games/", "sources/", "upstream/", "licenses/", "docs/", "tools/", ".agents/skills/")
    require(paths, "No publication changes")
    require(not git(root, "diff", "--name-only", "--diff-filter=D", base), "Do not delete published files automatically")
    require(not git(root, "diff", "--name-only", "--diff-filter=MDR", base, "--", "packages/"), "Published package bytes are immutable")
    for name in paths:
        require(name in allowed or name.startswith(prefixes), "Unrelated publication path: " + name)
        require(not any(x in name.lower() for x in (".signing", "private", "mapping.txt", "debug.zip")) and
                Path(name).suffix.lower() not in {".pem", ".key", ".p12", ".pfx", ".apk", ".jks"}, "Private/unrelated artifact: " + name)
        contained(root, name)
    subprocess.run(["git", "-C", str(root), "add", "--", *sorted(paths)], check=True)
    if git(root, "diff", "--cached", "--name-only"):
        subprocess.run(["git", "-C", str(root), "commit", "-m", message], check=True)
    commit = git(root, "rev-parse", "HEAD")
    subprocess.run(["git", "-C", str(root), "push", "origin", "HEAD:refs/heads/main"], check=True)
    readback(root, commit, paths)
    require(git(root, "ls-remote", "origin", "refs/heads/main").split()[0] == commit, "Remote head changed; inspect publication")
    print("Published and read back", commit, len(paths), "files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    build = sub.add_parser("add")
    build.add_argument("--recipe", type=Path, required=True)
    build.add_argument("--key", type=Path, required=True)
    pub = sub.add_parser("publish")
    pub.add_argument("--message", required=True)
    verify_remote = sub.add_parser("readback")
    verify_remote.add_argument("--commit", required=True)
    args = parser.parse_args()
    if args.command == "check":
        result = check(args.repo)
        print("Verified catalogue schema", result["schema"], len(result["patches"]), "packages")
    elif args.command == "add":
        add(args.repo, args.recipe, args.key)
    elif args.command == "publish":
        publish(args.repo, args.message)
    else:
        readback(args.repo, args.commit)


if __name__ == "__main__":
    main()
