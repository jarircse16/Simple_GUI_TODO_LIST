import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Task:
    def __init__(self, description, date, time):
        self.description = description
        self.completed = False
        self.date = date
        self.time = time

class TodoListManager:
    def __init__(self, window):
        self.tasks = []

        # Create the main window
        self.window = window
        self.window.title("To-Do List Manager")
        self.window.overrideredirect(True)  # Remove default window decorations

        self.x = 0
        self.y = 0

        # Create the title bar
        self.title_bar = ttk.Frame(self.window)
        self.title_bar.pack(fill=tk.X)

        # Bind mouse events for window movement
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.move_window)

        # Create the title label
        self.label_title = ttk.Label(self.title_bar, text="To-Do List Manager", font=("Helvetica", 12, "bold"))
        self.label_title.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the close button
        self.button_close = ttk.Button(self.title_bar, text="X", command=self.window.destroy)
        self.button_close.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create GUI elements
        self.label_description = ttk.Label(self.window, text="Task Description:")
        self.label_description.pack()

        self.entry_description = ttk.Entry(self.window)
        self.entry_description.pack()

        self.label_date = ttk.Label(self.window, text="Date (YYYY-MM-DD):")
        self.label_date.pack()

        self.entry_date = ttk.Entry(self.window)
        self.entry_date.pack()

        self.label_time = ttk.Label(self.window, text="Time (HH:MM):")
        self.label_time.pack()

        self.entry_time = ttk.Entry(self.window)
        self.entry_time.pack()

        self.button_add = ttk.Button(self.window, text="Add Task", command=self.add_task)
        self.button_add.pack()

        self.button_mark_completed = ttk.Button(self.window, text="Mark Completed", command=self.mark_task_as_completed)
        self.button_mark_completed.pack()

        self.button_delete = ttk.Button(self.window, text="Delete Task", command=self.delete_task)
        self.button_delete.pack()

        self.listbox_tasks = tk.Listbox(self.window, selectmode=tk.SINGLE)
        self.listbox_tasks.pack()

        self.load_tasks()  # Load saved tasks
        self.refresh_tasks()

    def add_task(self):
        description = self.entry_description.get()
        date = self.entry_date.get()
        time = self.entry_time.get()

        if description and date and time:
            task = Task(description, date, time)
            self.tasks.append(task)
            self.save_tasks()  # Save updated tasks
            self.entry_description.delete(0, tk.END)
            self.entry_date.delete(0, tk.END)
            self.entry_time.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter task details.")

    def mark_task_as_completed(self):
        selected_index = self.listbox_tasks.curselection()
        if selected_index:
            index = selected_index[0]
            task = self.tasks[index]
            if task.completed:
                messagebox.showinfo("Info", "Task is already completed.")
            else:
                task.completed = True
                self.save_tasks()  # Save updated tasks
                self.refresh_tasks()

    def delete_task(self):
        selected_index = self.listbox_tasks.curselection()
        if selected_index:
            index = selected_index[0]
            task = self.tasks.pop(index)
            messagebox.showinfo("Info", f"Task '{task.description}' deleted from the to-do list.")
            self.save_tasks()  # Save updated tasks
            self.refresh_tasks()

    def refresh_tasks(self):
        self.listbox_tasks.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task.completed else "Incomplete"
            self.listbox_tasks.insert(tk.END, f"{task.description} ({status}) - {task.date} {task.time}")

    def move_window(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.window.winfo_x() + deltax
        new_y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{new_x}+{new_y}")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.description},{task.completed},{task.date},{task.time}\n")  # Corrected line

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        description, completed, date, time = parts
                        task = Task(description, date, time)
                        task.completed = True if completed == "True" else False
                        self.tasks.append(task)
        except FileNotFoundError:
            return

# Create the main window
window = tk.Tk()

# Create a TodoListManager instance
manager = TodoListManager(window)

# Start the main event loop
window.mainloop()
