# StardewFPS：实验性帧率解锁

这是 Lake1059 的 **StardewFPS 1.0** 模组，用于改变 Stardew Valley 的目标更新频率。**不是性能优化补丁，也不是保持原游戏速度的高帧率补丁。** 原生分辨率下每帧处理超过 16.67 ms 的问题不会因为解除 60 FPS 上限而消失。

## 重要限制

- 作者明确说明动画帧速度、敌人速度会随设置的帧率改变，建议不要用于正常游玩。先备份存档，避免用主存档进行实验；删除模组不能撤销已经保存的游戏进度。
- 上游发布于 2024-03-22，页面标记兼容游戏 1.6；更新的游戏或 SMAPI 版本，以及 Aura 的 Wine/ARM64EC 手机环境，尚未验证。
- 必须安装适配游戏版本的 **Windows 版 SMAPI**，并通过 `StardewModdingAPI.exe` 启动。只启动原游戏 EXE 不会加载此模组。
- 本包只安装模组，不附带或自动安装 SMAPI，不修改游戏 EXE、不自动执行命令、不自动修改帧率和 VSync。
- 主菜单仍为 60 FPS；每次启动需要重新输入命令。提高目标帧率不保证设备能够达到该帧率。

## 安装及使用

1. 从 [SMAPI 官网](https://smapi.io/) 获取适配当前游戏版本的 Windows 安装包，按官方说明安装到自己的游戏目录。安装成功后确认 `StardewModdingAPI.exe` 能正常运行并显示控制台。此依赖在 Aura 手机上未经验证；如果 SMAPI 不能运行，本模组也不能使用。
2. 新版 Aura 的 `Game Management → 当前游戏 → Patch → Download patch` 提供本包。选择 **Experimental FPS unlock (SMAPI)** 下载并安装，文件会放到游戏 EXE 同目录下的 `Mods/StardewFPS/`。
3. 当前公开 Aura 0.1.118 没有新版下载入口。也可将仓库 `upstream/StardewFPS.1.0.0.zip` 解压，把 `StardewFPS` 文件夹放进游戏的 `Mods` 文件夹；附带的许可证位于仓库 `licenses/StardewFPS-MIT.txt`。
4. 通过 `StardewModdingAPI.exe` 启动游戏，关闭游戏内 VSync，加载存档，然后在 **SMAPI 控制台**输入 `fps 120`。不是 Wine CMD、游戏聊天框或 Android terminal。只输入正整数；上游模组没有完整的参数校验。建议先测试 `fps 60`，再尝试 90 或 120。
5. 完全退出游戏后，在 Aura 删除此补丁并恢复原文件，再重启游戏即可停用。手动安装者删除自己放入的 `Mods/StardewFPS` 文件夹。`fps 60` 可以恢复该次会话的目标频率，但完整恢复默认计时以移除模组后重启为准。

Aura 的安装记录仅表示文件已复制；不表示 SMAPI 依赖齐全、模组已加载或高帧率已生效。通过 Aura 安装时，被覆盖的旧模组文件会在手机本地备份，删除补丁时按安装记录恢复。手动安装不享有 Aura 的自动回滚。

## 来源与许可

- 作者：[Lake1059](https://github.com/Lake1059)
- [GitHub 1.0 Release](https://github.com/Lake1059/StardewFPS/releases/tag/1.0)，原始二进制 ZIP 保持不变。
- [对应源码](https://github.com/Lake1059/StardewFPS/tree/a3bf5bdd1f45fadcec0e7d0fa5b84b8b4b0ade12)，提交 `a3bf5bdd1f45fadcec0e7d0fa5b84b8b4b0ade12`，完整归档见仓库 `sources/StardewFPS-1.0.tar.gz`。
- 按上述 GitHub 版本自带的 MIT LICENSE.txt 再分发，全文原样保留，包括上游未填写的 `[year] [fullname]` 占位符；不自行改写作者版权声明。作者归属在此明确保留。本包取自 GitHub，不镜像 Nexus 下载文件。
- [作者说明与限制](https://www.nexusmods.com/stardewvalley/mods/20801)。代码仅设置 `TargetElapsedTime = 1 / fps` 和 `IsFixedTimeStep = True`，没有将动画/敌人更新与显示频率解耦。

本包没有修改上游 DLL 或 manifest；只额外附带本说明及 MIT 许可。原始 ZIP、源码及 Aura 安装包的 SHA-256 见仓库根目录 `SHA256SUMS`。
