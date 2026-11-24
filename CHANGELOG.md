# Changelog

## 2026-10-26 — Cuphead widescreen source links

- Added the original Cuphead UltraWide 1.1.0 download pages, BepInEx and architecture requirements, visual limitations, and differences from older fixes.
- Listed the original links because the author prohibits unauthorized reuploads and this repository has no redistribution permission. The DLL and ZIP were not mirrored, the signed catalog did not change, and Aura automatic installation remains unimplemented. A future package still requires permission, an exact game baseline, and full lifecycle verification.

## 2026-10-25 — Removed the old Mirror’s Edge widescreen tool from downloads

- A user reported that the new 19.5:9 direct install patch enabled widescreen. Removed the old `mirrors-edge-widescreen-tool` from the signed v2 download catalog and current category index to prevent confusion between the two entries. The new resource patch, executable startup fix, and other entries were retained.
- Kept the published tool ZIP, source, licenses, checksums, and strict v1 catalog. Installed entries, disabling, uninstalling, and offline recovery do not depend on the current download catalog. Local backups can stay in place. The new package does not depend on the old tool.
- Updated the instructions to distinguish user feedback, historical installation verification, and the supported scope. This change did not build an APK or alter game files or the new patch bytes.

## 2026-10-25 — Mirror’s Edge 19.5:9 direct widescreen resource patch

- Added manual patch `mirrors-edge-widescreen-195` 1.0.0. It verifies known base game and DLC Engine.u files and applies a four-byte aspect-ratio change. The package contains no game assets and does not require Tweaks or .NET. The old tool and previously published packages were retained. The patch can coexist with the executable startup fix.
- App versionCode 137 adds support for restricted schema 2 resource variants, full before-and-after hashes, and backup recovery. Older App versions hide this entry. A newer APK is required. This package targets 19.5:9 only and does not cover adjustable FOV, HUD, or videos.
- Installation, restoration, and post-edit decompression checks passed for four reference resources. Also passed 65 App checks and 10 release-tool tests. The original v1 catalog was retained. The in-game result on phones and the match against the user’s local resource version still needed checking. See the [instructions](docs/mirrors-edge/WIDESCREEN_195.md) and [validation record](docs/mirrors-edge/widescreen-195-validation.json).

## 2026-10-23 — Corrected the StardewFPS download instructions

- Read back the pinned GitHub commit and the main-branch catalog used by the App. StardewFPS 1.0.0-aura1 remained available, and the catalog signature and full package hash passed. The published package was neither reuploaded nor replaced.
- Updated the README and guide to use Game Management → Mod → Download mod in Aura 0.1.125 and explain why the mod does not appear in Download patch. Added SMAPI dependency installation, launcher selection, and the differences between disabling, uninstalling, and deleting.
- Preserved the experiment’s limitations. The FPS command must be entered manually, animation and enemy speeds can change, and this mod does not address performance below 60 FPS. Phone compatibility remained unverified.

## 2026-10-23 — Crysis 2 optional DX9 profile 1.0.0

- Added `crysis-2/compatibility/crysis2-dx9` using the game’s built-in `-dx9` argument. It matches the verified 1.9 x86 executable, requires Aura 0.1.122 (versionCode 123), leaves game EXE and CFG files intact, and requires manual selection.
- Completed App support for downloading and importing, enabling and disabling, retaining the package after uninstall, reinstalling offline, deleting, and passing the launch argument. Aura checks the version on installation, reactivation, and each launch. Passed 38 App checks and eight release-tool tests. The real baseline was checked read-only in a private workspace. The older packages and v1 catalog were retained.
- Withdrew the earlier CFG comparison because this build’s allowlist filters `r_Driver`. Actual DX9 loading and any improvement to phone startup stalls or cropping remained unverified. See the [instructions](docs/crysis-2/DX9.md) and [validation record](docs/crysis-2/validation.json).

## 2026-10-23 — Patch maintenance skill and automatic installation protocol

- Added the repository skill, AGENTS trigger rules, deterministic packaging, signing, validation, and publishing tools, and corresponding tests. The user gave ongoing authorization to release later game-specific fixes after verification. That authorization does not automatically extend to App source or APK publication.
- Categorized the seven existing packages by game and purpose and added the signed v2 catalog. The original catalog and published ZIPs were retained byte for byte. Updates must increment the version and keep the old package.
- Limited automatic installation to eligible fix categories, minimum App versions, exact executables, and exact target-file baselines. The App source checks before startup, installs and enables matching fixes, and honors manual choices. The seven existing packages remained manual. No demonstration patches were published.
- Updated the newer Patch menu paths and SMAPI dependency instructions. This change did not build an APK. Aura 0.1.121 does not read the automatic installation protocol. No additional phone gameplay testing was performed.
