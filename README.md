# 鸿蒙 UDID 获取工具 · HarmonyOS UDID Picker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://github.com/MySwallow/harmony-udid/actions/workflows/build.yml/badge.svg)](https://github.com/MySwallow/harmony-udid/actions)
[![Latest Release](https://img.shields.io/github/v/release/MySwallow/harmony-udid)](https://github.com/MySwallow/harmony-udid/releases/latest)

给**非开发人员**用的小工具：双击运行 → 手机用 USB 接上 → 点按钮 → 设备 UDID 自动复制到剪贴板。

## 解决了什么问题

HarmonyOS NEXT 上获取设备 UDID（用于内部测试 Profile 注册），**官方唯一途径**是命令行 `hdc shell bm get --udid`。这对测试 / 验收人员门槛太高——他们不一定有 DevEco Studio、不一定会用命令行。

本工具把 `hdc` 包了一层 GUI，配合自动嵌入的 `hdc` + `libusb_shared` 实现真正的"双击即用"，全程 < 30 秒。

> 注意：HarmonyOS NEXT 的 `deviceInfo.udid` API 受系统级权限 `ohos.permission.sec.ACCESS_UDID` 保护，三方应用**无法直接读取**——所以"装个 APP 显示 UDID"这条路走不通。本工具的本质仍然是调用 hdc，只是把流程做傻瓜化。

## 下载

到 [Releases 页面](https://github.com/MySwallow/harmony-udid/releases/latest) 选对应平台：

| 平台 | 文件 |
|---|---|
| Windows x64 | `HarmonyUDID-windows.exe` |
| macOS (Intel + Apple Silicon, Universal) | `HarmonyUDID-macos-universal.zip` |

macOS 一份通用 .app，**自动适配 Intel 和 Apple Silicon Mac**，不用区分。

## 使用步骤

### Windows
1. 双击 `HarmonyUDID-windows.exe`
2. SmartScreen 警告：**更多信息 → 仍要运行**
3. 手机 USB 接电脑
4. 手机开「开发者模式 + USB 调试」：
   - 设置 → 关于本机 → 连点 HarmonyOS 版本 5–7 次
   - 设置 → 系统 → 开发人员选项 → 「USB 调试」打开
5. 手机弹窗「允许 USB 调试？」点 **允许**
6. 工具里点「**获取 UDID**」→ UDID 自动复制到剪贴板
7. 粘贴回传给开发者

### macOS
1. 下载 `HarmonyUDID-macos-universal.zip`，双击解压
2. 第一次右键 `HarmonyUDID.app` → 打开（绕过 Gatekeeper 警告）
3. 如果系统弹"已损坏，无法打开"，二选一：
   - **图形界面（推荐给非技术用户）**：系统设置 → 隐私与安全性 → 滑到底部找到「HarmonyUDID 已被阻止」→ 点 **「仍要打开」** → 输入密码确认
   - **命令行（一行根除）**：终端执行 `xattr -dr com.apple.quarantine /path/to/HarmonyUDID.app`
4. 其余步骤同 Windows

> **注意**：如果你已经装了 DevEco Studio 并打开过，请先**完全退出** DevEco Studio，再用本工具，避免两个 hdc daemon 冲突。

## 工程结构

```
harmony-udid/
├── main.py                       # GUI 主程序（Python + Tkinter，跨平台）
├── .github/workflows/build.yml   # GitHub Actions matrix: Win + macOS Universal
├── LICENSE                       # MIT
└── README.md
```

`hdc` / `libusb_shared` 二进制不在仓库——CI 时由 [openharmony-rs/setup-ohos-sdk](https://github.com/openharmony-rs/setup-ohos-sdk) 与 [openharmony-rs/ohos-sdk](https://github.com/openharmony-rs/ohos-sdk) 自动拉取 OpenHarmony 5.0.0 SDK，提取 hdc + libusb 后随 PyInstaller 一起打包。

## 本地调试

```bash
git clone https://github.com/MySwallow/harmony-udid.git
cd harmony-udid

# Mac 上：从 DevEco Studio 拷一个 hdc 到当前目录
# 路径示例：~/Library/Huawei/Sdk/<version>/openharmony/toolchains/hdc
#         或 /Applications/DevEco-Studio.app/Contents/sdk/.../toolchains/hdc

python3 main.py
```

## 自己构建

任何人 Fork 后都能在自己的仓库下构建：

```bash
# 改完代码自动打三个平台
git push

# 或手动触发
gh workflow run build.yml

# 发版本到 Releases
git tag v1.0.0 -m "..." && git push --tags
```

## 隐私 & 安全

- 工具只调用本地 hdc，**不联网**，不上传任何信息
- 源码全部在本仓库，可自行审计
- 内嵌的 hdc / libusb_shared 来自 OpenHarmony 公开 SDK（Apache 2.0），未经过任何修改

## 致谢

- [OpenHarmony](https://www.openharmony.cn/) — 开源 SDK + hdc 工具
- [openharmony-rs/ohos-sdk](https://github.com/openharmony-rs/ohos-sdk) — GitHub Release 镜像
- [iHongRen/harmony-udid-tool](https://github.com/iHongRen/harmony-udid-tool) — 思路参考（macOS only）

## License

[MIT](LICENSE) © 2026 MySwallow
