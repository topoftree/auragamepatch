# Patch workflow validation

On 2026-10-23, the repository added the `aura-game-patch-release` skill and declarative release tool. The seven existing packages, catalog.json/catalog.sig, and SHA256SUMS stayed byte for byte. The new v2 catalog verified with the existing Ed25519 public key, and the game category index matched the signed catalog.

`python3 -m unittest discover -s tools/tests -v` passed seven tests covering reproducible packaging, retention of older versions, rejection of same-version replacement, signature and package tampering, paths and links, missing App integration evidence, the wrong key, and rejection of experimental categories. The tests used temporary keys and small fixtures. No demonstration packages were published.

`python3 tools/patch_release.py check` verified the v1 and v2 signatures, all catalog packages, checksums for retained source and upstream archives, and the category index. At the time, the App and patch repositories shared identical copies of the skill.

The companion App passed 80 host checks for automatic matching, baseline verification, manual priority, patch installation and recovery, the official SMAPI archive, import and download navigation, and bilingual resources. There were no failures or skips. Debug Lint reported zero errors and 80 warnings. Detailed results are in the App repository. This change did not produce a new APK. The protocol requires a later App build with versionCode 123 or higher, and the seven existing packages remained manual. Phone network behavior, gameplay results, and performance were not tested further.

Validated local App source commit: `29c60740de8ad08077bb464cc7b636e9e133b969`. This identifies the tested source. Public release of the App commit or an APK is a separate step.

Releases use normal fast-forward pushes. Files are read back at the exact remote commit and verified. To repeat the readback, run:

```bash
python3 tools/patch_release.py readback --commit FULL_RELEASE_COMMIT_SHA
```
