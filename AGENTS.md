# Aura patch repository agreements

- `mirrors-edge-widescreen-195` uses schema 2 `resourceBinary`. It targets a fixed game and resource and makes a single 19.5:9 float edit. It requires App versionCode 137 or later, is selected manually, and does not contain the full resource. New formats must preserve compatibility with older manifests and catalogs. Record launch-time byte verification separately from visual verification on a phone.

- This repository is the user-authorized public `topoftree/auragamepatch`. It does not contain standalone Aura App source code or complete commercial game files.
- On 2026-10-23, the user gave ongoing authorization to package, categorize, verify, and upload new game-specific compatibility and bug fixes, and to complete the corresponding App download, installation, activation, and recovery integration. This authorization does not cover APKs or publishing to other repositories.
- For patch work, first read the [aura-game-patch-release skill](.agents/skills/aura-game-patch-release/SKILL.md), then check the App repository’s rules and actual protocol.
- Once published, `packages/<id>/<version>.zip` must not be replaced or deleted. Increment the version for updates and keep old backups restorable.
- The old `mirrors-edge-widescreen-tool` was removed from the current v2 catalog and category index. Do not automatically restore the listing. Keep the historical ZIP, sources, licenses, and strict v1 catalog. Delisting leaves installed entries and offline recovery intact. A user reported that the new direct install enabled 19.5:9 widescreen. Attribute this to the user rather than claiming it as a maintainer device test.
- Use `tools/patch_release.py add/check/publish` for new packages. Keep catalog.json/catalog.sig for strict v1 clients. Categories and automatic installation policy use the independently signed v2 catalog.
- Keep the signing private key outside this repository. Do not publish credentials, user diagnostics, complete game executables or assets, private App source, or obfuscation mappings. Preserve upstream sources, licenses, and corresponding source.
- Automatic installation is limited to exact-version matches for compatibility and bug fixes. Do not reinstall a patch the user disabled, uninstalled, or deleted. Tools, FPS mods, widescreen patches, and Battlefield 3 single-player mode remain manual choices.
- Verify real App integration, rollback, and failure paths before committing a release and pushing it normally. Read back the published files at the remote commit. Do not force-push or claim untested phone results.
- A copy of this skill also lives in `.agents/skills/aura-game-patch-release/` in Aura’s private source repository. Keep shared workflow changes synchronized across both copies.
