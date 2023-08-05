import tkinter
import tkinter.ttk as ttk
import turtle
import threading


class BetterTurtle(tkinter.Tk):
    def __init__(self, title: str="BetterTurtle", geometry: str="500x500", active_control: bool=True):
        super().__init__()
        self.title(title)
        self.geometry(geometry)

        self.columnconfigure(7, weight=1)
        self.rowconfigure(1, weight=1)

        self.active_control = active_control

        # create widgets
        self.turtle_canvas = tkinter.Canvas(self)
        self.larger_button = ttk.Button(self, width=2, text="+", command=self.__zoom_in)
        self.smaller_button = ttk.Button(self, width=2, text="-", command=self.__zoom_out)
        self.left_button = ttk.Button(self, width=2, text="←", command=self.__move_left) #←↑→↓
        self.up_button = ttk.Button(self, width=2, text="↑", command=self.__move_up)
        self.right_button = ttk.Button(self, width=2, text="→", command=self.__move_right)
        self.down_button = ttk.Button(self, width=2, text="↓", command=self.__move_down)
        self.spacing_label = ttk.Label(self, text="")

        # grid widgets
        self.larger_button.grid(column=0, row=0)
        self.smaller_button.grid(column=1, row=0)
        self.left_button.grid(column=2, row=0)
        self.up_button.grid(column=3, row=0)
        self.right_button.grid(column=4, row=0)
        self.down_button.grid(column=5, row=0)
        self.spacing_label.grid(column=6, row=0)
        self.turtle_canvas.grid(column=0, row=1, columnspan=8, sticky="nsew")

        self.turtle = turtle.RawTurtle(self.turtle_canvas)

        thread = threading.Thread(target=lambda: self.mainloop)
        thread.start()

    def __zoom_in(self):
        if self.active_control:
            self.turtle_canvas.scale("all", 0, 0, 1.1, 1.1)

    def __zoom_out(self):
        if self.active_control:
            self.turtle_canvas.scale("all", 0, 0, 0.9, 0.9)

    def __move_left(self):
        if self.active_control:
            self.turtle_canvas.move("all", -10, 0)

    def __move_right(self):
        if self.active_control:
            self.turtle_canvas.move("all", 10, 0)

    def __move_up(self):
        if self.active_control:
            self.turtle_canvas.move("all", 0, -10)
    
    def __move_down(self):
        if self.active_control:
            self.turtle_canvas.move("all", 0, 10)

    def get_turtle(self):
        return self.turtle

    def not_exit(self):
        self.turtle.getscreen().update()
        self.mainloop()

    def tracer(self, number: int, *args):
        self.turtle._tracer(number)
