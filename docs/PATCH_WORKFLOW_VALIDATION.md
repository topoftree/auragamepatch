# 补丁工作流检查

2026-10-23：新增 `aura-game-patch-release` skill 与声明式发布工具。现有七个正式包、catalog.json/catalog.sig 和 SHA256SUMS 原始字节均未改变；新 v2 目录通过原有 Ed25519 公钥验签，游戏分类索引与签名目录一致。

`python3 -m unittest discover -s tools/tests -v`：7 项测试通过，覆盖可重复打包、旧版本保留、同版本拒绝改写、签名和包篡改、路径／链接、缺少 App 接入证据、错误密钥和实验分类拒绝。测试只使用临时密钥与临时小字节夹具，没有把演示包发布到正式目录。

`python3 tools/patch_release.py check`：v1/v2 签名、全部目录包、保留的源码／上游归档校验和与分类索引通过。skill 在应用与补丁仓库中保持相同。

配套 App 的自动匹配、基线检查、手动选择优先、补丁安装／恢复、SMAPI 官方归档、导入／下载导航和双语资源共 80 项宿主检查通过，无失败或跳过；Debug Lint 0 错误、80 条警告，详细结果保留在应用仓库。本次没有新 APK，versionCode 至少 123 的后续 App 才能使用自动协议，现有七个包仍手动选择。手机上的网络流程、游戏效果与性能未额外验证。

配套已验证的本地源码提交：`29c60740de8ad08077bb464cc7b636e9e133b969`。这只是源码身份记录，不表示该 App 提交或 APK 已公开发布。

发布使用正常 fast-forward 推送，并按远端完整 commit URL 回读变更文件核验。重新检查可运行：

```bash
python3 tools/patch_release.py readback --commit 完整发布提交SHA
```
