import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import csv
import os


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, index):
        if 0 <= index < len(self.books):
            return self.books.pop(index)
        return None

    def __str__(self):
        return f"Library: {self.name}, Total Books: {len(self.books)}"


class Book:
    def __init__(self, name, author, year, theme, photo=None):
        self.name = name
        self.author = author
        self.year = year
        self.theme = theme
        self.photo = photo  # Filepath to the photo

    def __str__(self):
        return f"'{self.name}' by {self.author} ({self.year}), Theme: {self.theme}"


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.library = None

        self.root.title("Library Management System")
        self.root.geometry("700x500")

        # UI Elements
        self.create_button = tk.Button(
            root, text="Create Library", command=self.create_library, font=("Helvetica", 12)
        )
        self.load_button = tk.Button(
            root, text="Load Library", command=self.load_library, font=("Helvetica", 12)
        )
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app, font=("Helvetica", 12))

        self.create_button.pack(pady=10)
        self.load_button.pack(pady=10)
        self.exit_button.pack(pady=10)

    def create_library(self):
        name = simpledialog.askstring("Library Name", "Enter the library name:")
        if name:
            self.library = Library(name)
            messagebox.showinfo("Success", f"Library '{name}' created!")
            self.open_library_interface()
        else:
            messagebox.showerror("Error", "Library name cannot be empty.")

    def load_library(self):
        files = [file for file in os.listdir() if file.endswith(".csv")]
        if not files:
            messagebox.showinfo("No Libraries", "No saved libraries found!")
            return

        file_choice = simpledialog.askinteger(
            "Load Library",
            f"Choose a library to load:\n\n" + "\n".join([f"{i+1}. {file}" for i, file in enumerate(files)]),
        )
        if file_choice and 1 <= file_choice <= len(files):
            filename = files[file_choice - 1]
            self.library = self.load_from_file(filename)
            messagebox.showinfo("Success", f"Library '{self.library.name}' loaded!")
            self.open_library_interface()
        else:
            messagebox.showerror("Error", "Invalid choice!")

    def open_library_interface(self):
        if not self.library:
            return

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Library: {self.library.name}")

        # Treeview for book list
        self.book_list = ttk.Treeview(
            self.root, columns=("Name", "Author", "Year", "Theme", "Photo"), show="headings"
        )
        self.book_list.heading("Name", text="Book Name")
        self.book_list.heading("Author", text="Author")
        self.book_list.heading("Year", text="Year")
        self.book_list.heading("Theme", text="Theme")
        self.book_list.heading("Photo", text="Photo")
        self.book_list.pack(fill=tk.BOTH, expand=True, pady=10)

        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.book_list.tag_configure("lightblue", background="lightblue")
        self.book_list.tag_configure("gray", background="lightgray")

        # Buttons
        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book, font=("Helvetica", 12))
        self.edit_button = tk.Button(self.root, text="Edit Book", command=self.edit_book, font=("Helvetica", 12))
        self.remove_button = tk.Button(self.root, text="Remove Book", command=self.remove_book, font=("Helvetica", 12))
        self.save_button = tk.Button(self.root, text="Save Library", command=self.save_library, font=("Helvetica", 12))
        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_main, font=("Helvetica", 12))

        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Populate book list
        self.refresh_book_list()

    def add_book(self):
        if not self.library:
            return

        name = simpledialog.askstring("Book Title", "Enter the book title:")
        author = simpledialog.askstring("Author", "Enter the author's name:")
        year = simpledialog.askstring("Year", "Enter the year of publication:")
        theme = simpledialog.askstring("Theme", "Enter the theme of the book:")
        photo = filedialog.askopenfilename(
            title="Select Book Photo", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")]
        )

        if name and author and year and theme:
            book = Book(name, author, year, theme, photo)
            self.library.add_book(book)
            self.refresh_book_list()
            messagebox.showinfo("Success", f"Book '{name}' added!")
        else:
            messagebox.showerror("Error", "All fields except photo must be filled out!")

    def edit_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        index = int(self.book_list.index(selected_item[0]))
        book = self.library.books[index]

        # Open dialog to edit book details
        name = simpledialog.askstring("Edit Book", "Edit book title:", initialvalue=book.name)
        author = simpledialog.askstring("Edit Book", "Edit author name:", initialvalue=book.author)
        year = simpledialog.askstring("Edit Book", "Edit year of publication:", initialvalue=book.year)
        theme = simpledialog.askstring("Edit Book", "Edit theme of the book:", initialvalue=book.theme)
        photo = filedialog.askopenfilename(
            title="Select Book Photo (optional)", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")]
        )

        if name and author and year and theme:
            # Update the book details
            book.name = name
            book.author = author
            book.year = year
            book.theme = theme
            if photo:
                book.photo = photo
            self.refresh_book_list()
            messagebox.showinfo("Success", "Book details updated!")
        else:
            messagebox.showerror("Error", "All fields except photo must be filled out!")

    def remove_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        index = int(self.book_list.index(selected_item[0]))
        removed_book = self.library.remove_book(index)
        if removed_book:
            self.refresh_book_list()
            messagebox.showinfo("Success", f"Book '{removed_book.name}' removed!")

    def save_library(self):
        if not self.library:
            return

        filename = simpledialog.askstring("Save Library", "Enter the filename to save the library:")
        if filename:
            if not filename.endswith(".csv"):
                filename += ".csv"
            self.save_to_file(self.library, filename)
            messagebox.showinfo("Success", f"Library saved to '{filename}'!")

    def back_to_main(self):
        self.library = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def refresh_book_list(self):
        for row in self.book_list.get_children():
            self.book_list.delete(row)

        for idx, book in enumerate(self.library.books):
            tag = "lightblue" if idx % 2 == 0 else "gray"
            self.book_list.insert(
                "", tk.END, values=(book.name, book.author, book.year, book.theme, book.photo or "No Photo"), tags=(tag,)
            )

    @staticmethod
    def save_to_file(library, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Library Name", library.name])
            writer.writerow(["Book Name", "Author", "Year", "Theme", "Photo"])
            for book in library.books:
                writer.writerow([book.name, book.author, book.year, book.theme, book.photo])

    @staticmethod
    def load_from_file(filename):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip library name
            library_name = next(reader)[1]
            library = Library(library_name)

            for row in reader:
                if row:
                    name, author, year, theme, photo = row
                    library.add_book(Book(name, author, year, theme, photo or None))

        return library

    def exit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
