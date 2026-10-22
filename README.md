# Aura Game Patches

Aura 的游戏专用兼容补丁和宽屏工具仓库。应用按实际启动 EXE 匹配补丁；Steam 游戏和 Local 游戏均可使用。这里不包含完整游戏文件、游戏凭证或用户诊断。

## 补丁列表

| 游戏 | 补丁 | 安装方式 | 恢复方式 |
| --- | --- | --- | --- |
| Battlefield 3 | 单人兼容 | 下载启动配置，只对 `bf3.exe` 禁用可选 `pbcl` / `pbcl64` 加载 | 删除配置，下次启动恢复原行为 |
| Metal Gear Solid V: Ground Zeroes | 启动兼容 | 下载配置，启用配套 Wine/FEX 的 image-page 与 tick-thunk 支持 | 删除配置，下次启动停用 |
| Mirror’s Edge（2008） | 时间转换启动修复 | 校验完整 EXE 哈希后应用少量字节修改 | 使用本机原文件备份恢复 |
| South Park: The Fractured But Whole | 虚拟地址分配兼容 | 校验完整 EXE 哈希后修改分配参数 | 使用本机原文件备份恢复 |
| Ground Zeroes | MGSVFix 0.0.3 宽屏 | 自动安装 ASI / DLL / INI，并设置此游戏的 `winmm=n,b` | 删除新增文件、恢复原文件并取消该启动覆盖 |
| Mirror’s Edge（2008） | Mirror’s Edge Tweaks 4.5.0-beta3 | **交互式工具下载，需要另行运行；下载不代表已应用宽屏** | Aura 管理工具文件；工具后来修改的游戏文件由工具自身的备份/恢复功能管理 |
| Stardew Valley | StardewFPS 1.0 实验性解锁 | **依赖 SMAPI；改变动画和敌人速度，不建议正常游玩** | 删除模组、恢复旧文件后重启；不撤销存档进度 |

战地 3 的单人兼容不作为通用开关，不替代 EA / Steam 登录或授权，不提供联机模拟，也不把游戏变成不需要客户端的离线版。联机前请移除该配置。

Ground Zeroes 启动包是**依赖运行时能力的配置补丁**，不是可直接放入任意模拟器的独立 DLL。Wine/FEX 的配套机制仍需由 Aura 运行时提供；此仓库保存开关配置与相应源码改动。基础通用 Wine / DXVK 修复继续随应用运行时提供。

## 在 Aura 中使用

需要带新版 Patch 页面的 Aura；当前公开 0.1.118 不会自动识别本目录。进入：

`Settings → Game Management → 当前游戏 → Patch → Download patch`

选中补丁后查看说明，再选择「下载并安装」。安装前关闭游戏。已安装记录支持离线查看；选择「删除补丁并恢复原文件」撤销。`Import patch` 继续支持用户自己的已解压文件/文件夹。

游戏专用的 EXE 补丁采用完整文件大小、原 SHA-256、逐字节原值与修改后 SHA-256 校验；其他版本会拒绝安装，不能靠重命名文件强行适配。请先恢复旧版 Aura 专用兼容，再安装同一修复的新包。旧版已应用的修改和本地备份保留供恢复。

### 本地备份

文件补丁安装前，Aura 将所有被覆盖文件备份到设备内应用私有目录 `game-patches/<游戏ID>/<安装批次>/old/`，备份不上传到本仓库。完成备份后才替换文件；安装/恢复中断会保留日志并阻止游戏在半完成状态启动。

卸载时新增文件会删除，覆盖文件会从备份恢复。多个补丁覆盖同一文件时，先卸载后装的补丁。游戏更新或用户修改后，Aura 会拒绝覆盖与记录不符的文件。清除 Aura 数据或卸载 Aura 会丢失这些本地备份。配置包不修改游戏文件，删除其安装记录即取消下次启动的专用配置。

## Stardew Valley 帧率实验

已提供 [StardewFPS 使用说明](docs/STARDEW_FPS.md)、原始模组、对应源码和 MIT 许可。需要通过 Windows 版 SMAPI 启动，在加载存档后关闭游戏 VSync，并在 SMAPI 控制台输入 `fps 120`。本包不会自动安装 SMAPI，也不会自动解锁帧率；它会改变动画和敌人速度，不能解决当前低于 60 FPS 的渲染开销。手机 Wine/ARM64EC 兼容性尚未验证。

