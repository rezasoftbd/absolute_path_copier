#!/usr/bin/env python3
"""Absolute Path Copier — drag a file or folder in, get its absolute path on the clipboard."""

import os
import tkinter as tk
from tkinter import font as tkfont

from tkinterdnd2 import DND_FILES, TkinterDnD

BG = "#1e1f26"
DROP_BG = "#272935"
DROP_ACTIVE = "#34384a"
ACCENT = "#6c8cff"
TEXT = "#e6e6ec"
MUTED = "#8a8d9b"
OK = "#5fd38d"


def parse_dropped(data: str):
    """tkinterdnd2 hands paths as a brace/space-delimited string. Split it into real paths."""
    paths, buf, in_brace = [], "", False
    for ch in data:
        if ch == "{":
            in_brace = True
        elif ch == "}":
            in_brace = False
            paths.append(buf)
            buf = ""
        elif ch == " " and not in_brace:
            if buf:
                paths.append(buf)
            buf = ""
        else:
            buf += ch
    if buf:
        paths.append(buf)
    return [p for p in paths if p]


class App:
    def __init__(self, root):
        self.root = root
        root.title("Absolute Path Copier")
        root.geometry("560x420")
        root.minsize(440, 340)
        root.configure(bg=BG)

        title_font = tkfont.Font(family="SF Pro Display", size=18, weight="bold")
        hint_font = tkfont.Font(family="SF Pro Text", size=12)
        path_font = tkfont.Font(family="SF Mono", size=12)
        status_font = tkfont.Font(family="SF Pro Text", size=11)

        tk.Label(root, text="Absolute Path Copier", bg=BG, fg=TEXT,
                 font=title_font).pack(pady=(22, 2))
        tk.Label(root, text="Drop a file or folder — its path is copied automatically",
                 bg=BG, fg=MUTED, font=hint_font).pack(pady=(0, 16))

        self.drop = tk.Frame(root, bg=DROP_BG, highlightbackground=ACCENT,
                             highlightthickness=2, bd=0)
        self.drop.pack(fill="both", expand=True, padx=20, pady=(0, 6))
        self.drop.pack_propagate(False)

        self.drop_label = tk.Label(self.drop, text="⤓\n\nDrag & drop here",
                                   bg=DROP_BG, fg=MUTED, font=hint_font, justify="center")
        self.drop_label.pack(expand=True)

        self.path_var = tk.StringVar(value="")
        self.path_box = tk.Entry(root, textvariable=self.path_var, font=path_font,
                                 bg=DROP_BG, fg=TEXT, insertbackground=TEXT,
                                 relief="flat", readonlybackground=DROP_BG, state="readonly")
        self.path_box.pack(fill="x", padx=20, pady=(8, 4))
        self.path_box.bind("<Button-1>", lambda e: self.select_all())

        self.status = tk.Label(root, text="Waiting for a drop…", bg=BG, fg=MUTED,
                               font=status_font)
        self.status.pack(pady=(2, 14))

        for w in (self.drop, self.drop_label):
            w.drop_target_register(DND_FILES)
            w.dnd_bind("<<Drop>>", self.on_drop)
            w.dnd_bind("<<DragEnter>>", self.on_enter)
            w.dnd_bind("<<DragLeave>>", self.on_leave)

    def on_enter(self, _):
        self.drop.configure(bg=DROP_ACTIVE)
        self.drop_label.configure(bg=DROP_ACTIVE, fg=ACCENT)
        return "copy"

    def on_leave(self, _):
        self.drop.configure(bg=DROP_BG)
        self.drop_label.configure(bg=DROP_BG, fg=MUTED)

    def on_drop(self, event):
        self.on_leave(None)
        paths = parse_dropped(event.data)
        if not paths:
            return
        abs_paths = [os.path.abspath(os.path.expanduser(p)) for p in paths]
        joined = "\n".join(abs_paths)

        self.path_var.set(joined if len(abs_paths) == 1 else f"{len(abs_paths)} paths copied")
        self.copy(joined)

        if len(abs_paths) == 1:
            kind = "Folder" if os.path.isdir(abs_paths[0]) else "File"
            self.drop_label.configure(text=f"✓\n\n{os.path.basename(abs_paths[0])}", fg=OK)
            self.flash(f"✓ {kind} path copied to clipboard")
        else:
            self.drop_label.configure(text=f"✓\n\n{len(abs_paths)} items", fg=OK)
            self.flash(f"✓ {len(abs_paths)} paths copied (newline-separated)")

    def copy(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def select_all(self):
        self.path_box.selection_range(0, "end")
        return "break"

    def flash(self, msg):
        self.status.configure(text=msg, fg=OK)
        self.root.after(2600, lambda: self.status.configure(text="Drop another item…", fg=MUTED))


def main():
    root = TkinterDnD.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
