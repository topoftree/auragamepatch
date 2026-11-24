# Cuphead widescreen candidate and original downloads

**External links only.** The package is not mirrored or listed in Aura’s signed download catalog. Widescreen behavior in Aura and on phones has yet to be tested.

## Cuphead UltraWide

- Author: [opaaaaaaaaaaaa’s Cuphead UltraWide](https://www.nexusmods.com/cuphead/mods/122).
- The [original files page](https://www.nexusmods.com/cuphead/mods/122?tab=files) lists mod version 1.1.0, dated 2026-07-17, at 4 KB.
- The [author’s GitHub release](https://github.com/gabrielsitta4/game-mods/releases/tag/Cuphead-CupheadUltraWideBepInEx-v1.1.0) provides the same version as a ZIP and links back to Nexus mod 122. The author’s repository README links to the same Nexus account and mod. Download from the original release page.
- The author describes a BepInEx/Harmony camera patch that automatically adjusts to the display aspect ratio between 16:9 and 2.39:1. It expands the visible scene and forces Overscan to 0. Some scripted scenes may expose the edges of the background.
- The plugin goes at `BepInEx/plugins/CupheadUltraWideBepInEx.dll`. Version 1.1.0 refers to the mod. Check game version compatibility separately.

The author describes [BepInEx for Cuphead](https://www.nexusmods.com/cuphead/mods/173) as the official BepInEx 5.4.23.5 **x64** package. Check the architecture of Cuphead.exe before using it. An x64 loader cannot be used with the x86 game.

The author’s Wine/Proton instructions require `winhttp=n,b`. This loading requirement has yet to be verified in Aura and is not configured automatically. To verify loading, check `BepInEx/LogOutput.log` and the camera patch logs. The page does not provide exact game builds, managed assembly hashes, or a complete DLC compatibility list, so verify the widescreen effect in-game.

## Original links and redistribution

The author’s upload permissions checked on 2026-10-26 say:

> You are not allowed to upload this file to other sites under any circumstances.

Modifications also require the author’s prior permission. This repository has no authorization to mirror the DLL or ZIP. It lists the original links and does not redistribute modified proprietary game assemblies. Official BepInEx is licensed separately. Check its upstream license and corresponding source obligations before distributing the loader.

A read-only inspection of the author’s GitHub asset `CupheadUltraWideBepInEx-1.1.0.zip` found a 4,960-byte ZIP with SHA-256 `c21604053f8e09017c1526d24186d87fbcf3d47883b48ec0b5aa53cdd08acb8e`. It contains only the 10,240-byte plugin DLL and its parent directory. No source or license is bundled. The inspection did not execute the DLL or establish redistribution rights or phone compatibility.

Before adding a legally redistributable package to the signed catalog, verify the supported game build, loader architecture, existing DLL overrides, and Aura’s download, enable, disable, uninstall, and conflict recovery behavior. Keep installation a manual choice.

## Older alternatives

[Mod fix ultra-wide screen](https://www.nexusmods.com/cuphead/mods/90) replaces `Cuphead_Data/Managed/Assembly-CSharp.dll`. Its author says it only removes some black borders. Boss fights and tutorial areas still use 16:9 assets. The older [WSGF fix](https://www.wsgf.org/phpBB3/viewtopic.php?f=64&t=32324) targets versions 1.00, 1.1.3, and 1.1.4. Compatibility with current builds remains unverified.

This candidate addresses aspect ratio. Any effect on the stock driver’s dark image, flicker, or performance remains unverified.
