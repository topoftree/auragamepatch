# Source provenance

- `MGSVFix-0.0.3.tar.gz`: https://codeberg.org/Lyall/MGSVFix/archive/0.0.3.tar.gz (tag 0.0.3). MIT; submodule URLs and build instructions are retained in the archive.
- `MirrorsEdgeTweaks-4.5.0-beta3.tar.gz`: https://github.com/softsoundd/MirrorsEdgeTweaks/archive/98b54444998ec4e67dc085ad088b1fe6a3454032.tar.gz (tag 4.5.0-beta3). GPL-3.0; .NET 10 WPF source, build workflows, dependency versions and third-party notices included.
- `NativeSharpLzo-0.3.5.tar.gz`: https://github.com/BigBang1112/NativeSharpLzo/archive/298767511961fec0ad9585d782b3bdb5a08f5e00.tar.gz (tag v0.3.5), used by the above tool. GPL-3.0 with LZO under GPL-2.0-or-later.
- `lzo-2.10.tar.gz`: https://www.oberhumer.com/opensource/lzo/download/lzo-2.10.tar.gz, native library version pinned by NativeSharpLzo 0.3.5’s release build workflow, which is included in its source archive.
- `ground-zeroes/`: exact source modifications for the runtime capabilities selected by the downloadable Ground Zeroes launch profile. FEX changes use its MIT license; Wine changes use LGPL-2.1-or-later. These files document the required runtime implementation; installing the profile does not hot-swap Wine/FEX binaries.

The original upstream binary ZIPs are unmodified. The Aura MGSVFix install package only changes its default INI to disable intro skipping and FPS unlocking, and adds license texts. SHA-256 sums are at the repository root.
