# Aura Game Patches

Aura’s repository for game-specific compatibility patches, widescreen tools, and mods. Aura matches patches against the executable it actually launches. Both Steam and Local games are supported. This repository does not contain complete game files, game credentials, or user diagnostics.

Browse by game and purpose using the [patch directory](games/README.md) or the [machine-readable index](games/index.json). Entries are grouped into compatibility, bug fixes, widescreen, mods, and tools. Existing package paths are preserved.

The [aura-game-patch-release skill](.agents/skills/aura-game-patch-release/SKILL.md) describes the maintainer workflow for integrating game-specific fixes into Aura, building reproducible packages, signing and publishing them, and verifying the published files. General Wine, FEX, and DXVK fixes ship with the Aura runtime.

## Patch list

See the [Cuphead widescreen candidate](docs/cuphead/WIDESCREEN.md) for the original sources and installation requirements. The repository lists the author’s original download links only. The third-party package has not been mirrored or added to Aura’s signed download catalog, and compatibility with Aura has not been tested.

| Game | Patch | How to install | How to revert |
| --- | --- | --- | --- |
| Crysis 2 (1.9 x86) | [Optional DX9 launch profile](docs/crysis-2/DX9.md) | Download and enable manually. Requires Aura 0.1.122 (versionCode 123) and an exact match for the supported executable. Uses only the game’s built-in `-dx9` option. | Disable or uninstall the profile, then fully restart the game to restore its original launch arguments. Game files are left intact. |
| Battlefield 3 | Single-player compatibility | Download the launch profile. It disables optional `pbcl` / `pbcl64` loading for `bf3.exe` only. | Remove the profile to restore the original behavior on the next launch. |
| Metal Gear Solid V: Ground Zeroes | Startup compatibility | Download the profile to enable the matching Wine/FEX image-page and tick-thunk support. | Remove the profile to disable it on the next launch. |
| Mirror’s Edge (2008) | Time conversion startup fix | The patch checks the full executable hash and then changes a small number of bytes. | Restore the original file from the local backup. |
| Mirror’s Edge (2008) | [19.5:9 widescreen direct install](docs/mirrors-edge/WIDESCREEN_195.md) | **App versionCode 137 or later.** Select this patch manually. It verifies the base game and DLC assets before changing a single aspect-ratio value. No separate tool is required. | Disable or uninstall the patch to restore the original assets while keeping the executable startup fix. |
| South Park: The Fractured But Whole | Virtual address allocation compatibility | The patch checks the full executable hash before changing an allocation parameter. | Restore the original file from the local backup. |
| Ground Zeroes | MGSVFix 0.0.3 widescreen | The installer copies the ASI, DLL, and INI files and sets `winmm=n,b` for this game. | Remove the added files, restore the original files, and clear the launch override. |
| Stardew Valley | [StardewFPS 1.0 experimental FPS unlock](docs/STARDEW_FPS.md) | Use **Mod → Download mod**. The mod requires SMAPI and changes animation and enemy speeds, so it is not recommended for regular play. | Disable the mod, restore the previous files, and restart. Save progress is retained. |

The Battlefield 3 single-player profile is specific to that game. It does not replace EA or Steam sign-in or authorization, emulate online services, or convert the game into a client-free offline edition. Remove the profile before playing online.

The Ground Zeroes startup package is a **configuration patch that depends on Aura’s runtime**. It requires the matching Wine/FEX support and cannot be dropped into another emulator as a standalone DLL. This repository contains the profile and its corresponding source changes. General Wine and DXVK fixes ship with the Aura runtime.

## Using patches and mods in Aura

Aura 0.1.125 separates patches and mods in Game Management. Compatibility fixes, widescreen patches, and tools are available here:

`Game Management → Patch → Download patch` for the selected game.

**StardewFPS and SMAPI** are available here:

`Game Management → Mod → Download mod` for the selected game.

StardewFPS is categorized as a `mod`, so newer builds list it under Download mod. If the Mod list is empty, reopen the download page to refresh it and check that the game entry launches `Stardew Valley.exe` or `StardewModdingAPI.exe`. Aura uses the executable to match catalog entries even when the cover art matches.

