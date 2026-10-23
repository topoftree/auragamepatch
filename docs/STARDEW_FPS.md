# StardewFPS：实验性帧率解锁

这是 Lake1059 的 **StardewFPS 1.0** 模组，用于改变 Stardew Valley 的目标更新频率。**不是性能优化补丁，也不是保持原游戏速度的高帧率补丁。** 原生分辨率下每帧处理超过 16.67 ms 的问题不会因为解除 60 FPS 上限而消失。

## 重要限制

- 作者明确说明动画帧速度、敌人速度会随设置的帧率改变，建议不要用于正常游玩。先备份存档，避免用主存档进行实验；删除模组不能撤销已经保存的游戏进度。
- 上游发布于 2024-03-22，页面标记兼容游戏 1.6；更新的游戏或 SMAPI 版本，以及 Aura 的 Wine/ARM64EC 手机环境，尚未验证。
- 必须安装适配游戏版本的 **Windows 版 SMAPI**，并通过 `StardewModdingAPI.exe` 启动。只启动原游戏 EXE 不会加载此模组。
- 本 ZIP 只包含模组，不附带 SMAPI；带依赖管理的 Aura 会在用户安装／启用此模组时补齐固定官方 SMAPI，并在 SMAPI 启用时选择其启动入口。手动解压 ZIP 不会安装依赖。不修改游戏 EXE、不自动执行命令、不自动修改帧率和 VSync。
- 主菜单仍为 60 FPS；每次启动需要重新输入命令。提高目标帧率不保证设备能够达到该帧率。

## 安装及使用

1. 完全退出游戏。Aura 0.1.125 中进入 **Stardew Valley 的 Game Management → Mod → Download mod**，选择 **Experimental FPS unlock (SMAPI)** 下载并安装。它属于模组，不在新版的 Download patch 列表。目录按真实启动 EXE 匹配，支持 `Stardew Valley.exe` 和 `StardewModdingAPI.exe`。
2. Aura 将文件安装到游戏 EXE 同目录的 `Mods/StardewFPS/`，并在需要时补齐固定官方 Windows SMAPI。当前内置依赖为 SMAPI 4.5.2，要求 Stardew Valley 1.6.14+；不适配的游戏不能强行安装。依赖下载失败可重试，或在 Import mod 选择同一受支持版本的官方安装 ZIP。SMAPI 和 StardewFPS 的已安装记录位于 Mod 页面 Download mod 下方。
3. 确认 SMAPI 与模组均启用，正常点击 Aura 的 Start game；启用的 SMAPI 会使 Aura 改用 `StardewModdingAPI.exe`。确认控制台实际报告模组加载成功；诊断中的 `selected=SMAPI` 也只证明选择了入口。旧版没有依赖管理或自行解压安装者，应先按 [SMAPI 官方说明](https://smapi.io/) 安装适配游戏的 Windows 版本，再放入仓库原始模组 `upstream/StardewFPS.1.0.0.zip` 中的 `StardewFPS` 文件夹。
4. 关闭游戏内 VSync，加载存档，然后在 **SMAPI 控制台**输入 `fps 120`。不是 Wine CMD、游戏聊天框或 Android terminal。只输入正整数；上游模组没有完整的参数校验。建议先测试 `fps 60`，再尝试 90 或 120。主菜单仍为 60 FPS，每次启动需重新执行命令。
5. 停用时先完全退出游戏，在 Mod 页面打开已安装的 StardewFPS，选择关闭，再重新启动。卸载会恢复原文件并保留本机模组副本，删除还会清除该副本；停用不要求删除文件。若还要关闭 SMAPI，先关闭所有依赖它的模组。手动安装者自行移除 `Mods/StardewFPS`。`fps 60` 可以恢复该次会话的目标频率，但完整恢复默认计时应关闭模组后重启。

旧版没有独立 Mod 页时，本包在 Patch → Download patch。已发布 ZIP 内附带的旧版说明保留原样，当前页面的入口与依赖说明适用于新版 Aura；不改写既有安装包。

Aura 的安装记录仅表示文件已复制；不表示 SMAPI 依赖齐全、模组已加载或高帧率已生效。通过 Aura 安装时，被覆盖的旧模组文件会在手机本地备份，删除补丁时按安装记录恢复。手动安装不享有 Aura 的自动回滚。

## 来源与许可

- 作者：[Lake1059](https://github.com/Lake1059)
- [GitHub 1.0 Release](https://github.com/Lake1059/StardewFPS/releases/tag/1.0)，原始二进制 ZIP 保持不变。
- [对应源码](https://github.com/Lake1059/StardewFPS/tree/a3bf5bdd1f45fadcec0e7d0fa5b84b8b4b0ade12)，提交 `a3bf5bdd1f45fadcec0e7d0fa5b84b8b4b0ade12`，完整归档见仓库 `sources/StardewFPS-1.0.tar.gz`。
- 按上述 GitHub 版本自带的 MIT LICENSE.txt 再分发，全文原样保留，包括上游未填写的 `[year] [fullname]` 占位符；不自行改写作者版权声明。作者归属在此明确保留。本包取自 GitHub，不镜像 Nexus 下载文件。
- [作者说明与限制](https://www.nexusmods.com/stardewvalley/mods/20801)。代码仅设置 `TargetElapsedTime = 1 / fps` 和 `IsFixedTimeStep = True`，没有将动画/敌人更新与显示频率解耦。

本包没有修改上游 DLL 或 manifest；只额外附带本说明及 MIT 许可。原始 ZIP、源码及 Aura 安装包的 SHA-256 见仓库根目录 `SHA256SUMS`。
