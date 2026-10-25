import base64
import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("patch_release", Path(__file__).parents[1] / "patch_release.py")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class PatchReleaseTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.key = Path(self.temp.name) / "test-private.pem"
        subprocess.run(["openssl", "genpkey", "-algorithm", "ED25519", "-out", str(self.key)], check=True, capture_output=True)
        public = subprocess.check_output(["openssl", "pkey", "-in", str(self.key), "-pubout", "-outform", "DER"])
        old_key = release.PUBLIC_KEY
        self.addCleanup(setattr, release, "PUBLIC_KEY", old_key)
        release.PUBLIC_KEY = base64.b64encode(public).decode()
        subprocess.run(["openssl", "pkey", "-in", str(self.key), "-pubout", "-out", str(self.root / "catalog-public-key.pem")], check=True, capture_output=True)
        (self.root / "catalog.json").write_bytes(release.encoded({"schema": 1, "patches": []}))
        sig = Path(self.temp.name) / "sig"
        subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", str(self.key), "-rawin", "-in", str(self.root / "catalog.json"), "-out", str(sig)], check=True)
        (self.root / "catalog.sig").write_bytes(base64.b64encode(sig.read_bytes()) + b"\n")
        release.write_catalog(self.root, [], self.key)
        (self.root / "LICENSE").write_text("Test fixture only\n")
        (self.root / "validation.json").write_text(json.dumps({"installRestoreTested": True, "versionMismatchTested": True,
            "activationTested": True, "appCommit": "0" * 40}))

    def recipe(self, version="1.0.0"):
        entry = {"id": "example-fix", "version": version, "title": "Fixture", "description": "Test only",
                 "executables": ["Game.exe"], "kind": "binary", "game": "example", "category": "fix", "policy": "",
                 "autoInstall": {"minAppVersionCode": 123, "executable": {"bytes": 8, "sha256": release.digest(b"ORIGINAL")}}}
        path = self.root / f"recipes/example/fix/example-fix/{version}/recipe.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        value = {"schema": 1, "entry": entry, "binary": {"bytes": 8, "before": release.digest(b"ORIGINAL"),
            "after": release.digest(b"ORXGINAL"), "edits": [{"offset": 2, "before": "49", "after": "58"}]},
            "provenance": {"upstream": "https://example.test/fixture", "license": "LICENSE", "validation": "validation.json"}}
        path.write_bytes(release.encoded(value))
        return path

    def test_reproducible_signed_add_and_retained_versions(self):
        recipe = self.recipe()
        release.add(self.root, recipe, self.key)
        original = (self.root / "packages/example-fix/1.0.0.zip").read_bytes()
        release.add(self.root, recipe, self.key)
        self.assertEqual(original, (self.root / "packages/example-fix/1.0.0.zip").read_bytes())
        release.add(self.root, self.recipe("1.0.1"), self.key)
        self.assertEqual(original, (self.root / "packages/example-fix/1.0.0.zip").read_bytes())
        self.assertEqual("1.0.1", release.check(self.root)["patches"][0]["version"])
        self.assertEqual(["example-fix"], json.loads((self.root / "games/index.json").read_bytes())["example"]["fix"])

    def test_same_version_cannot_replace_published_bytes(self):
        path = self.recipe()
        release.add(self.root, path, self.key)
        value = json.loads(path.read_bytes())
        value["binary"]["edits"][0]["after"] = "59"
        path.write_bytes(release.encoded(value))
        with self.assertRaisesRegex(ValueError, "immutable"):
            release.add(self.root, path, self.key)

    def test_tampered_signature_or_package_is_rejected(self):
        release.add(self.root, self.recipe(), self.key)
        (self.root / "packages/example-fix/1.0.0.zip").write_bytes(b"bad")
        with self.assertRaisesRegex(ValueError, "hash/size"):
            release.check(self.root)
        (self.root / "catalog-v2.json").write_bytes(b"{}")
        with self.assertRaises(subprocess.CalledProcessError):
            release.check(self.root)

    def test_missing_integration_evidence_refuses_automatic_publication(self):
        path = self.recipe()
        (self.root / "validation.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "integration evidence"):
            release.add(self.root, path, self.key)
        self.assertFalse((self.root / "packages/example-fix/1.0.0.zip").exists())

    def test_unsafe_paths_and_symlinks_are_rejected(self):
        for path in ("../x", "/x", "CON.txt", "a/./b", "a\\b", "a/", "a.", ".aura-secret/x"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.path_ok(path)
        (self.root / "link").symlink_to(self.key)
        with self.assertRaises(ValueError):
            release.contained(self.root, "link")

    def test_wrong_key_does_not_change_catalogue_or_create_package(self):
        path = self.recipe()
        original = (self.root / "catalog-v2.json").read_bytes()
        key = Path(self.temp.name) / "wrong.pem"
        subprocess.run(["openssl", "genpkey", "-algorithm", "ED25519", "-out", str(key)], check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "signing key"):
            release.add(self.root, path, key)
        self.assertEqual(original, (self.root / "catalog-v2.json").read_bytes())
        self.assertFalse((self.root / "packages/example-fix/1.0.0.zip").exists())

    def test_experimental_category_cannot_enable_automatic_installation(self):
        path = self.recipe()
        value = json.loads(path.read_bytes())
        entry = value["entry"]
        entry.update(path="packages/example-fix/1.0.0.zip", bytes=1, sha256="0" * 64, category="mod")
        with self.assertRaisesRegex(ValueError, "remain manual"):
            release.validate_entry(entry)

    def test_crysis2_renderer_profile_requires_supported_app_and_stays_manual(self):
        entry = {"id": "crysis2-dx9", "version": "1.0.0", "title": "Crysis 2 DX9", "description": "Optional",
                 "executables": ["Crysis2.exe"], "kind": "profile", "game": "crysis-2", "category": "compatibility",
                 "policy": "crysis2-dx9", "path": "packages/crysis2-dx9/1.0.0.zip", "bytes": 1,
                 "sha256": "0" * 64, "minAppVersionCode": 123}
        release.validate_entry(entry)
        for changes in ({"minAppVersionCode": 122}, {"executables": ["Crysis2Remastered.exe"]},
                        {"kind": "files"}, {"id": "other", "path": "packages/other/1.0.0.zip"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                release.validate_entry(entry | changes)
        with self.assertRaisesRegex(ValueError, "remain manual"):
            release.validate_entry(entry | {"autoInstall": {"minAppVersionCode": 123,
                "executable": {"bytes": 40670208, "sha256": "0" * 64}}})

    def resource_recipe(self):
        path = self.recipe()
        value = json.loads(path.read_bytes())
        value["schema"] = 2
        value.pop("binary")
        entry = value["entry"]
        entry.pop("autoInstall")
        entry.update(id="mirrors-edge-widescreen-195", policy="mirrors-edge-widescreen-195",
                     game="mirrors-edge", category="widescreen", executables=["MirrorsEdge.exe"], minAppVersionCode=137)
        value["resourceBinary"] = dict(path="TdGame/CookedPC/Engine.u", variants=[dict(
            bytes=4, before=release.digest(bytes.fromhex("f38ee33f")), after=release.digest(bytes.fromhex("abaa0a40")),
            edits=[dict(offset=0, before="f38ee33f", after="abaa0a40")])])
        target = self.root / "recipes/mirrors-edge/widescreen/mirrors-edge-widescreen-195/1.0.0/recipe.json"
        target.parent.mkdir(parents=True)
        target.write_bytes(release.encoded(value))
        return target, value

    def test_resource_schema_two_is_reproducible_and_keeps_v1_unchanged(self):
        path, _ = self.resource_recipe()
        old = (self.root / "catalog.json").read_bytes()
        old_signature = (self.root / "catalog.sig").read_bytes()
        release.add(self.root, path, self.key)
        first = (self.root / "packages/mirrors-edge-widescreen-195/1.0.0.zip").read_bytes()
        release.add(self.root, path, self.key)
        self.assertEqual(first, (self.root / "packages/mirrors-edge-widescreen-195/1.0.0.zip").read_bytes())
        self.assertEqual(old, (self.root / "catalog.json").read_bytes())
        self.assertEqual(old_signature, (self.root / "catalog.sig").read_bytes())
        self.assertEqual(137, release.check(self.root)["patches"][0]["minAppVersionCode"])

    def test_resource_recipe_rejects_wrong_scope_and_unsupported_versions(self):
        path, value = self.resource_recipe()
        invalid = []
        for change in ({"minAppVersionCode": 136}, {"category": "fix"}, {"executables": ["bf3.exe"]},
                       {"autoInstall": {"minAppVersionCode": 137, "executable": {"bytes": 4, "sha256": "0" * 64}}}):
            candidate = copy.deepcopy(value)
            candidate["entry"].update(change)
            # Preserve the intended recipe folder to test entry checks directly.
            entry = candidate["entry"] | dict(path="packages/mirrors-edge-widescreen-195/1.0.0.zip", bytes=1, sha256="0" * 64)
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_entry(entry)
        candidate = copy.deepcopy(value); candidate["schema"] = 1; invalid.append(candidate)
        candidate = copy.deepcopy(value); candidate["resourceBinary"]["path"] = "../Engine.u"; invalid.append(candidate)
        candidate = copy.deepcopy(value); candidate["resourceBinary"]["variants"] *= 2; invalid.append(candidate)
        candidate = copy.deepcopy(value); candidate["resourceBinary"]["variants"][0]["edits"][0]["after"] = "00000000"; invalid.append(candidate)
        for candidate in invalid:
            path.write_bytes(release.encoded(candidate))
            with self.assertRaises(ValueError):
                release.add(self.root, path, self.key)
        self.assertFalse((self.root / "packages/mirrors-edge-widescreen-195/1.0.0.zip").exists())


if __name__ == "__main__":
    unittest.main()
