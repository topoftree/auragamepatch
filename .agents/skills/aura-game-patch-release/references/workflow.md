# Workflow and commands

Find the repositories by their remotes. The App remote is `topoftree/winlator` and the public patch remote is `topoftree/auragamepatch`. The original environment used `/workspace/audit-winlator` and `/workspace/auragamepatch`. Verify the paths when the environment changes. Python 3.10 or later, OpenSSL with Ed25519 support, and Git are required. Use the proxy and credentials configured for the environment.

## Repository layout

```text
.agents/skills/aura-game-patch-release/   # Public copy of this skill, without App source
recipes/<game>/<category>/<id>/<version>/recipe.json
recipes/<game>/<category>/<id>/<version>/payload/  # Redistributable inputs
packages/<id>/<version>.zip              # Immutable packages, including old versions
games/index.json                         # Generated game and category index
games/README.md                          # Generated browsable directory
docs/<game>/                             # Usage instructions and validation evidence
licenses/                               # Original licenses and third-party notices
sources/                                # Modified and required corresponding source
upstream/                               # Unmodified redistributable upstream packages
catalog-v2.json + catalog-v2.sig         # Signed catalog for newer App versions
catalog.json + catalog.sig               # Retained for older clients
```

`tools/patch_release.py` is maintained in this public repository. Run `check` first to verify the current signatures and packages. Use `add` to merge a new package into the existing v2 catalog while retaining entries for other games. The tool rejects different bytes under an existing version. Increment the version for updates and keep older ZIPs.

## Recipes

The top level of `recipe.json` contains `schema: 1`, `entry`, optional `binary` and `files`, and `provenance`. `entry` includes `id/version/title/description/executables/kind/policy/game/category` and optional `autoInstall`. The tool generates `path/bytes/sha256`. The complete field definitions follow the App’s Kotlin data classes.

Set `minAppVersionCode` on the entry when a package needs installation or startup support from a newer App version. Older clients can hide unsupported entries before reading their policies, so an unknown policy does not invalidate the whole catalog. The automatic rule cannot specify a lower minimum. New protocol fields still require a controlled upgrade of strict decoders.

Use `[{"source":"payload/fix.dll","target":"fix.dll"}]` for `files`. The source must be inside the recipe directory, and the target is relative to the actual launch executable’s directory. `binary` maps to the App’s `PackageBinaryPatch` and uses `bytes/before/after/edits`. Each edit has `offset/before/after`.

Resource edits use recipe and manifest `schema: 2` with `resourceBinary: {path, variants}`. Each variant follows the `binary` structure. Currently only `mirrors-edge-widescreen-195` is allowlisted. The fixed target is `TdGame/CookedPC/Engine.u` in the same game root as `Binaries/MirrorsEdge.exe`. `../` is not allowed. Each variant is capped at 16 MiB and requires full before-and-after hashes. Only one fixed 16:9 to 19.5:9 float edit is permitted. Require at least App versionCode 137 and keep this patch manual. Keep this capability out of schema 1 and retain the old packages and catalogs.

`provenance` contains `upstream` (an HTTPS source URL), `license` (a license file in the repository), and `validation` (a validation file in the repository). For automatic installation, the validation file must be JSON. Include actual Boolean results for `installRestoreTested/versionMismatchTested/activationTested` and the full tested `appCommit`. Include the test commands, results, and whether the patch was tested on a phone. Only record a passing result when the check passed.

Example automatic rule. Replace placeholders with verified values before signing a real catalog.

```json
{
  "minAppVersionCode": 123,
  "executable": {"bytes": 12345, "sha256": "64 lowercase hexadecimal characters for the original EXE SHA-256"},
  "targets": [
    {"path": "fix.dll", "before": null},
    {"path": "config.ini", "before": {"bytes": 456, "sha256": "SHA-256 of the original file"}}
  ]
}
```

For binary and profile patches, use an empty target list. For a binary patch, the executable baseline must match the recipe’s before value. For file patches, list exactly every installation target, including newly added license files. Do not automatically overwrite unknown files or targets already owned by another patch. VersionCode 123 was reserved for the first implementation of this protocol. If the required capability ships later, use the actual versionCode.

## Commands

Run these from the patch repository root. Substitute verified paths and use normal shell quoting.

```bash
python3 tools/patch_release.py check
python3 tools/patch_release.py add \
  --recipe recipes/GAME/CATEGORY/PATCH/VERSION/recipe.json \
  --key /private/location/game-patch-catalogue-ed25519.pem
python3 -m unittest discover -s tools/tests -v
python3 tools/patch_release.py check
git diff --check
git diff --stat
python3 tools/patch_release.py publish --message "Add GAME compatibility repair VERSION"
```

The current private key is in the App repository at the ignored path `.signing/game-patch-catalogue-ed25519.pem`. This path grants no permission to read other credentials or upload the key. If the key is unavailable, keep the unpublished work and report the missing signing environment. Do not create a replacement key for the App’s trust root.

Run the App’s Gradle checks for `GamePatchAutomaticTest`, `GamePatchPackageTest`, `GamePatchLifecycleTest`, and the startup tests for the new policy. For SMAPI work, use the official package with its pinned SHA-256 in the existing integration tests. New capabilities require updates to the App allowlist, tool allowlist, and tests. Verify the App integration in addition to checking package integrity.

The release tool rejects unknown remotes, deletion of public files, replacement of published ZIPs, and unrelated artifacts such as keys, APKs, and mappings. It only permits fast-forward pushes. After publication, verify changed files at the exact remote commit URL. If a failure occurs after the push, check the remote head and files before retrying. Do not recreate the same package version.

If the push succeeds and network access fails during readback, use `python3 tools/patch_release.py readback --commit FULL_COMMIT_SHA` to retry verification without pushing or replacing a package.

## Report each verification level separately

1. Reproducible packaging, signing, and package validation passed.
2. App installation, recovery, startup policy, and negative cases passed.
3. The repository publication and remote readback succeeded.
4. The companion App APK was built or delivered. This skill does not authorize that step.
5. The user’s phone gameplay was verified.

Verify game startup, mod loading, and FPS in the game itself. Passing installation or startup policy checks establishes only that those steps work.
