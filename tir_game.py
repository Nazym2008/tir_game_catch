import tkinter as tk
import random
import math


# ОСНОВНОЙ ИГРОВОЙ ОБЪЕКТ
class GameObject:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size


# КЛАСС МИШЕНИ
class Target(GameObject):
    def __init__(self, canvas):
        super().__init__(canvas, 400, 250, 30)

        self.speed_x = 3
        self.speed_y = 2

        self.draw()

    def draw(self):
        self.canvas.delete("target")

        self.canvas.create_oval(
            self.x - 30, self.y - 30,
            self.x + 30, self.y + 30,
            fill="red", outline="white", width=3,
            tags="target"
        )

        self.canvas.create_oval(
            self.x - 20, self.y - 20,
            self.x + 20, self.y + 20,
            fill="white", outline="red",
            tags="target"
        )

        self.canvas.create_oval(
            self.x - 10, self.y - 10,
            self.x + 10, self.y + 10,
            fill="red", outline="white",
            tags="target"
        )

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x >= 770 or self.x <= 30:
            self.speed_x *= -1

        if self.y >= 470 or self.y <= 30:
            self.speed_y *= -1

        self.draw()

    def relocate(self):
        self.x = random.randint(60, 740)
        self.y = random.randint(60, 440)
        self.draw()


# КЛАСС ПУЛИ
class Bullet(GameObject):
    def __init__(self, canvas, x, y, target_x, target_y):
        super().__init__(canvas, x, y, 5)

        dx = target_x - x
        dy = target_y - y

        distance = math.hypot(dx, dy)

        if distance == 0:
            distance = 1

        self.speed_x = dx / distance * 12
        self.speed_y = dy / distance * 12

        self.item = self.canvas.create_oval(
            x - 5, y - 5,
            x + 5, y + 5,
            fill="yellow", outline="black"
        )

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        self.canvas.coords(
            self.item,
            self.x - 5, self.y - 5,
            self.x + 5, self.y + 5
        )


# ГЛАВНЫЙ КЛАСС ИГРЫ
class Game:
    def __init__(self, root):
        self.root = root

        self.root.title("2D ТИР")
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        self.score = 0
        self.level = 1
        self.time_left = 60

        self.bullets = []
        self.running = True

        # ИНТЕРФЕЙС
        self.info = tk.Frame(root, bg="#202020")
        self.info.pack(fill="x")

        self.score_label = tk.Label(
            self.info, text="Очки: 0",
            fg="white", bg="#202020",
            font=("Arial", 18, "bold")
        )
        self.score_label.pack(side="left", padx=30, pady=10)

        self.timer_label = tk.Label(
            self.info, text="Время: 60",
            fg="white", bg="#202020",
            font=("Arial", 18, "bold")
        )
        self.timer_label.pack(side="left", padx=50)

        self.level_label = tk.Label(
            self.info, text="Уровень: 1",
            fg="white", bg="#202020",
            font=("Arial", 18, "bold")
        )
        self.level_label.pack(side="left", padx=30)

        # ИГРОВОЕ ПОЛЕ
        self.canvas = tk.Canvas(
            root, width=800, height=500,
            bg="#72B85B",
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.create_rectangle(
            0, 480, 800, 500,
            fill="#795548", outline=""
        )

        self.target = Target(self.canvas)

        self.canvas.bind("<Button-1>", self.shoot)

        # КНОПКА ПЕРЕЗАПУСКА
        self.restart_button = tk.Button(
            root,
            text="Начать заново",
            font=("Arial", 14, "bold"),
            command=self.restart
        )
        self.restart_button.pack(pady=5)

        self.game_loop()
        self.timer_loop()

    # СТРЕЛЬБА
    def shoot(self, event):
        if not self.running:
            return

        bullet = Bullet(
            self.canvas,
            400, 480,
            event.x, event.y
        )

        self.bullets.append(bullet)

    # ОБНОВЛЕНИЕ ИГРЫ
    def game_loop(self):
        if not self.running:
            return

        self.target.move()

        for bullet in self.bullets[:]:
            bullet.move()

            distance = math.hypot(
                bullet.x - self.target.x,
                bullet.y - self.target.y
            )

            # ПРОВЕРКА ПОПАДАНИЯ
            if distance <= 30:
                self.score += 1

                self.canvas.delete(bullet.item)
                self.bullets.remove(bullet)

                self.target.relocate()

                # НОВЫЙ УРОВЕНЬ
                self.level = self.score // 5 + 1

                speed = 3 + (self.level - 1)

                self.target.speed_x = speed
                self.target.speed_y = speed * 0.7

                self.score_label.config(
                    text="Очки: " + str(self.score)
                )

                self.level_label.config(
                    text="Уровень: " + str(self.level)
                )

            elif (bullet.x < 0 or bullet.x > 800 or
                  bullet.y < 0 or bullet.y > 500):

                self.canvas.delete(bullet.item)
                self.bullets.remove(bullet)

        self.root.after(20, self.game_loop)

    # ТАЙМЕР
    def timer_loop(self):
        if not self.running:
            return

        self.time_left -= 1

        self.timer_label.config(
            text="Время: " + str(self.time_left)
        )

        if self.time_left <= 0:
            self.end_game()
            return

        self.root.after(1000, self.timer_loop)

    # КОНЕЦ ИГРЫ
    def end_game(self):
        self.running = False

        self.canvas.create_rectangle(
            150, 170, 650, 340,
            fill="white", outline="black",
            width=3, tags="result"
        )

        self.canvas.create_text(
            400, 210,
            text="ИГРА ОКОНЧЕНА!",
            fill="red",
            font=("Arial", 28, "bold"),
            tags="result"
        )

        self.canvas.create_text(
            400, 260,
            text="Ваш результат: " + str(self.score),
            fill="black",
            font=("Arial", 22),
            tags="result"
        )

        self.canvas.create_text(
            400, 300,
            text="Нажмите «Начать заново»",
            fill="blue",
            font=("Arial", 16),
            tags="result"
        )

    # ПЕРЕЗАПУСК
    def restart(self):
        self.running = False

        self.canvas.delete("all")

        self.score = 0
        self.level = 1
        self.time_left = 60

        self.bullets = []
        self.running = True

        self.canvas.create_rectangle(
            0, 480, 800, 500,
            fill="#795548", outline=""
        )

        self.score_label.config(text="Очки: 0")
        self.timer_label.config(text="Время: 60")
        self.level_label.config(text="Уровень: 1")

        self.target = Target(self.canvas)

        self.game_loop()
        self.timer_loop()


# ЗАПУСК ИГРЫ
root = tk.Tk()
game = Game(root)

root.mainloop()
