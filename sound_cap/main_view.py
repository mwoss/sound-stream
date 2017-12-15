from tkinter import *
from tkinter import ttk
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
#         print(meters.get())
#     except ValueError:
#         pass
#
#
# root = Tk()
# root.title("Feet to Meters")
#
# mainframe = ttk.Frame(root, padding="5 5 5 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)
#
# feet = StringVar()
# meters = StringVar()
#
# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W, E))
#
# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
#
# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
#
# for child in mainframe.winfo_children():
#     child.grid_configure(padx=5, pady=5)
#
# # feet_entry.focus()
# root.bind('<Return>', calculate)
#
# root.mainloop()


class SoundRecord(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Sound Record")
        self.frames = {}

        main_cont = ttk.Frame(self)
        main_cont.pack(side='top', fill='both', expand=True)
        main_cont.grid_rowconfigure(0, weight=1)
        main_cont.grid_columnconfigure(0, weight=1)

        frame = MainPage(main_cont, self)
        self.frames[MainPage] = frame
        frame.grid(row=0, column=0, sticky=(N, W, E, S))

        self.show_frame(MainPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


def button_test(text):
    print(text)


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Sound graph")
        label.pack(padx=10, pady=10)

        button = ttk.Button(self, text="Click me", command=lambda: button_test("lul"))
        button.pack(pady=5)

        fig = Figure(figsize=(6, 6))
        plot = fig.add_subplot(1, 1, 1)
        plot.plot([0, 1, 3, 4, 5], [5, 12, 51, 11, 2])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


class AnimatePlot(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Test")
        label.pack(padx=5, pady=5)

        button = ttk.Button(self, text="Back to main page",
                            command=lambda: controller.show_frame(MainPage))
        button.pack(pady=5)


app = SoundRecord()
app.mainloop()
