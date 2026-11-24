# Mirror’s Edge (2008) 19.5:9 widescreen direct install

In **Game Management → Mirror’s Edge → Patch → Download patch**, select **Mirror’s Edge · 19.5:9 widescreen (direct install)**. It requires **Aura versionCode 137** or later. Aura 0.1.135 (code 136) hides the entry. Do not manually import this schema 2 package on earlier versions.

This package applies a small resource edit directly. The old **Mirror’s Edge Tweaks / Widescreen repair tool** was interactive and was removed from the v2 download catalog. The direct install package has no Tweaks or .NET dependency and does not execute scripts.

Use it for 19.5:9 resolutions such as **1560×720, 2340×1080, or 3120×1440**. Exit the game completely before installing. Select the matching resolution and fullscreen in-game, then restart. This patch is specific to 19.5:9. It does not add adjustable FOV or fix the HUD or prerecorded videos. Intro videos may still have black borders.

## What the patch changes

The patch targets `TdGame/CookedPC/Engine.u` in the game root containing `Binaries/MirrorsEdge.exe`. It replaces a single little-endian float, `f38ee33f` (about 16:9), with `abaa0a40` (19.5:9). It leaves the executable intact and can be used with the `mirrors-edge-time` startup compatibility patch.

The table lists the four supported resource baselines. The installer verifies file size, the full SHA-256 before and after editing, and the original bytes at the edit location. Other releases and resources already changed by Tweaks or a mod are rejected even if they have the same filename. A user reported that this package enabled widescreen, but their resource hash was not recorded, so the exact matched baseline is unknown.

| Baseline | Bytes | Edit offset (decimal) |
| --- | ---: | ---: |
| Base game, original LZO-compressed package | 1,662,824 | 645,379 |
| DLC, original LZO-compressed package | 1,669,463 | 646,328 |
| Base game, decompressed UE3 package | 6,109,346 | 2,694,461 |
| DLC, decompressed UE3 package | 6,113,320 | 2,695,252 |

The [declarative recipe](../../recipes/mirrors-edge-2008/widescreen/mirrors-edge-widescreen-195/1.0.0/recipe.json) records the full hashes before and after the edit. The patched compressed files still decompress successfully. Only the matching four bytes differ in the decompressed output, so the phone does not need to recompress the entire UE3 resource.

## Recovery and verification

Disabling restores the full pre-install resource. Re-enabling uses Aura’s retained local copy. Uninstalling restores the resource and keeps the package for offline reinstallation. Deleting restores the resource and removes Aura’s copy and receipt. Original resource backups stay on the device. Aura refuses to overwrite files after a game update, manual edit, or conflict with a later patch. Interrupted operations use the existing transaction recovery flow.

The launch diagnostic `MIRRORS_EDGE_WIDESCREEN_V1 resource=BYTES_VERIFIED` means Aura verified the full installed file hash again before launch. `MISMATCH` means the file differs from the installation record. The in-game result needs a visual check and remains labeled `game_effect=UNCONFIRMED`.

See the [initial validation record](widescreen-195-validation.json) for real resource checks, Aura installation and recovery, and negative cases. **On 2026-10-25, a user reported that the new package enabled widescreen on their device.** Maintainer testing on phones and verification across other devices, aspect ratios, and prerecorded videos remain open.

Removing the old tool from the download catalog leaves installed entries, tool files, and recovery backups available on devices. The two packages are independent. If you downloaded the old tool but never ran it, you can uninstall or delete it from its existing entry. If you used Tweaks to change the game, use the tool’s own recovery records. Aura’s tool download rollback covers the installed tool files only. The repository retains the old ZIP, source, and license for reference.

## Sources and reproduction

- Known method: [WSGF Mirror’s Edge](https://www.wsgf.org/dr/mirrors-edge).
- Reference files: `Base_Engine.zip` and `DLC_Engine.zip` from the [upstream Tweaks runtime-assets release](https://github.com/softsoundd/MirrorsEdgeTweaks/releases/tag/runtime-assets). These files were analyzed locally. Neither complete nor partial game assets are included in the repository or patch.
- The UE3 chunk layout was checked against the upstream `DecompressionService.cs`. The pinned source is in `sources/MirrorsEdgeTweaks-4.5.0-beta3.tar.gz`, and the upstream GPL text is in `licenses/`. The new recipe and standalone Python verifier are covered by the repository’s MIT license. They do not repackage the upstream tool or its native decompression DLL.
- `tools/verify_mirrors_edge_widescreen.py` pins the full hashes of the external reference ZIPs. In a separate Python environment, install `lzokay==2.1.0` and run `python3 tools/verify_mirrors_edge_widescreen.py --reference-dir /path/to/reference-zips`. It validates the full hashes before and after the edit, correct decompression, and the exact four-byte difference for both compressed resources and their decompressed counterparts. It does not download files or run the game or downloaded programs.