Select a patch, read its description, then choose **Download and install**. Close the game before installing. Installed patches appear below Download patch. Disabling a patch restores the original state. Uninstalling removes the patch and keeps the local package for offline reinstallation. Deleting removes Aura’s saved package and backups. `Import patch` accepts ZIP archives and extracted files and limits changes to the selected game directory.

The Mod page offers the same controls, with installed mods listed below Download mod. On older versions without a separate Mod page, mods still appear under Patch. Existing mods do not need to be reinstalled after the categories change.

### Automatic installation for new fixes

The newer protocol uses the separately signed `catalog-v2.json` and `catalog-v2.sig`. Compatible Aura versions check for patches when preparing a new game session. Aura can automatically download and enable a compatibility or bug fix patch, with backups of affected files, only if the patch explicitly declares `autoInstall` and meets the minimum App version, full executable hash, and original-file checks for every target. Aura respects existing installed versions and does not override a manual decision to disable, uninstall, or delete a patch. If the device is offline or the download fails, retry or import the patch on the Patch page. Aura must first recover any interrupted file operation.

**Automatic installation and the new Crysis 2 launch policy require Aura 0.1.122 (versionCode 123) or later. Neither is available in 0.1.121. See Aura’s release notes for APK availability.** All eight packages currently in the v2 catalog remain manual. The optional Crysis 2 DX9 profile, BF3 single-player profile, widescreen patches, FPS mods, and interactive tools are outside the automatic fix policy. A successful install does not confirm how a patch works on a phone.

Game-specific executable patches check the full file size and original SHA-256, verify the old bytes at each edit, and check the resulting SHA-256. Unsupported versions are rejected even if the file is renamed. Before installing a new package for the same fix, revert the older Aura compatibility patch. Previously applied changes and local backups are retained for recovery.

### Local backups

Before installing a file patch, Aura backs up each file it will overwrite to its private on-device directory at `game-patches/<game-id>/<install-batch>/old/`. Backups stay on the device. Aura replaces files only after the backup is complete. If installation or restoration is interrupted, Aura keeps a log and blocks the game from launching until recovery is complete.

When uninstalling, Aura deletes added files and restores overwritten files from backup. If multiple patches touch the same file, uninstall the most recently applied patch first. Aura refuses to overwrite files that no longer match its records after a game update or manual edit. Clearing Aura’s data or uninstalling Aura removes these local backups. Configuration packages leave game files intact, and deleting their installation record clears the profile for the next launch.

## Stardew Valley FPS experiment

This repository includes the [StardewFPS usage guide](docs/STARDEW_FPS.md), the [Aura installation package](packages/stardew-fps-experimental/1.0.0-aura1.zip), the original mod, corresponding source code, and its MIT license. In newer builds, go to **Mod → Download mod → Experimental FPS unlock (SMAPI)**. Launch the game through the Windows version of SMAPI, load a save, turn off in-game VSync, and enter `fps 120` in the SMAPI console. The package contains the mod only. Aura builds with dependency management can install the pinned SMAPI version for a selected or enabled mod and switch the launch executable. The FPS command is entered manually. The mod changes animation and enemy speeds and does not reduce the rendering cost behind the current sub-60 FPS issue. Compatibility with Wine/ARM64EC on phones has not been verified.

## Widescreen patches and tools

Mirror’s Edge uses the [19.5:9 direct install package](docs/mirrors-edge/WIDESCREEN_195.md). It supports resolutions with that aspect ratio, such as 1560×720, and requires **App versionCode 137 or later**. A user reported that the new package enabled widescreen. Other asset versions and devices have yet to be verified.

The old **Widescreen repair tool / Mirror’s Edge Tweaks** was removed from the v2 download catalog and patch index to avoid confusion. Refresh the list in Aura’s Download patch page to see the current entries. If the old tool is already installed, you can still disable, uninstall, or delete it from the Patch page. Existing backups remain available. The published ZIP, source and license information, and strict v1 catalog are retained for reference. The new widescreen package works independently of the old tool.

Original packages are stored unchanged in [upstream](upstream). The Aura installation packages referenced by the signed catalog are in [packages](packages).

### Ground Zeroes / MGSVFix

