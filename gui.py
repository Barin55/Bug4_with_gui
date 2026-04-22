import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from main import TaskManager, Task
import sys
from io import StringIO

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Загружаем менеджер задач (файл tasks.csv будет рядом)
        self.task_manager = TaskManager()

        # Кнопки
        btn_add = tk.Button(root, text="Добавить задачу", command=self.add_task, width=25, height=2)
        btn_add.pack(pady=5)

        btn_view = tk.Button(root, text="Просмотреть задачи", command=self.view_tasks, width=25, height=2)
        btn_view.pack(pady=5)

        btn_done = tk.Button(root, text="Отметить задачу как выполненную", command=self.mark_done, width=25, height=2)
        btn_done.pack(pady=5)

        btn_exit = tk.Button(root, text="Выйти", command=root.quit, width=25, height=2)
        btn_exit.pack(pady=5)

    def add_task(self):
        # Окно добавления задачи
        win = tk.Toplevel(self.root)
        win.title("Новая задача")
        win.geometry("400x300")

        tk.Label(win, text="Заголовок:").pack(pady=5)
        title_entry = tk.Entry(win, width=50)
        title_entry.pack()

        tk.Label(win, text="Описание:").pack(pady=5)
        desc_entry = tk.Entry(win, width=50)
        desc_entry.pack()

        tk.Label(win, text="Важность (1-5):").pack(pady=5)
        imp_spin = tk.Spinbox(win, from_=1, to=5, width=10)
        imp_spin.pack()

        def save():
            title = title_entry.get().strip()
            desc = desc_entry.get().strip()
            try:
                imp = int(imp_spin.get())
                if not (1 <= imp <= 5):
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Важность должна быть числом от 1 до 5")
                return
            if not title:
                messagebox.showerror("Ошибка", "Заголовок не может быть пустым")
                return
            task = Task(title, desc, imp)
            self.task_manager.add_task(task)
            win.destroy()
            messagebox.showinfo("Успех", f"Задача '{title}' добавлена")

        btn_save = tk.Button(win, text="Сохранить", command=save)
        btn_save.pack(pady=10)

    def view_tasks(self):
        # Формируем строку со списком задач (как в консольной версии)
        output = "Список активных задач (отсортированных по важности):\n"
        if not self.task_manager.tasks:
            output += "Нет активных задач.\n"
        else:
            sorted_tasks = sorted(self.task_manager.tasks, key=lambda t: t.importance)
            for task in sorted_tasks:
                output += f"Заголовок: {task.title}, Описание: {task.description}, Важность: {task.importance}, Статус: {task.status}\n"

        if self.task_manager.completed_tasks:
            output += "\nСписок завершенных задач:\n"
            for task in self.task_manager.completed_tasks:
                output += f"Заголовок: {task.title}, Описание: {task.description}, Важность: {task.importance}, Статус: {task.status}\n"
        else:
            output += "\nНет завершенных задач."

        # Показываем в отдельном окне
        win = tk.Toplevel(self.root)
        win.title("Список задач")
        win.geometry("600x400")
        text = tk.Text(win, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(text)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scroll.set)
        scroll.config(command=text.yview)
        text.insert(tk.END, output)
        text.config(state=tk.DISABLED)  # только чтение

    def mark_done(self):
        title = simpledialog.askstring("Завершить задачу", "Введите заголовок задачи:")
        if title:
            self.task_manager.mark_task_as_done(title)
            # Сообщение уже выводится в консоль, но покажем пользователю
            messagebox.showinfo("Результат", f"Задача '{title}' отмечена выполненной (если существовала)")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()