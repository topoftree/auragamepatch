# 工作流和命令

先定位仓库，不依赖固定云路径：应用 remote 应为 `topoftree/winlator`，公开补丁 remote 应为 `topoftree/auragamepatch`。当前环境分别为 `/workspace/audit-winlator`、`/workspace/auragamepatch`；换环境后重新检查。Python 3.10+、OpenSSL（Ed25519）和 Git 必需，网络使用环境配置的代理和凭证。

## 仓库结构

```text
.agents/skills/aura-game-patch-release/  # 本 skill 的公开副本（不包含 App 源码）
recipes/<game>/<category>/<id>/<version>/recipe.json
recipes/<game>/<category>/<id>/<version>/payload/  # 可再分发输入
packages/<id>/<version>.zip             # 不可变安装包；保留旧版
games/index.json                        # 自动生成的游戏／分类索引
games/README.md                         # 自动生成的浏览目录
docs/<game>/                            # 使用方法和验证证据
licenses/                              # 原许可与第三方声明
sources/                               # 修改源码／必要对应源码
upstream/                              # 未改动的可再分发上游包
catalog-v2.json + catalog-v2.sig        # 新版 App 读取的签名目录
catalog.json + catalog.sig              # 旧版客户端保留
```

`tools/patch_release.py` 是发布工具，在公开仓库中维护。先运行 `check` 验证现有签名与所有包。新包通过 `add` 合并当前 v2 目录，不重建／丢弃别的游戏条目。相同版本不同字节会拒绝；更新增加版本并保留旧 ZIP。

## 配方

`recipe.json` 顶层：`schema: 1`、`entry`、可选 `binary`、`files`、`provenance`。`entry` 包含 `id/version/title/description/executables/kind/policy/game/category` 和可选 `autoInstall`；`path/bytes/sha256` 由工具生成。完整字段对应 App 的 Kotlin 数据类。

需要较新 App 的安装／启动能力时设置 entry 的 `minAppVersionCode`，旧客户端先按此字段隐藏不支持的条目，避免未知 policy 导致整个目录不可用。自动规则内的最低版本不得低于此值。新增协议字段形状仍需受控升级，不能只靠最低版本绕开严格解码器。

`files` 是 `[{"source":"payload/fix.dll","target":"fix.dll"}]`；source 必须在此配方目录内，target 相对真实启动 EXE 目录。`binary` 对应 App 的 `PackageBinaryPatch`：`bytes/before/after/edits`，每项 edit 为 `offset/before/after`。

`provenance` 包含：`upstream`（来源 HTTPS URL）、`license`（仓库内许可文件）、`validation`（仓库内验证文件）。自动安装的验证文件为 JSON，包含真实的 `installRestoreTested/versionMismatchTested/activationTested` 布尔结果和所测试 App 的完整 `appCommit`，并附测试命令、结果及手机是否验证等证据。不得只为通过校验填写 true。

自动规则形状（示意，不能将占位内容签入真实目录）：

```json
{
  "minAppVersionCode": 123,
  "executable": {"bytes": 12345, "sha256": "实际原始 EXE 的 64 位小写 SHA-256"},
  "targets": [
    {"path": "fix.dll", "before": null},
    {"path": "config.ini", "before": {"bytes": 456, "sha256": "实际原文件的 SHA-256"}}
  ]
}
```

binary/profile 的 targets 为空；binary 的 executable 基线须等于配方 before。files 的 targets 必须精确覆盖所有安装目标，包含许可文件等新增文件。已有未知文件或另一补丁占用目标时不自动覆盖。最低 123 是首次实现该协议的预留版本门槛；如实际能力在更晚版本交付，必须提高到实际 versionCode，不能只看版本名称。

## 命令

在补丁仓库根目录，替换变量为已核实路径，使用正常 shell 引号：

```bash
python3 tools/patch_release.py check
python3 tools/patch_release.py add \
  --recipe recipes/GAME/CATEGORY/PATCH/VERSION/recipe.json \
  --key /private/location/game-patch-catalogue-ed25519.pem
python3 -m unittest discover -s tools/tests -v
python3 tools/patch_release.py check
git diff --check
git diff --stat
python3 tools/patch_release.py publish --message "Add GAME compatibility repair VERSION"
```

当前私钥在应用仓库忽略的 `.signing/game-patch-catalogue-ed25519.pem`；此路径**不代表授权读取其他凭据或上传该文件**。密钥不可用时保留未发布成果，说明需要签名环境；不创建新密钥替换 App 信任根。

App 侧针对 `GamePatchAutomaticTest`、`GamePatchPackageTest`、`GamePatchLifecycleTest` 和新策略的启动测试执行项目 Gradle 检查。涉及 SMAPI 时使用已固定 SHA-256 的官方包完成现有集成测试。新能力要更新 App 白名单、工具白名单和测试，不能把单纯 package check 当作端到端验证。

发布工具拒绝未知远端、删除公开文件、改写已发布 ZIP、密钥/APK/mapping 等非补丁文件；只对正常 fast-forward 推送。发布后从固定远端 commit URL 回读变更文件并核验。失败若发生在 push 后，先检查远端头与文件，不重复制造同版本包。

push 成功但回读网络中断时，可使用 `python3 tools/patch_release.py readback --commit 完整提交SHA` 单独重试核验，不再推送或改写版本。

## 必须如实区分

1. 可重复打包、签名和校验通过。
2. App 安装、恢复、启动策略和负面用例通过。
3. 已发布并远端回读成功。
4. 配套 App 已生成 APK／已交付（本 skill 不自动授权此项）。
5. 用户手机真实游戏表现已验证。

安装或启动策略存在不代表游戏已进入主菜单、模组已加载或 FPS 已提高。
