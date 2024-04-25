import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font

class RichTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NexusTech Text Editor")
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab_button = tk.Button(self, text="New Tab", command=self.new_tab)
        self.add_tab_button.pack(side="top", padx=5)

        self.menu = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu, tearoff=False)
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

        self.format_menu = tk.Menu(self.menu, tearoff=False)
        self.format_menu.add_command(label="Font", command=self.choose_font)
        self.format_menu.add_command(label="Font Color", command=self.choose_font_color)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold, accelerator="Ctrl+B")
        self.format_menu.add_command(label="Italic", command=self.toggle_italic, accelerator="Ctrl+I")
        self.format_menu.add_command(label="Underline", command=self.toggle_underline, accelerator="Ctrl+U")
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Align Left", command=lambda: self.align_text("left"))
        self.format_menu.add_command(label="Align Center", command=lambda: self.align_text("center"))
        self.format_menu.add_command(label="Align Right", command=lambda: self.align_text("right"))
        self.menu.add_cascade(label="Format", menu=self.format_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label="About Text Editor", command=self.about_text_editor)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menu)

        self.bind_shortcuts()

    def create_tab(self, tab_name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tab_name)
        text = tk.Text(tab, wrap="word", font=("Arial", 12))
        text.pack(expand=True, fill="both")

        close_button = tk.Button(tab, text="x", command=lambda: self.close_tab(tab))
        close_button.place(relx=1.0, rely=0, anchor="ne")

    def close_tab(self, tab):
        self.notebook.forget(tab)

    def new_tab(self):
        tab_count = self.notebook.index("end") + 1
        tab_name = f"Tab {tab_count}"
        self.create_tab(tab_name)
        self.notebook.select(tab_name)

    def bind_shortcuts(self):
        self.bind_all("<Control-n>", lambda event: self.new_file())
        self.bind_all("<Control-o>", lambda event: self.open_file())
        self.bind_all("<Control-s>", lambda event: self.save_file())
        self.bind_all("<Control-Shift-S>", lambda event: self.save_as_file())
        self.bind_all("<Control-x>", lambda event: self.cut())
        self.bind_all("<Control-c>", lambda event: self.copy())
        self.bind_all("<Control-v>", lambda event: self.paste())
        self.bind_all("<Control-b>", lambda event: self.toggle_bold())
        self.bind_all("<Control-i>", lambda event: self.toggle_italic())
        self.bind_all("<Control-u>", lambda event: self.toggle_underline())

    def new_file(self):
        text = self.notebook.select().winfo_children()[0]
        text.delete(1.0, tk.END)

    def open_file(self):
        text = self.notebook.select().winfo_children()[0]
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            filename = os.path.basename(file_path)
            with open(file_path, "r") as file:
                text.delete(1.0, tk.END)
                text.insert(1.0, file.read())
            self.notebook.tab("current", text=filename)

    def save_file(self):
        text = self.notebook.select().winfo_children()[0]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text.get(1.0, tk.END))

    def save_as_file(self):
        self.save_file()

    def cut(self):
        text = self.notebook.select().winfo_children()[0]
        text.event_generate("<<Cut>>")

    def copy(self):
        text = self.notebook.select().winfo_children()[0]
        text.event_generate("<<Copy>>")

    def paste(self):
        text = self.notebook.select().winfo_children()[0]
        text.event_generate("<<Paste>>")

    def undo(self):
        text = self.notebook.select().winfo_children()[0]
        text.edit_undo()

    def redo(self):
        text = self.notebook.select().winfo_children()[0]
        text.edit_redo()

    def toggle_bold(self):
        text = self.notebook.select().winfo_children()[0]
        current_tags = text.tag_names("sel.first")
        if "bold" in current_tags:
            text.tag_remove("bold", "sel.first", "sel.last")
        else:
            text.tag_add("bold", "sel.first", "sel.last")
            text.tag_configure("bold", font=("Arial", 12, "bold"))

    def toggle_italic(self):
        text = self.notebook.select().winfo_children()[0]
        current_tags = text.tag_names("sel.first")
        if "italic" in current_tags:
            text.tag_remove("italic", "sel.first", "sel.last")
        else:
            text.tag_add("italic", "sel.first", "sel.last")
            text.tag_configure("italic", font=("Arial", 12, "italic"))

    def toggle_underline(self):
        text = self.notebook.select().winfo_children()[0]
        current_tags = text.tag_names("sel.first")
        if "underline" in current_tags:
            text.tag_remove("underline", "sel.first", "sel.last")
        else:
            text.tag_add("underline", "sel.first", "sel.last")
            text.tag_configure("underline", underline=True)

    def choose_font(self):
        text = self.notebook.select().winfo_children()[0]
        font_tuple = font.Font(font=text["font"])
        chosen_font = font.families()
        font_name = messagebox.askstring("Choose Font", "Enter font name:", parent=self)
        if font_name:
            font_tuple.configure(family=font_name)
            text.configure(font=font_tuple)

    def choose_font_color(self):
        text = self.notebook.select().winfo_children()[0]
        color = tk.colorchooser.askcolor(parent=self)
        if color:
            text.tag_add("font_color", "sel.first", "sel.last")
            text.tag_configure("font_color", foreground=color[1])

    def align_text(self, alignment):
        text = self.notebook.select().winfo_children()[0]
        text.tag_configure("align", justify=alignment)
        text.tag_add("align", "sel.first", "sel.last")

    def about_text_editor(self):
        messagebox.showinfo("About Text Editor", "NexusTech Text Editor is a tool created in tkinter python")

    def quit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            super().quit()

if __name__ == "__main__":
    app = RichTextEditor()
    app.mainloop()
