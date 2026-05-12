# 鸿蒙 UDID 获取工具

给**非开发人员**用的小工具：双击运行 → 手机用 USB 接上 → 点按钮 → 设备 UDID 自动复制到剪贴板，直接粘贴回传给开发者。

> 解决场景：HarmonyOS NEXT 设备 UDID 必须通过 hdc 命令行获取，普通测试人员上手成本高。这个工具把 `hdc shell bm get --udid` 包了一层 GUI，配合内置的 `hdc.exe` 实现真正"双击即用"。

## 下载

最新的 Windows .exe：
- 仓库主页 → **Actions** → 最新一次 `Build Windows EXE` 运行 → 滑到底部 `Artifacts` → 下载 `HarmonyUDID-windows.zip`
- 或者推一个 `v*` 标签后到 **Releases** 页面下载（自动发布）

解压后得到 `HarmonyUDID.exe`，可改名为「鸿蒙UDID获取工具.exe」再发给测试方。

## 测试方使用步骤

1. 双击 `HarmonyUDID.exe`
2. 第一次 Windows SmartScreen 会拦：**更多信息 → 仍要运行**
3. 手机用数据线连电脑
4. 手机开「开发者模式 + USB 调试」：
   - 设置 → 关于本机 → 连点 HarmonyOS 版本 5–7 次
   - 设置 → 系统 → 开发人员选项 → 开启「USB 调试」
5. 手机弹「允许 USB 调试？」点**允许**
6. 工具里点「**获取 UDID**」按钮
7. UDID 自动复制到剪贴板，**粘贴回传给开发者**（微信/邮件均可）

## 工程结构

```
udid-picker/
├── main.py                       # GUI 主程序（跨平台）
├── .github/workflows/build.yml   # GitHub Actions: 自动打包 Windows .exe
├── .gitignore
└── README.md
```

`hdc.exe` 不放仓库——workflow 跑的时候用 `openharmony-rs/setup-ohos-sdk` 从 OpenHarmony GitHub 镜像自动拉取（首次约 5 分钟，后续走 cache 秒级）。

## 本地调试（Mac/Linux）

```bash
# 从 DevEco Studio 拷一个 hdc 到当前目录
cp /Applications/DevEco-Studio.app/Contents/sdk/HarmonyOS-NEXT-DBn/openharmony/toolchains/hdc .

# 直接跑
python3 main.py
```

## 触发打包

- **自动**：改了 `main.py` push 到 main
- **手动**：仓库 → Actions → Build Windows EXE → Run workflow
- **发版**：`git tag v1.0.0 && git push --tags` → 自动建 Release 附带 .exe

## 隐私

工具只调用本地 `hdc shell bm get --udid` 命令，不联网，不上传任何信息。
