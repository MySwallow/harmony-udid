# -*- coding: utf-8 -*-
"""鸿蒙 HarmonyOS 设备 UDID 一键获取工具

适用：测试方零门槛拿到设备 UDID 反馈给开发者用于内部测试 Profile 注册
依赖：同目录下放 hdc(.exe)
"""
import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

VERSION = "1.0.0"
TITLE = "鸿蒙 UDID 获取工具"


def hdc_path():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    name = "hdc.exe" if sys.platform == "win32" else "hdc"
    bundled = os.path.join(base, name)
    return bundled if os.path.exists(bundled) else "hdc"


def run_hdc(args, timeout=10):
    kwargs = {
        "capture_output": True,
        "text": True,
        "encoding": "utf-8",
        "errors": "ignore",
        "timeout": timeout,
    }
    if sys.platform == "win32":
        kwargs["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
    return subprocess.run([hdc_path()] + args, **kwargs)


def fetch_udid():
    try:
        targets = run_hdc(["list", "targets"], timeout=8)
        stdout = (targets.stdout or "").strip()
        if not stdout or "Empty" in stdout:
            return False, (
                "未检测到设备。\n\n"
                "请检查：\n"
                "  1. 数据线已连接电脑和手机\n"
                "  2. 手机已开启「开发者模式」\n"
                "     （设置 -> 关于本机 -> 多次点击 HarmonyOS 版本）\n"
                "  3. 手机已开启「USB 调试」\n"
                "     （设置 -> 系统 -> 开发人员选项 -> USB 调试）\n"
                "  4. 手机弹窗「允许 USB 调试？」时点了「允许」\n\n"
                "插好后请重新点「获取 UDID」按钮。"
            )

        result = run_hdc(["shell", "bm", "get", "--udid"], timeout=10)
        out = (result.stdout or "").strip()
        match = re.search(r"([A-Fa-f0-9]{64})", out)
        if match:
            return True, match.group(1)
        return False, f"已连接设备，但读取 UDID 失败。\n\nhdc 输出：\n{out or '(空)'}"
    except FileNotFoundError:
        return False, (
            "找不到 hdc。\n\n"
            "本工具同目录下需要 hdc.exe（Win）/ hdc（Mac/Linux）。"
        )
    except subprocess.TimeoutExpired:
        return False, "hdc 命令超时。请拔掉重插 USB 后重试。"
    except Exception as e:
        return False, f"未预期的错误：{e}"


def center(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 3
    win.geometry(f"{w}x{h}+{x}+{y}")


def main():
    root = tk.Tk()
    root.title(f"{TITLE}  v{VERSION}")
    center(root, 620, 440)
    root.resizable(False, False)

    bold = tkfont.Font(size=13, weight="bold")
    normal = tkfont.Font(size=11)
    mono_family = "Consolas" if sys.platform == "win32" else "Menlo"
    mono = tkfont.Font(family=mono_family, size=11)

    tk.Label(root, text=TITLE, font=bold, pady=12).pack()
    tk.Label(
        root,
        text="1. 数据线接电脑    2. 开启开发者模式 + USB 调试    3. 点下方按钮",
        font=normal, fg="#444", pady=4,
    ).pack()

    out_frame = tk.Frame(root, padx=14, pady=10)
    out_frame.pack(fill="both", expand=True)
    out = tk.Text(
        out_frame, height=12, font=mono, wrap="word",
        bg="#fafafa", relief="solid", borderwidth=1, padx=10, pady=8,
    )
    out.pack(fill="both", expand=True)
    out.insert("1.0", "等待操作。点击下方「获取 UDID」按钮开始。")
    out.config(state="disabled")

    state = {"udid": None}

    def show(msg, ok=False):
        out.config(state="normal")
        out.delete("1.0", "end")
        out.insert("1.0", msg)
        out.config(state="disabled")
        copy_btn.config(state="normal" if ok else "disabled")

    def on_fetch():
        show("正在读取……")
        root.update()
        ok, value = fetch_udid()
        if ok:
            state["udid"] = value
            root.clipboard_clear()
            root.clipboard_append(value)
            show(
                f"[读取成功] UDID 已自动复制到剪贴板\n\n{value}\n\n"
                "现在你可以直接粘贴给开发者（微信 / 邮件 / 任意输入框）。",
                ok=True,
            )
        else:
            state["udid"] = None
            show(value)

    def on_copy():
        if state["udid"]:
            root.clipboard_clear()
            root.clipboard_append(state["udid"])
            messagebox.showinfo("已复制", "UDID 已复制到剪贴板")

    btn_frame = tk.Frame(root, pady=6)
    btn_frame.pack()
    tk.Button(
        btn_frame, text="获取 UDID", font=bold, padx=24, pady=8, command=on_fetch,
    ).pack(side="left", padx=8)
    copy_btn = tk.Button(
        btn_frame, text="再次复制", font=normal, padx=16, pady=8,
        command=on_copy, state="disabled",
    )
    copy_btn.pack(side="left", padx=8)

    tk.Label(
        root, text=f"v{VERSION}  ·  本工具不会上传任何信息",
        fg="#999", pady=6,
    ).pack(side="bottom")

    root.mainloop()


if __name__ == "__main__":
    main()
