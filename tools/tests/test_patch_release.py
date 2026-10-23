import base64
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


if __name__ == "__main__":
    unittest.main()
