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

        # 窗口置顶
        self.root.attributes("-topmost", True)

        # 窗口大小
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


        # 圆形
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
            fill="lime",
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


        # 全局监听 Q
        # 游戏/其他按键状态下也能触发
        keyboard.on_press_key(
            "q",
            lambda e: self.start()
        )


        self.root.mainloop()



    # 开始拖动
    def start_move(self, event):
        self.x = event.x
        self.y = event.y



    # 移动窗口
    def move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y

        self.root.geometry(
            f"+{x}+{y}"
        )



    # Q触发
    def start(self):
        global running

        # 倒计时期间禁止再次触发
        if running:
            return

        running = True

        threading.Thread(
            target=self.countdown,
            daemon=True
        ).start()



    # 倒计时
    def countdown(self):
        global running

        for i in range(COUNTDOWN, 0, -1):

            # 14-6绿色，5-1红色
            if i > 5:
                color = "lime"
            else:
                color = "red"


            self.canvas.itemconfig(
                self.text,
                text=str(i),
                fill=color
            )

            time.sleep(1)



        # 1结束直接恢复14
        self.canvas.itemconfig(
            self.text,
            text=str(COUNTDOWN),
            fill="lime"
        )

        running = False



if __name__ == "__main__":
    TimerApp()
