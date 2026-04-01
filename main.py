from loguru import logger
import csv
import os
logger.remove()

class Task:
    def __init__(self, title, description, importance=1, status="New"):
        self.title = title
        self.description = description
        self.importance = importance
        self.status = status

    def mark_as_done(self):
        self.status = "Done"

class TaskManager:
    def __init__(self, tasks_file="tasks.csv"):
        self.tasks_file = tasks_file
        self.tasks = []
        self.completed_tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, mode='r', newline='') as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    task = Task(
                        row['Title'],
                        row['Description'],
                        int(row['Importance']),
                        row['Status']
                    )
                    if task.status == "Done":
                        self.completed_tasks.append(task)
                    else:
                        self.tasks.append(task)

    def save_tasks(self):
        with open(self.tasks_file, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Title", "Description", "Importance", "Status"])
            for task in self.tasks:
                writer.writerow([task.title, task.description, task.importance, task.status])
            for task in self.completed_tasks:
                writer.writerow([task.title, task.description, task.importance, task.status])

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()
        message = f"Добавлена новая задача: {task.title}"
        logger.success(message)
        print(message)

    def list_tasks(self):
        message = "Список активных задач (отсортированных по важности):\n"
        print(message)
        logger.info("Начинается сортировка задач")
        sorted_tasks = sorted(self.tasks, key=lambda task: task.importance)
        for task in sorted_tasks:
            message = f"Заголовок: {task.title}, Описание: {task.description}, Важность: {task.importance}, Статус: {task.status}"
            print(message)

        if self.completed_tasks:
            message = "Список завершенных задач:"
            print(message)
            for task in self.completed_tasks:
                message = f"Заголовок: {task.title}, Описание: {task.description}, Важность: {task.importance}, Статус: {task.status}"
                print(message)

    def mark_task_as_done(self, title):
        for task in self.tasks:
            if task.title == title:
                task.mark_as_done()
                self.completed_tasks.append(task)
                self.tasks.remove(task)
                self.save_tasks()
                message = f"Задача '{title}' отмечена как завершенная."
                logger.success(message)
                print(message)
                return
        message = f"Задача с заголовком '{title}' не найдена."
        logger.warning(message)
        print(message)

def main():
    log_file = "task_manager.log"
    logger.add(log_file)

    task_manager = TaskManager()

    while True:
        print("1. Добавить задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как завершенную")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите заголовок задачи: ")
            description = input("Введите описание задачи: ")
            importance = int(input("Введите индекс важности (1-5): "))
            if 1 <= importance <= 5:
                task = Task(title, description, importance)
                task_manager.add_task(task)
            else:
                print("Неверный индекс важности. Индекс должен быть в диапазоне от 1 до 5.")
                logger.warning(f"Пользователь ввёл неожидаемый индекс - {importance}")
        elif choice == '2':
            task_manager.list_tasks()
        elif choice == '3':
            title = input("Введите заголовок задачи, которую хотите отметить как завершенную: ")
            task_manager.mark_task_as_done(title)
        elif choice == '4':
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие снова.")
            logger.warning("Пользователь ввёл неожидаемый вариант")
        print()


if __name__ == "__main__":
    main()
