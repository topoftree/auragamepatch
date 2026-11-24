---
name: aura-game-patch-release
description: Build, categorize, verify, and publish Aura game-specific compatibility and bug fixes to topoftree/auragamepatch, with App integration for automatic download, installation, activation, and recovery. Use this skill when fixing a specific game, adding or updating a patch, or changing its lifecycle. General Wine/FEX/DXVK engine fixes stay in the App runtime.
---

# Aura game patch releases

On 2026-10-23, the user explicitly authorized packaging and uploading future game-specific compatibility and bug fixes to `topoftree/auragamepatch`, with categorization and matching App support for automatic download, installation, and activation. This authorization continues within that scope. Publish directly after meeting the evidence and verification requirements. Follow any later, more specific user instructions.

This skill applies when working on a relevant Aura patch task. It creates no background job. If source, keys, network access, or verification conditions are missing, report the specific gap and complete any remaining work you can verify. Report publication and game results only when confirmed.

## 1. Confirm the scope of the fix

1. Read the project’s `AGENTS.md`, the [workflow and protocol](references/workflow.md), and the App’s `docs/GAME_PATCH_DOWNLOADS.md`. Check the worktrees and remotes for both repositories and preserve user changes.
2. Identify the problem, game, actual launch executable, architecture, release version, original file size and SHA-256, reproduction evidence, and expected behavior. Steam IDs can help with lookup. A Local entry’s cover ID does not establish game identity. Analyze game files and user diagnostics locally.
3. Keep general memory, presentation, synchronization, and driver fixes in the runtime. Use this repository for executable-specific byte edits, version adaptations, profiles, and mods. If a patch depends on runtime support, implement and test that support and state the minimum App version.
4. Store the recipe under `game → category → patch-id → version`. Allowed categories are `compatibility`, `fix`, `widescreen`, `mod`, and `tool`. Do not reclassify an FPS mod or interactive tool as a fix to make it eligible for automatic installation.

## 2. Build a reproducible package

Use the existing declarative manifests: `binary` for exact byte edits, `files` for copies relative to the actual executable, `profile` for App allowlisted configuration, and `tool` for tool files only. Do not add downloaded-script execution, arbitrary commands, absolute paths, writes outside the game root, or unsupported launch arguments.

- Put packages at `packages/<id>/<version>.zip`. Published versions are immutable. Keep source, upstream provenance, licenses, and verification records in the repository and comply with the upstream license’s corresponding-source obligations.
- Publish only the necessary recipes and redistributable components. Exclude full game executables or assets, credentials, raw diagnostics, APK signing material, catalog private keys, R8 mappings, and standalone App source.
- For byte edits, require full before-and-after SHA-256 hashes, file size, and the old and new bytes at each edit. Validate versions using the contents of the file.
- Do not publish fabricated patches, tests, or demonstration packages. Keep temporary fixtures out of the public catalog.

## 3. Integrate with the App

Read and reuse `GamePatchCatalog`, `GamePatchPackage`, `GamePatchRepository`, `GamePatchFiles`, `InstalledGamePatchPolicy`, and `GamePatchAutomatic`. App support must include working integration.

- `catalog-v2.json` and `catalog-v2.sig` define categories and automatic installation. Keep `catalog.json` / `catalog.sig` compatible with older clients and keep new fields out of strict v1 decoders.
- Only verified compatibility and bug fixes may declare `autoInstall`. Specify the minimum App versionCode, exact executable baseline, and original baseline for every target. `before: null` means the target must not exist. Before launch, match the baselines, download, verify the signature and hash, acquire the storage lease, recheck, then install and enable.
- Do not automatically replace an installed version or restore a patch the user disabled, uninstalled, or deleted. Recover interrupted operations first. Do not change files or the session snapshot while the game is running. For offline, timeout, or mismatch cases, leave game files intact, record the reason, and let the user retry or use Import patch under Library → game details → Patch.
- If a package needs a new configuration key, DLL loading, or a loader dependency, add narrow support scoped to the game, including the App launch snapshot and tests. Update the tool allowlist and minimum App version. Reject unknown keys explicitly. There is no generic post-download installer execution.
- Keep Battlefield 3 single-player mode, widescreen patches, FPS unlocks, experimental mods, and interactive tools manual. Install SMAPI automatically only for a dependency of a user-enabled mod. Do not automatically skip videos, change game speed, or alter client authorization or online behavior.
- Store download records in the existing Patch management page. Disabling restores the original state. Uninstalling keeps a copy for offline reinstallation. Deleting clears Aura’s copy. Original file backups stay on the device. Preserve conflict handling, interruption recovery, manual priority, and Steam/Local isolation.

## 4. Verify and publish

1. Test installation, activation, disabling, uninstalling, deleting, restoring, rejection of unknown versions, conflicts, repeat installation, manual overrides, and network failures. For automatic installation, verify the real launch call site and minimum version gate. Record host checks and phone gameplay separately.
2. Use `tools/patch_release.py add` to produce a deterministic package, sign the v2 catalog, and update categories. See the reference for commands. `build_catalog.py` is a historical full-catalog generator. Do not use it to add games.
3. Use `tools/patch_release.py check` and review the public diff, categories, documentation, corresponding source, licenses, and verification evidence. Verify against the project’s actual public key. Read the private key only from outside the repository. Never upload, print, or automatically rotate it.
4. Update this repository’s README and CHANGELOG, plus the App’s Chinese CHANGELOG, protocol documentation, and applicable AGENTS rules. Commit the tested App changes locally first and record the App commit in the automatic patch validation record.
5. From a clean, reviewed patch branch, run `tools/patch_release.py publish` to push `topoftree/auragamepatch/main`. Download the changed files by exact remote commit and verify their hashes. Fetch and inspect any concurrent changes before retrying. Do not force-push.
6. This skill grants no additional authorization to build an APK, publish to `topoftree/Aura`, or push private App source. Follow the user’s current instructions for those actions. If the companion App support has yet to ship, state that the patch repository is published and automatic installation requires a later APK.

Report the patch repository commit or catalog link, supported game version, manual or automatic policy, verification results, and any remaining phone checks. If publication fails, keep the local work and report where it stopped.