## 两个宽屏资源

原始包保持上游字节不变，位于 [upstream](upstream)。签名目录使用的 Aura 安装包位于 [packages](packages)。

### Ground Zeroes / MGSVFix

- 作者：[Lyall](https://codeberg.org/Lyall/MGSVFix)，原版 [0.0.3](https://codeberg.org/Lyall/MGSVFix/releases/tag/0.0.3)，MIT。
- 自动包安装到 `MgsGroundZeroes.exe` 同目录；按游戏添加 Wine 原生 `winmm` 优先加载，不修改共享容器设置。
- 原版附带的「跳过片头」「解锁帧率」在 Aura 自动包中默认关闭。分辨率、长宽比与 HUD 修复保持开启。原始 ZIP 没有改动。
- 跟随游戏所选分辨率，不把 S24 Ultra 的 13:6 强行当成 21:9。可选 3120×1440、2340×1080、1560×720；具体上限取决于当前容器。
- 尚未在目标手机上验证 Wine/ARM64EC 下的 ASI 加载与画面效果；安装成功不等于真机兼容已确认。

### Mirror’s Edge Tweaks

- 作者：[softsoundd](https://github.com/softsoundd/MirrorsEdgeTweaks)，原版 [4.5.0-beta3](https://github.com/softsoundd/MirrorsEdgeTweaks/releases/tag/4.5.0-beta3)，GPL-3.0；对应源码随仓库提供。
- 包内是 `Mirror's Edge Tweaks.exe`，需要 Windows .NET 10 桌面运行时。它不是放进游戏目录就生效的 ASI 补丁，也没有已核实的无人值守安装接口。
- Aura 将工具放到游戏 EXE 旁的 `AuraPatchTools/MirrorsEdgeTweaks/`。请在能运行该工具的 Windows/Wine 环境中选择游戏目录并应用 FOV 修复和所需分辨率。
- 工具会修改 Unreal 包及配置等文件。**Aura 的工具下载回滚不涵盖工具以后自行产生的修改**；运行前保留游戏文件/配置副本，并遵循工具自身的恢复说明。不能把工具下载按钮当成自动宽屏安装按钮。
- 此版本的 .NET 10 WPF 界面在手机 Wine/ARM64EC 下未经实测；必要时在 PC 处理自己的游戏副本，再用 Aura 的 Import patch 导入处理后的文件，获得 Aura 的文件级备份恢复。

## 目录、校验与维护

- [catalog.json](catalog.json)：版本 1 目录，按 EXE 匹配，列出每个安装包的大小和 SHA-256。
- [catalog.sig](catalog.sig)、[catalog-public-key.pem](catalog-public-key.pem)：Ed25519 分离签名与公钥。签名私钥不在公开仓库，也不是 APK 签名密钥。
- [SHA256SUMS](SHA256SUMS)：安装包、上游原始包及源码归档的校验值。
- [sources](sources)：上游源码归档及 Ground Zeroes 运行时改动。
- [licenses](licenses)：各作者许可证与第三方声明。
- [tools/build_catalog.py](tools/build_catalog.py)：确定性安装包生成器。构建时显式传入仓库外的签名私钥：`python3 tools/build_catalog.py --key /private/path/catalogue.pem`。

安装包只允许有界的文件复制、精确字节修改和已支持的启动配置，不执行包内脚本。不要替换已经发布的版本目录；更新请增加版本号、重新构建并签名。新的原生代码类型或运行时能力需要相应应用版本支持。

## 来源和许可证

Aura 自有目录、补丁定义和打包脚本按 [MIT](LICENSE) 提供；第三方作品保留原许可证。MGSVFix、Ultimate ASI Loader、safetyhook、Zydis/Zycore、mINI、StardewFPS 的声明位于 `licenses`。Mirror’s Edge Tweaks 及 NativeSharpLzo 的对应版本源码、GPL 文本与第三方声明均附带；构建依赖版本见原源码项目文件。

Game-specific executable packages contain only small modification recipes, not complete proprietary executables. Names and trademarks belong to their respective owners. No gameplay performance gain or target-device compatibility is claimed without device testing.
