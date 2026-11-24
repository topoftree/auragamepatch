# Crysis 2 1.9: Optional DX9 launch profile

This manual compatibility profile uses the game’s built-in `-dx9` argument. It requires Aura **0.1.122 (versionCode 123)** or later. Aura 0.1.121 does not support this policy. See Aura’s release notes for APK availability.

The profile leaves the executable, configuration files, resolution, saves, and video settings intact. DX9 may affect which DX11 effects are available. **Whether this resolves startup stalls or image cropping on Android is still unconfirmed.** Verify that the game actually loads `CryRenderD3D9.dll` and check the result on screen. An early probe for `d3d9.dll` or the presence of the launch argument is insufficient.

## Verified version and rationale

- Original Crysis 2 1.9.0.0, 32-bit, `Crysis2.exe`, 40,670,208 bytes.
- SHA-256: `0079d15b5b85a1ec7e50bb5e59c14eb255ffc247f2ac87e67b65b402bc8a7d91`.
- The analysis used only a read-only examination of the user-provided file. This repository does not contain the full game files or user logs.
- The game’s own allowlist filters `r_Driver` out of `system.cfg` and `user.cfg`. The earlier single-line diagnostic CFG, `r_Driver = "DX9"`, cannot select DX9 in this build. Moving or renaming that file will not help.
- The static call chain uses allowlist object `0x170e5b8` and match function `0xf385ee`. Configuration handler `0x467c40` sets the CVar only after the allowlist check. The native DX9 argument branch at `0x480591–0x4805f8` sets `r_Driver` directly. These are PE virtual addresses for the SHA-256 above.
- This confirms that the game accepts `-dx9` independently of CFG filtering. Reaching the main menu still requires a game run.

## Use and recovery

1. Update to a supported version of Aura and fully exit the game.
2. For this game, open **Game Management → Patch → Download patch**, select this profile, and download and install it. The profile is manually selected and is excluded from first-launch automatic fixes.
3. Find the installed entry below Download patch. Make sure it is enabled, then launch normally.
4. Aura verifies the supported executable when installing, re-enabling, and starting a new session. An incompatible version is rejected on install or re-enable. If a game update makes an existing profile incompatible, Aura skips the DX9 argument and records why.
5. After disabling the profile, fully restart the game to restore the original arguments. Uninstalling retains a local copy for offline reinstallation. Deleting clears Aura’s saved profile. The setting cannot switch during a running session.

You can disable or uninstall the earlier single-line diagnostic CFG from its own management entry and restore it through Aura’s existing backup workflow. This profile does not remove that file or overwrite other CFG files. Disabling the profile also preserves any `-dx9` argument you set separately.

`GAME_RENDERER_PROFILE_V1` reports whether the argument was prepared, the executable did not match, or the file could not be read. The actual renderer remains unconfirmed. Host checks for installation, recovery, and launch arguments are in the [validation record](validation.json). The profile and packaging are covered by the repository’s MIT license. Neither Crytek’s proprietary executable nor its disassembly is included.
