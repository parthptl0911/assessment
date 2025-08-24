import os
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "MiniBlog"
POSTS_DIR = "posts"

class User:
    def __init__(self, name: str):
        self.name = name.strip()

    def is_valid(self) -> bool:
        return len(self.name) > 0


class Post:
    def __init__(self, user: User, title: str, content: str):
        self.user = user
        self.title = title.strip()
        self.content = content.rstrip()

    def _slugify(self, text: str) -> str:
        text = text.strip().lower()
        text = text.replace(" ", "_")
        text = re.sub(r"[^a-z0-9_\-]", "", text)
        return text or "untitled"

    def filename(self) -> str:
        user_slug = self._slugify(self.user.name)
        title_slug = self._slugify(self.title)
        return f"{user_slug}_{title_slug}.txt"

    def to_file(self, folder: str) -> str:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, self.filename())
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = [
            f"Title: {self.title}",
            f"Author: {self.user.name}",
            f"Created: {now}",
            "-" * 40,
        ]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(header) + "\n")
            f.write(self.content + "\n")
        return path


class MiniBlogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x600")
        self.minsize(840, 520)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        self._build_editor_panel()
        self._build_viewer_panel()

        self.refresh_file_list()

    def _build_editor_panel(self):
        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

        ttk.Label(frame, text="Create a New Post", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 8)
        )

        ttk.Label(frame, text="Your Name:").grid(row=1, column=0, sticky="w")
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(frame, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(frame, text="Post Title:").grid(row=2, column=0, sticky="w")
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(frame, textvariable=self.title_var)
        self.title_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(frame, text="Content:").grid(row=3, column=0, sticky="nw")
        self.content_text = tk.Text(frame, wrap="word", height=18, undo=True)
        self.content_text.grid(row=3, column=1, columnspan=2, sticky="nsew", pady=4)

        btns = ttk.Frame(frame)
        btns.grid(row=4, column=1, columnspan=2, sticky="e", pady=(8, 0))
        save_btn = ttk.Button(btns, text="Save Post", command=self.save_post)
        clear_btn = ttk.Button(btns, text="Clear", command=self.clear_editor)
        save_btn.grid(row=0, column=0, padx=(0, 6))
        clear_btn.grid(row=0, column=1)

        tip = (
            "Tip: Files are saved in the 'posts' folder.\n"
            "Filename = <yourname>_<title>.txt"
        )
        ttk.Label(frame, text=tip, foreground="#666").grid(
            row=5, column=0, columnspan=3, sticky="sw", pady=(8, 0)
        )

    def _build_viewer_panel(self):
        right = ttk.Frame(self, padding=12)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(3, weight=1)

        ttk.Label(right, text="Saved Posts", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        toolbar = ttk.Frame(right)
        toolbar.grid(row=1, column=0, sticky="ew", pady=(6, 6))
        refresh_btn = ttk.Button(toolbar, text="Refresh List", command=self.refresh_file_list)
        open_btn = ttk.Button(toolbar, text="Open Selected", command=self.open_selected_file)
        refresh_btn.pack(side="left")
        open_btn.pack(side="left", padx=(6, 0))
 
        self.file_list = tk.Listbox(right, height=12, activestyle="dotbox")
        self.file_list.grid(row=2, column=0, sticky="nsew")
        self.file_list.bind("<Double-1>", lambda e: self.open_selected_file())

        ttk.Label(right, text="Preview").grid(row=3, column=0, sticky="w", pady=(8, 0))
        self.preview = tk.Text(right, wrap="word", height=14, state="disabled")
        self.preview.grid(row=4, column=0, sticky="nsew")

    def _read_editor(self):
        name = self.name_var.get().strip()
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", "end").strip()
        return name, title, content

    def clear_editor(self):
        self.title_var.set("")
        self.content_text.delete("1.0", "end")
        self.title_entry.focus_set()

    def save_post(self):
        name, title, content = self._read_editor()

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if not title:
            messagebox.showerror("Error", "Please enter a post title.")
            return
        if not content:
            messagebox.showerror("Error", "Post content cannot be empty.")
            return

        try:
            user = User(name)
            post = Post(user, title, content)
            path = post.to_file(POSTS_DIR)
            messagebox.showinfo("Saved", f"Post saved:\n{os.path.basename(path)}")
            self.refresh_file_list(select_filename=os.path.basename(path))
            self.clear_editor()
        except OSError as e:
            messagebox.showerror("File Error", f"Could not save the post.\n\n{e}")

    def refresh_file_list(self, select_filename: str | None = None):
        self.file_list.delete(0, "end")
        try:
            os.makedirs(POSTS_DIR, exist_ok=True)
            files = [f for f in os.listdir(POSTS_DIR) if f.lower().endswith(".txt")]
            files.sort(key=lambda x: x.lower())
            for f in files:
                self.file_list.insert("end", f)

            if select_filename and select_filename in files:
                idx = files.index(select_filename)
                self.file_list.selection_clear(0, "end")
                self.file_list.selection_set(idx)
                self.file_list.see(idx)
        except OSError as e:
            messagebox.showerror("Folder Error", f"Problem accessing '{POSTS_DIR}'.\n\n{e}")

    def open_selected_file(self):
        try:
            idxs = self.file_list.curselection()
            if not idxs:
                messagebox.showwarning("No Selection", "Please select a file first.")
                return
            filename = self.file_list.get(idxs[0])
            path = os.path.join(POSTS_DIR, filename)
            if not os.path.exists(path):
                messagebox.showerror("Not Found", f"The file does not exist:\n{filename}")
                self.refresh_file_list()
                return
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.preview.configure(state="normal")
            self.preview.delete("1.0", "end")
            self.preview.insert("1.0", content)
            self.preview.configure(state="disabled")
        except OSError as e:
            messagebox.showerror("Read Error", f"Could not read the file.\n\n{e}")


def main():
    app = MiniBlogApp()
    app.mainloop()


if __name__ == "__main__":
    main()
