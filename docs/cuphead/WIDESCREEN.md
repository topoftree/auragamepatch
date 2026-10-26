# Cuphead 宽屏候选与原始下载入口

状态：**外部来源索引，未镜像安装包，未加入 Aura 的签名下载目录。** 此页面不表示已在 Aura 或手机上验证宽屏效果。

## Cuphead UltraWide

- 作者：[opaaaaaaaaaaaa 的 Cuphead UltraWide](https://www.nexusmods.com/cuphead/mods/122)。
- [原始文件页](https://www.nexusmods.com/cuphead/mods/122?tab=files)：模组 1.1.0，2026-07-17，页面标注 4 KB。
- [作者 GitHub 发布页](https://github.com/gabrielsitta4/game-mods/releases/tag/Cuphead-CupheadUltraWideBepInEx-v1.1.0)也提供同版本 ZIP，并反向链接至 Nexus 122；作者仓库 README 链接同一 Nexus 账号及模组。可从原发布页下载，无需在本仓库镜像。
- 作者说明：BepInEx／Harmony 相机补丁，自动按显示比例调整，限制在 16:9～2.39:1；扩大可见场景，Overscan 强制为 0。部分脚本场景可能露出背景边缘。
- 插件目标：`BepInEx/plugins/CupheadUltraWideBepInEx.dll`。1.1.0 是模组版本，不能据此推断匹配的游戏版本。

依赖页面：[BepInEx for Cuphead](https://www.nexusmods.com/cuphead/mods/173)。作者描述其为官方 BepInEx 5.4.23.5 **x64** 包；实际使用前必须核实 Cuphead.exe 的架构，不能给 x86 游戏套 x64 加载器。

作者的 Wine／Proton 指引要求 `winhttp=n,b`；这是需要在 Aura 中单独核实的加载条件，不是已经实现的 Aura 自动启动策略。插件是否加载应检查 `BepInEx/LogOutput.log` 及相机补丁记录。页面没有提供精确游戏构建／托管程序集哈希和完整 DLC 适配表，因此不能把复制文件成功当作宽屏已生效。

## 当前只提供来源链接

2026-10-26 核对作者页，其上传许可写明：

> You are not allowed to upload this file to other sites under any circumstances.

修改许可也要求先取得作者许可。尚未提供可覆盖本仓库发布的授权，因此不镜像 DLL／ZIP，不伪造下载条目，不发布修改后的商业游戏程序集。该限制不代表官方开源 BepInEx 本身的许可；若后续使用加载器，另核对其上游许可证和对应源码义务。

已只读检查作者 GitHub 的 `CupheadUltraWideBepInEx-1.1.0.zip`：4960 字节，SHA-256 `c21604053f8e09017c1526d24186d87fbcf3d47883b48ec0b5aa53cdd08acb8e`，仅有插件 DLL（10240 字节）和父目录，没有附带源码或许可证。此检查不执行 DLL，也不建立再分发授权或手机兼容性证明。

取得可再分发授权与合法安装包后，仍需核对目标游戏基线、加载器架构、已有 DLL 覆盖关系，并完成 Aura 的下载、启用、关闭、卸载和冲突恢复测试，再将真实包加入签名目录。宽屏保持手动选择，不能自动改变游戏文件。

## 旧方案

[Mod fix ultra-wide screen](https://www.nexusmods.com/cuphead/mods/90) 直接替换 `Cuphead_Data/Managed/Assembly-CSharp.dll`，作者明确说明只能部分去黑边，Boss 和训练关仍受 16:9 资源限制。旧 [WSGF 修复](https://www.wsgf.org/phpBB3/viewtopic.php?f=64&t=32324) 面向 1.00／1.1.3／1.1.4，不作为当前游戏版本兼容证明。

宽屏与原厂驱动的暗画面属于不同问题；这个候选不承诺解决颜色、闪烁或性能问题。
