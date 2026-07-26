import tkinter as tk
import keyboard
import threading
import time


COUNTDOWN = 14
CIRCLE_SIZE = 80
FONT_SIZE = 40

running = False


class TimerApp:
    def __init__(self):
        self.root = tk.Tk()

        # 无边框
        self.root.overrideredirect(True)

        # 置顶
        self.root.attributes("-topmost", True)

        # 窗口大小（给关闭按钮留空间）
        size = CIRCLE_SIZE + 20
        self.root.geometry(f"{size}x{size}")

        # 透明背景
        self.root.configure(bg="black")
        self.root.attributes("-transparentcolor", "black")


        # 画布
        self.canvas = tk.Canvas(
            self.root,
            width=size,
            height=size,
            bg="black",
            highlightthickness=0
        )

        self.canvas.pack()


        # 圆
        self.canvas.create_oval(
            10,
            10,
            10 + CIRCLE_SIZE,
            10 + CIRCLE_SIZE,
            fill="#111111",
            outline=""
        )


        # 数字
        self.text = self.canvas.create_text(
            size // 2,
            size // 2,
            text=str(COUNTDOWN),
            fill="white",
            font=("Arial", FONT_SIZE)
        )


        # 关闭按钮
        self.close = self.canvas.create_text(
            size - 5,
            5,
            text="×",
            fill="red",
            font=("Arial", 16, "bold")
        )


        self.canvas.tag_bind(
            self.close,
            "<Button-1>",
            lambda e: self.root.destroy()
        )


        # 拖动窗口
        self.canvas.bind(
            "<ButtonPress-1>",
            self.start_move
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.move
        )


        keyboard.add_hotkey("q", self.start)


        self.root.mainloop()



    def start_move(self, event):
        self.x = event.x
        self.y = event.y


    def move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y

        self.root.geometry(
            f"+{x}+{y}"
        )


    def start(self):
        global running

        if running:
            return

        running = True

        threading.Thread(
            target=self.countdown,
            daemon=True
        ).start()



    def countdown(self):
        global running

        for i in range(COUNTDOWN, -1, -1):

            self.canvas.itemconfig(
                self.text,
                text=str(i)
            )

            time.sleep(1)


        self.canvas.itemconfig(
            self.text,
            text=str(COUNTDOWN)
        )

        running = False



if __name__ == "__main__":
    TimerApp()