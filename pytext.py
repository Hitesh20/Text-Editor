import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class MenuBar:
    def __init__(self, parent):
        font_specs = ('ubuntu', 10)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File", accelerator="Ctrl+N", command=parent.new_file)
        file_dropdown.add_command(label="Open File", accelerator="Ctrl+O", command=parent.open_file)
        file_dropdown.add_command(label="Save", accelerator="Ctrl+S", command=parent.save)
        file_dropdown.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit", accelerator="Ctrl+E", command=parent.master.destroy)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes", command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About", command=self.show_about_message)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

    def show_about_message(self):
        box_title = "About PyText"
        box_message = "A simple text editor using Tkinter"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 1 - PyText Editor"
        messagebox.showinfo(box_title, box_message)

class StatusBar:
    def __init__(self, parent):
        font_specs = ('ubuntu', 8)

        self.status = tk.StringVar()
        self.status.set("PyText Editor")

        label = tk.Label(parent.textarea, textvariable=self.status, fg='black', bg='lightgrey', anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your File has been saved")
        else:
            self.status.set("PyText Editor")


class PyText:
    def __init__(self, master):
        master.title("Untitled - PyText")
        master.geometry("800x600")

        font_specs = ('ubuntu', 18)

        self.master = master
        self.fileName=None

        self.textarea = tk.Text(master, font = font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menuBar=MenuBar(self)
        self.statusBar=StatusBar(self)

        self.bind_shortcuts()


    def set_window_title(self, name=None):
        if name:
            self.master.title(name + ' - PyText')
        else:
            self.master.title('Untitled - PyText')

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.fileName = None
        self.set_window_title()

    def open_file(self, *args):
        self.fileName=filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),("Text Files", "*.txt"), ("Python Scripts", "*.py"),
                       ("Markdown Documents", "*.md"), ("JavaScript Files", "*.js"), ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css"), ("Java Files", "*.java")]
        )
        if self.fileName:
            self.textarea.delete(1.0, tk.END)
            with open(self.fileName, "r") as f:
                self.textarea.insert(1.0, f.read())

            self.set_window_title(self.fileName)

    def save(self, *args):
        if self.fileName:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.fileName, "w") as f:
                    f.write(textarea_content)
                self.statusBar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()


    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile='Untitled.txt',
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Scripts", "*.py"),
                           ("Markdown Documents", "*.md"), ("JavaScript Files", "*.js"), ("HTML Documents", "*.html"),
                           ("CSS Documents", "*.css"), ("Java Files", "*.java")]
            )
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)

            self.fileName = new_file
            self.set_window_title(self.fileName)
            self.statusBar.update_status(True)
        except Exception as e:
            print(e)


    def exit(self, *args):
        master.destroy()



    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Control-e>', self.exit)
        self.textarea.bind('<Key>', self.statusBar.update_status)




if __name__ == "__main__":
    master = tk.Tk()
    pt = PyText(master)     #initializing pyText
    master.mainloop()
