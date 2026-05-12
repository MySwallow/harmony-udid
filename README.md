# 鸿蒙 UDID 获取工具

给**非开发人员**用的小工具：双击运行 → 手机 USB 接上 → 点按钮 → 设备 UDID 自动复制到剪贴板，直接粘贴回传给开发者。

> 解决场景：HarmonyOS NEXT 设备 UDID 必须通过 hdc 命令行获取，普通测试人员上手成本高。这个工具把 `hdc shell bm get --udid` 包了一层 GUI，配合内置 hdc 二进制实现真正"双击即用"。

## 支持平台

| 平台 | 产物 | 文件名 |
|---|---|---|
| Windows x64 | `.exe` | `HarmonyUDID-windows.exe` |
| macOS Universal (Intel + Apple Silicon) | `.app`（zip 打包） | `HarmonyUDID-macos-universal.zip` |

> 两个 job 并行构建。macOS 用 Universal2 binary — 一个 `.app` 同时兼容 Intel + Apple Silicon Mac。
> 不依赖 `macos-13` runner（GitHub 的 Intel runner 排队严重），全程在 `macos-latest` 上完成。

## 下载

### 方式 A：仓库 Actions 页面（仅协作者可见）
仓库主页 → **Actions** → 最新一次 `Build Multi-Platform` → 底部 `Artifacts` 区下载对应平台 zip。

### 方式 B：GitHub Release（推荐发给测试方）
```bash
# 在 Mac 上
cd ~/Documents/dev/udid-picker
git tag v1.0.0 -m "首版"
git push --tags
```
完成后到 https://github.com/MySwallow/udid-picker/releases/latest 下载，**测试方不需要 GitHub 账号**。

### 方式 C：CLI 一键下载
```bash
# Windows 版
gh run download --repo MySwallow/udid-picker --name HarmonyUDID-windows --dir ~/Downloads/

# macOS Universal 版（兼容 Intel + Apple Silicon）
gh run download --repo MySwallow/udid-picker --name HarmonyUDID-macos-universal --dir ~/Downloads/
```

## 测试方使用步骤

### Windows
1. 下载 `HarmonyUDID-windows.exe`，双击打开
2. SmartScreen 拦截时：**更多信息 → 仍要运行**
3. 手机 USB 连电脑 + 开启 USB 调试
4. 工具里点「获取 UDID」→ 自动复制到剪贴板
5. 粘贴回传给开发者

### macOS
1. 下载 `HarmonyUDID-macos-universal.zip`（一份通用包，自动适配 Intel + Apple Silicon）
2. 双击解压得到 `HarmonyUDID.app`
3. 第一次右键 → 打开（绕过 Gatekeeper 警告）
   - 如果报"应用已损坏"：终端执行 `xattr -dr com.apple.quarantine /path/to/HarmonyUDID.app`
4. 后续步骤同 Windows

## 工程结构

```
udid-picker/
├── main.py                       # GUI 主程序（跨平台 Python + Tkinter）
├── .github/workflows/build.yml   # GitHub Actions matrix: Win / Intel Mac / ARM Mac
├── .gitignore
└── README.md
```

`hdc` / `hdc.exe` 不放仓库——workflow 跑的时候用 `openharmony-rs/setup-ohos-sdk` 自动拉对应平台的 OpenHarmony SDK，提取出 hdc 后内嵌进打包产物。

## 本地调试

```bash
# Mac 用户从 DevEco Studio 拷一个 hdc
cp /Applications/DevEco-Studio.app/Contents/sdk/HarmonyOS-NEXT-DBn/openharmony/toolchains/hdc .
python3 main.py
```

## 触发打包

| 想做的事 | 命令 |
|---|---|
| 改完代码自动打 | `git push` |
| 不改代码重打 | `gh workflow run build.yml --repo MySwallow/udid-picker` |
| 打稳定版本发给测试方 | `git tag v1.0.0 && git push --tags` |
| 看进度 | `gh run watch --repo MySwallow/udid-picker` |

## 隐私

工具只调用本地 hdc，不联网，不上传任何信息。
