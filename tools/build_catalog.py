#!/usr/bin/env python3
"""Rebuild deterministic Aura packages. Sign with an external Ed25519 private key."""
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SHA = lambda data: hashlib.sha256(data).hexdigest()


def build_package(name, version, title, description, executable, kind, *, policy='', binary=None, files=None):
    files = files or {}
    manifest = dict(schema=1, id=name, version=version, kind=kind, policy=policy,
                    files=[dict(source='files/' + target, target=target, sha256=SHA(data))
                           for target, data in files.items()])
    if binary:
        manifest['binary'] = binary
    destination = ROOT / 'packages' / name / (version + '.zip')
    destination.parent.mkdir(parents=True, exist_ok=True)
    entries = {'manifest.json': json.dumps(manifest, indent=2).encode()}
    entries.update({'files/' + target: data for target, data in files.items()})
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, data in sorted(entries.items()):
            info = zipfile.ZipInfo(path, (2026, 10, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    data = destination.read_bytes()
    return dict(id=name, version=version, title=title, description=description, executables=[executable],
                path=destination.relative_to(ROOT).as_posix(), bytes=len(data), sha256=SHA(data), kind=kind, policy=policy)


def build():
    entries = []
    entries.append(build_package('bf3-single-player', '1.0.0', 'Battlefield 3 · Single-player compatibility',
        'Battlefield 3 only. Disables optional pbcl/pbcl64 DLL loading for the existing single-player campaign. '
        'Does not replace EA/Steam authentication, unlock content, or provide multiplayer/offline emulation. '
        'Remove this profile before joining multiplayer servers that require PunkBuster.',
        'bf3.exe', 'profile', policy='bf3-single-player'))
    entries.append(build_package('mgs-ground-zeroes-startup', '1.0.0', 'Ground Zeroes · Startup compatibility',
        'Launch profile for MgsGroundZeroes.exe only. Enables image-page registration and the Wine tick thunk. '
        'Requires an Aura runtime containing the matching Wine/FEX support. This is a runtime-dependent profile, '
        'not a standalone game DLL or an FPS optimization. Removing the profile disables it next launch.',
        'MgsGroundZeroes.exe', 'profile', policy='mgs-startup'))
    entries.append(build_package('mirrors-edge-time', '1.0.0', 'Mirror’s Edge (2008) · Time conversion startup fix',
        'Exact-version executable patch routing the failing time conversion to the existing MSVCR80 implementation. '
        'Requires the original 60,167,392-byte EXE with SHA-256 84eea8fd3c4494d8ce3db8fc55b846f731425d6a2cd63da1189d641daf2929e4. '
        'Restore any legacy Aura startup patch before installation. Original EXE backed up locally.',
        'MirrorsEdge.exe', 'binary', binary=dict(bytes=60167392,
            before='84eea8fd3c4494d8ce3db8fc55b846f731425d6a2cd63da1189d641daf2929e4',
            after='5871a8af08e39fd7c35ba4ddd8c215355f91cf488835e4ee3de310e9645da4a5',
            edits=[dict(offset=0x020a31bd, before='8b44240453568b305733dbe8aac4ffff85f6', after='8b4424048338007c06ff259830b20231c0c3')])))
    entries.append(build_package('southpark-tfbw-low-va', '1.0.0', 'South Park: The Fractured But Whole · Address space compatibility',
        'Exact-version virtual-address allocation patch for SouthPark_TFBW.exe (223,530,184 bytes). '
        'Reduces virtual pool reservations, not physical RAM usage. Does not support The Stick of Truth. '
        'Restore any legacy Aura low-address patch first. Original EXE backed up locally.',
        'SouthPark_TFBW.exe', 'binary', binary=dict(bytes=223530184,
            before='0e1c90063627f8f01e83fa0be94f70d1d75e1af02572f0eef8d3b4bc5e4f5ae1',
            after='ae4f27a7b414fc620491eb8932167f88d1c88502c1c6108e40fea065bcd8814c',
            edits=[dict(offset=offset, before=before, after=after) for offset, before, after in
                   [(0x0abd64af,'40','10'), (0x0abd64cc,'c0','30'), (0x0abd64ed,'40','10'), (0x0abd6514,'40','10')]])))
    with zipfile.ZipFile(ROOT / 'upstream/MGSVFix_0.0.3.zip') as archive:
        files = {name: archive.read(name) for name in ['MGSVFix.asi', 'MGSVFix.ini', 'winmm.dll']}
    # Ship a widescreen-focused profile, preserving the original ZIP separately.
    for section in ['Intro Skip', 'Unlock Framerate']:
        files['MGSVFix.ini'], count = re.subn(rb'(\[' + section.encode() + rb'\][^\[]*?Enabled\s*=\s*)true',
                                             rb'\g<1>false', files['MGSVFix.ini'])
        assert count == 1
    for license in ROOT.joinpath('licenses').glob('*.txt'):
        if license.name in {'MGSVFix-MIT.txt','Ultimate-ASI-Loader.txt','safetyhook.txt','Zydis.txt','Zycore.txt','mINI.txt'}:
            files['AuraPatchLicenses/MGSVFix/' + license.name] = license.read_bytes()
    entries.append(build_package('mgs-ground-zeroes-widescreen', '0.0.3-aura1', 'Ground Zeroes · MGSVFix widescreen',
        'MGSVFix 0.0.3 by Lyall, with Ultimate ASI Loader. Installs beside MgsGroundZeroes.exe and adds a per-game '
        'winmm=n,b override. Fixes resolution, aspect ratio and HUD for the selected display ratio. '
        'Intro skipping and FPS unlocking default off in this package. Wine/ARM64EC phone behavior still requires testing.',
        'MgsGroundZeroes.exe', 'files', policy='winmm-native', files=files))
    with zipfile.ZipFile(ROOT / 'upstream/MirrorsEdgeTweaks_4.5.0-beta3.zip') as archive:
        exe = archive.read("Mirror's Edge Tweaks.exe")
    files = {"AuraPatchTools/MirrorsEdgeTweaks/Mirror's Edge Tweaks.exe": exe}
    for name in ['MirrorsEdgeTweaks-GPL-3.0.txt','MirrorsEdgeTweaks-THIRD-PARTY-NOTICES.md','NativeSharpLzo-GPL-3.0.txt','LZO-GPL-2.0.txt']:
        files['AuraPatchTools/MirrorsEdgeTweaks/' + name] = (ROOT/'licenses'/name).read_bytes()
    entries.append(build_package('mirrors-edge-widescreen-tool', '4.5.0-beta3', 'Mirror’s Edge · Widescreen repair tool',
        'Mirror’s Edge Tweaks 4.5.0-beta3 by softsoundd. Interactive Windows tool requiring .NET 10; '
        'downloading is not applying the widescreen fix. Follow README instructions to apply FOV/resolution changes. '
        'Aura only manages removal of this downloaded tool, not game changes made later by the tool. '
        'Original tool, matching source and license notices are included in the repository.',
        'MirrorsEdge.exe', 'tool', files=files))
    return json.dumps(dict(schema=1, patches=entries), ensure_ascii=False, indent=2).encode() + b'\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', required=True, type=Path, help='External private Ed25519 PEM; never commit this file')
    args = parser.parse_args()
    catalog = build()
    (ROOT/'catalog.json').write_bytes(catalog)
    with tempfile.TemporaryDirectory() as temporary:
        signature = Path(temporary)/'signature'
        subprocess.run(['openssl','pkeyutl','-sign','-inkey',str(args.key),'-rawin',
                        '-in',str(ROOT/'catalog.json'),'-out',str(signature)], check=True)
        (ROOT/'catalog.sig').write_bytes(base64.b64encode(signature.read_bytes()) + b'\n')
    subprocess.run(['openssl','pkey','-in',str(args.key),'-pubout','-out',str(ROOT/'catalog-public-key.pem')], check=True)
    sums = []
    for folder in ['packages','upstream','sources']:
        for file in sorted((ROOT/folder).rglob('*')):
            if file.is_file(): sums.append(SHA(file.read_bytes()) + '  ' + file.relative_to(ROOT).as_posix())
    (ROOT/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print('Built and signed', len(json.loads(catalog)['patches']), 'packages')


if __name__ == '__main__': main()
