import tkinter as tk
import functools
fp = functools.partial

NASA_GREY = "#17171b"
NASA_LIGHT_GREY = "#959599"

class Page(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.controller = controller

        self.controls_window = tk.Frame(self)
        self.controls_window.pack(fill="x", side="top", anchor="nw")
        self.controls_window.configure(bg="black")

        self.content_window = tk.Frame(self)
        self.content_window.pack(fill="both", expand=True, side="top")
        self.content_window.configure(bg="black", borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    
    def go_to_start(self):
            self.controller.show_frame(Page.main_page)
    
    main_page = None


class ScrollList(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=self.interior.winfo_reqwidth())

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

        def _on_mousewheel(event, scroll):
            self.canvas.yview_scroll(int(scroll), "units")

        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<Button-4>", fp(_on_mousewheel, scroll=-1))
            self.canvas.bind_all("<Button-5>", fp(_on_mousewheel, scroll=1))

        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")


        scrollbar_v = tk.Scrollbar(master)
        scrollbar_v.pack(side= "right", fill="y")
        self.canvas = tk.Canvas(master, bd=0, highlightthickness=0, yscrollcommand=scrollbar_v.set, bg="black")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        scrollbar_v.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.interior = tk.Frame(self.canvas, bg="black")
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
        self.interior.bind('<Configure>', _configure_interior)
        self.canvas.bind('<Configure>', _configure_canvas)
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

    def _scroll_to_bottom(self):
            self.canvas.yview_moveto(tk.END)

class ListItem(tk.Frame):
    def __init__(self, master, bg=NASA_GREY):
        super().__init__(master, bg=bg)
    
    def place_item(self):
        self.pack(pady=5, padx=10, fill="x")


class HyperLabel(tk.Label):
    def __init__(self, master, text, command, wraplength, font=("Helvetica", 20), fg="white", justify="left", bg=NASA_GREY, cursor="hand2"):
        super().__init__(master, text = text, font=font, fg=fg, justify=justify, bg=bg, cursor=cursor, wraplength=wraplength)
        self.command = command
        self.font = font
        self.text = text

        def _underline_on_enter(event):
            self.config(cursor="hand2", font=(self.font[0], self.font[1], "underline"))

        def _underline_on_leave(event):
            self.config(cursor="", font=(self.font[0], self.font[1], "normal"))

        def _execute_on_click(event):
            self.command()

        self.bind("<Enter>", _underline_on_enter)
        self.bind("<Leave>", _underline_on_leave)
        self.bind("<Button-1>", _execute_on_click)