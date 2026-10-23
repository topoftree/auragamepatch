# Aura patch repository agreements

- 本仓库是用户授权公开的 `topoftree/auragamepatch`，不包含独立 Aura 应用源码或完整商业游戏文件。
- 用户 2026-10-23 持续授权：新增游戏专用兼容／修复补丁后自动打包、分类、验证并上传，同时完成对应 App 的下载、安装、启用和恢复接入。此授权不含 APK 或其他仓库的发布。
- 相关任务必须先读 [.agents/skills/aura-game-patch-release/SKILL.md](.agents/skills/aura-game-patch-release/SKILL.md)，并核对 App 仓库的规则和实际协议。
- `packages/<id>/<version>.zip` 发布后不可改写／删除。新版本增加版本号，旧备份必须能恢复。
- 新包用 `tools/patch_release.py add/check/publish`。保留严格 v1 客户端的 catalog.json/catalog.sig；分类／自动策略用独立签名 v2 目录。
- 签名私钥必须在本仓库外；不得发布凭证、用户诊断、完整游戏 EXE／资源、私有 App 源码或混淆映射。保留上游来源、许可与对应源码。
- 自动安装只允许精确版本匹配的兼容／错误修复，不重新安装用户关闭、卸载或删除的补丁；工具、FPS 模组、宽屏和 BF3 单人模式仍手动选择。
- 发布先验证真实 App 接入、回滚与失败路径，再提交并正常推送；远端按 commit 回读核验。不强推、不将未验证的手机效果写成已验证。
- 此 skill 的副本同时在 Aura 私有源码仓库 `.agents/skills/aura-game-patch-release/`；修改共享流程时保持两份相同。