- [Lyall](https://codeberg.org/Lyall/MGSVFix) released the original [0.0.3](https://codeberg.org/Lyall/MGSVFix/releases/tag/0.0.3) under the MIT license.
- The Aura installer puts the files next to `MgsGroundZeroes.exe`. Wine is configured to prefer native `winmm` for this game only. Shared container settings are left intact.
- Aura’s package disables the original mod’s intro skip and FPS unlock by default. Resolution, aspect-ratio, and HUD fixes stay enabled. The original ZIP is unchanged.
- The patch uses the resolution selected in-game and preserves the S24 Ultra’s 13:6 aspect ratio. Options include 3120×1440, 2340×1080, and 1560×720. The maximum resolution depends on the current container.
- ASI loading and visual results under Wine/ARM64EC still need verification on the target phone. A successful install confirms file installation only.

### Mirror’s Edge Tweaks (archived and removed from the current download catalog)

- [softsoundd](https://github.com/softsoundd/MirrorsEdgeTweaks) released the original [4.5.0-beta3](https://github.com/softsoundd/MirrorsEdgeTweaks/releases/tag/4.5.0-beta3) under GPL-3.0. This repository includes the corresponding source code.
- The package contains `Mirror's Edge Tweaks.exe` and requires the Windows .NET 10 Desktop Runtime. It is an interactive tool, with no verified unattended installation interface. Copying it into the game directory does not apply a patch.
- Aura places the tool in `AuraPatchTools/MirrorsEdgeTweaks/` next to the game executable. Run it in a Windows or Wine environment that supports it, select the game directory, then apply the FOV fix and your chosen resolution.
- The tool can modify Unreal packages, configuration files, and other files. **Rolling back the tool download in Aura does not undo changes the tool made later.** Back up the game files and configuration before running it, and follow the tool’s restoration instructions. The download button installs the tool only.
- This version’s .NET 10 WPF interface has not been tested on a phone under Wine/ARM64EC. If needed, use the tool on your own copy of the game on a PC, then use Aura’s Import patch to bring in the modified files with Aura’s file-level backup and restore support.

## Catalogs, checksums, and maintenance

- [catalog-v2.json](catalog-v2.json) is the signed v2 catalog. It includes game categories and rules for future automatic installation based on exact matches. All eight current packages require manual selection.
- [catalog.json](catalog.json) preserves the original catalog and its signature for strict v1 clients. New protocol fields are kept out of v1.
- [catalog.sig](catalog.sig) is the detached Ed25519 signature. [catalog-public-key.pem](catalog-public-key.pem) contains the public key. The private catalog-signing key is kept outside this public repository and is separate from the APK signing key.
- [SHA256SUMS](SHA256SUMS) contains checksums for installation packages, original upstream packages, and source archives.
- [sources](sources) contains upstream source archives and the Ground Zeroes runtime changes.
- [licenses](licenses) contains author licenses and third-party notices.
- [tools/patch_release.py](tools/patch_release.py) builds, signs, categorizes, checks, and publishes patches reproducibly. It uses a private key stored outside the repository and does not rotate the trust root automatically. Commands and recipes are in the [maintenance guide](.agents/skills/aura-game-patch-release/references/workflow.md). The historical `build_catalog.py` is kept to trace older packages and is not used to add packages or rebuild the current catalog.

Installation packages can only copy files within the supported scope, apply exact byte edits, and set supported launch options. Aura does not execute scripts bundled in a patch. Leave published version directories intact. For an update, bump the version, rebuild, and sign again. New types of native code or runtime capabilities require support in the corresponding App version.

## Sources and licenses

Aura’s own catalogs, patch definitions, and packaging scripts are available under the [MIT license](LICENSE). Third-party works retain their original licenses. The notices for MGSVFix, Ultimate ASI Loader, safetyhook, Zydis/Zycore, mINI, and StardewFPS are in `licenses`. The corresponding source code, GPL license texts, and third-party notices for Mirror’s Edge Tweaks and NativeSharpLzo are also included. See the original projects’ files for build dependency versions.

Game-specific executable packages contain only small modification recipes, not complete proprietary executables. Names and trademarks belong to their respective owners. No gameplay performance gain or target-device compatibility is claimed without device testing.
