# StardewFPS: Experimental FPS unlock

Lake1059’s **StardewFPS 1.0** mod changes Stardew Valley’s target update rate. **It changes game timing and does not optimize rendering.** If a frame takes more than 16.67 ms to process at native resolution, removing the 60 FPS cap will not reduce that cost.

## Limitations

- The author states that animation and enemy speeds change with the selected FPS and advises against using the mod for regular play. Back up your saves first and avoid using your main save for experiments. Removing the mod cannot undo saved progress.
- The upstream release is dated 2024-03-22 and lists support for Stardew Valley 1.6. Newer game or SMAPI versions and Aura’s Wine/ARM64EC environment on phones have yet to be verified.
- Install the **Windows version of SMAPI** that matches your game, then launch through `StardewModdingAPI.exe`. The original game executable does not load the mod on its own.
- This ZIP contains only the mod. On Aura versions with dependency management, installing or enabling it installs the pinned official SMAPI release as needed, and Aura selects the SMAPI launcher when enabled. Extracting the ZIP manually does not install dependencies. The package leaves the game executable, FPS, and VSync settings intact and does not run commands automatically.
- The main menu stays at 60 FPS. Enter the command again after each launch. Setting a higher target does not guarantee the device can reach it.

## Installation and use

1. Exit the game completely. In Aura 0.1.125, open **Game Management → Mod → Download mod** for Stardew Valley, then select **Experimental FPS unlock (SMAPI)** and install it. Newer versions list it under Mod. The catalog matches the actual launch executable and supports `Stardew Valley.exe` and `StardewModdingAPI.exe`.
2. Aura installs the files to `Mods/StardewFPS/` next to the game executable and installs the pinned official Windows SMAPI if needed. The bundled dependency selection is SMAPI 4.5.2, which requires Stardew Valley 1.6.14 or later. Aura rejects incompatible game versions. If the dependency download fails, retry or use Import mod to select the official ZIP for the same supported version. Both installed entries appear below Download mod.
3. Make sure SMAPI and the mod are enabled, then use Aura’s Start game button. Enabling SMAPI makes Aura launch `StardewModdingAPI.exe`. Check the console for a successful mod load. The diagnostic field `selected=SMAPI` only confirms the selected executable. On older Aura builds without dependency management, or when installing manually, follow the [official SMAPI instructions](https://smapi.io/) to install the matching Windows version, then copy the `StardewFPS` folder from `upstream/StardewFPS.1.0.0.zip`.
4. Turn off in-game VSync, load a save, then enter `fps 120` in the **SMAPI console**. Wine CMD, the in-game chat box, and the Android terminal do not accept this command. Use positive integers only, since the upstream mod does not fully validate its arguments. Try `fps 60` before testing 90 or 120. The main menu stays at 60 FPS, and you must enter the command each time you launch the game.
5. To disable the mod, fully exit the game, open the installed StardewFPS entry on the Mod page, disable it, and relaunch. Uninstalling restores the original files and keeps a local copy for offline reinstallation. Deleting also removes that copy. Disabling does not require deleting anything. Before disabling SMAPI, disable all mods that depend on it. For a manual install, remove `Mods/StardewFPS` yourself. The `fps 60` command restores the target for the current session. To restore default timing fully, disable the mod and restart.

On older versions without a separate Mod page, the package appears under Patch → Download patch. The previously published ZIP retains its original instructions. This page describes the menus and dependency behavior in newer Aura versions.

An Aura installation record confirms that files were copied. Use the SMAPI console to confirm that dependencies loaded and the mod took effect. For Aura installs, overwritten mod files are backed up locally and restored according to the installation record when deleting the patch. Manual installs do not have Aura’s automatic rollback.

## Source and license

- Author: [Lake1059](https://github.com/Lake1059).
- [GitHub 1.0 Release](https://github.com/Lake1059/StardewFPS/releases/tag/1.0). The original binary ZIP is unchanged.
- [Corresponding source code](https://github.com/Lake1059/StardewFPS/tree/a3bf5bdd1f45fadcec0e7d0fa5b84b8b4b0ade12), commit `a3bf5bdd1f45fadcec0e7d0fa5b84b8b4b0ade12`. The full archive is in `sources/StardewFPS-1.0.tar.gz`.
- Redistribution follows the MIT LICENSE.txt from that GitHub release. The full license text retains the upstream `[year] [fullname]` placeholders exactly as provided. The author is credited here. This package comes from GitHub, and the Nexus download is not mirrored.
- [Author’s description and limitations](https://www.nexusmods.com/stardewvalley/mods/20801). The code only sets `TargetElapsedTime = 1 / fps` and `IsFixedTimeStep = True`. It does not separate animation or enemy updates from the display rate.

The package adds this guide and the MIT license while leaving the upstream DLL and manifest unchanged. See `SHA256SUMS` at the repository root for the original ZIP, source archive, and Aura package hashes.
