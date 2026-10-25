# Mirror’s Edge（2008）19.5:9 直接安装补丁

在 **Game Management → Mirror’s Edge → Patch → Download patch** 选择 **Mirror’s Edge · 19.5:9 widescreen (direct install)**。最低 **Aura versionCode 137**；0.1.135（code 136）会隐藏此条目。不要在旧版 App 手动导入这个 schema 2 包。

此包是可直接应用的资源字节配方。原来的 **Mirror’s Edge Tweaks / Widescreen repair tool** 是交互工具，只下载不会应用宽屏，现已从新版 v2 下载目录撤下。新包不需要另开 Tweaks 或安装 .NET，也不自动执行任何脚本。

适用于 19.5:9，例如 **1560×720、2340×1080、3120×1440**。完全退出游戏后安装，游戏内选择对应分辨率及全屏，再重新启动。其他屏幕比例不要套用此包；这不是随意分辨率的动态修复。它不附加可调 FOV、HUD 或预录影片修复，不保证开场影片铺满屏幕。

## 实际修改

目标为 `Binaries/MirrorsEdge.exe` 所属游戏根目录内的 `TdGame/CookedPC/Engine.u`，只将一处小端 float `f38ee33f`（约 16:9）改为 `abaa0a40`（19.5:9）。不改 EXE，因此可以与 `mirrors-edge-time` 启动兼容补丁同时使用。

支持下表四个完整资源基线。安装会核对文件大小、完整修改前 SHA-256、编辑点旧字节及完整修改后 SHA-256。文件名相同不代表版本相同；其他发行版或已经被 Tweaks／模组改过的资源会拒绝安装并保留原文件。用户反馈新包已生效，但尚无该次资源哈希记录，不能据此确定具体命中了哪个基线或推广为所有版本支持。

| 基线 | 字节数 | 编辑偏移（十进制） |
| --- | ---: | ---: |
| Base，原 LZO 压缩包 | 1,662,824 | 645,379 |
| DLC，原 LZO 压缩包 | 1,669,463 | 646,328 |
| Base，解压后的 UE3 包 | 6,109,346 | 2,694,461 |
| DLC，解压后的 UE3 包 | 6,113,320 | 2,695,252 |

完整前后哈希位于 [声明式配方](../../recipes/mirrors-edge-2008/widescreen/mirrors-edge-widescreen-195/1.0.0/recipe.json)。压缩版编辑后仍成功解压，解压内容只改变相应的 4 字节；不需要在手机重压缩整个 UE3 资源。

## 恢复与验证

关闭恢复安装前的完整资源，重新启用使用 Aura 的本地保留副本；卸载恢复资源并保留补丁供离线重装；删除恢复后清除 Aura 的副本和收据。原资源备份只存在用户设备上。游戏更新、手动修改或后装补丁冲突时拒绝覆盖；中断沿用事务恢复流程。

启动诊断 `MIRRORS_EDGE_WIDESCREEN_V1 resource=BYTES_VERIFIED` 表示本次启动前重新核对了已安装文件的完整哈希。`MISMATCH` 表示文件与安装记录不同。两者都不代替游戏画面验证，`game_effect=UNCONFIRMED` 保持明确。

实物资源校验、App 安装／恢复及负面用例见 [初次验证记录](widescreen-195-validation.json)。**2026-10-25 用户反馈安装新包后已实现宽屏**；这是该用户设备的使用反馈，不是维护环境完成的手机测试，也不证明所有设备、比例或预录影片均适用。

旧工具从下载列表撤下不会移除设备上的已安装记录、工具文件或恢复备份。新包与旧工具不互相依赖；若旧工具仅下载而未另行运行，可从旧条目卸载／删除工具文件。若曾通过 Tweaks 修改游戏，Aura 的工具下载回滚不包含它后来自行做的修改，应遵循工具自身的恢复记录。仓库保留旧 ZIP、源码和许可供历史核验。

## 来源与复现

- 已知修复方法：[WSGF Mirror’s Edge](https://www.wsgf.org/dr/mirrors-edge)。
- 校验参考资源：[上游 Tweaks runtime-assets](https://github.com/softsoundd/MirrorsEdgeTweaks/releases/tag/runtime-assets) 的 `Base_Engine.zip`、`DLC_Engine.zip`。资源仅在本地分析，仓库／补丁不含完整或裁切游戏资源。
- UE3 分块布局与上游 `DecompressionService.cs` 交叉核对；对应固定源码已保留于 `sources/MirrorsEdgeTweaks-4.5.0-beta3.tar.gz`，上游 GPL 文本在 `licenses/`。新配方和独立 Python 校验器按仓库 MIT 许可提供，不重打包上游工具或原生解压 DLL。
- 外部参考 ZIP 完整哈希固定在 `tools/verify_mirrors_edge_widescreen.py`。在独立 Python 环境安装 `lzokay==2.1.0` 后，运行 `python3 tools/verify_mirrors_edge_widescreen.py --reference-dir /path/to/reference-zips`，会验证两份压缩资源和对应解压资源的全部前后哈希、解压完整性及精确四字节差分。校验器不下载文件、不执行游戏或下载的程序。
