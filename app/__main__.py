import tkinter as tk
from .handlers.APOD import APOD
from .handlers.NEO import NEO
from .gui import Page, ScrollList, ListItem, HyperLabel, NASA_GREY, NASA_LIGHT_GREY

with open('app/key.txt', 'r') as file:
    KEY = file.read()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("NASA API Browser")
        self.geometry("720x720")
        self.minsize(720,720)
        self.configure(bg="black")

        footer = tk.Frame(self, bg="#ebebeb")
        footer.pack(side="bottom", fill="x")

        self.message = tk.Label(footer, text="WELCOME", bg="#ebebeb")
        self.message.pack(anchor="nw")

        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}  
  
        for F in (StartPage,
                  APOD,
                  NEO,
                  ):
  
            frame = F(container, self)

            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0,sticky="nsew")
  
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Page):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        Page.main_page = StartPage

        #####CONTROLS#####
        def validate(P):
            if len(P) == 0:
                return True
            elif len(P) <= 40 and P.isalnum():
                return True
            else:
                return False

        def update_key():
            new_key = key_entry.get()
            if len(new_key)<40:
                controller.message.configure(text="ENTER VALID KEY")
            else:
                with open("key.txt", "w") as file:
                    file.write(new_key)
                KEY = new_key
                controller.message.configure(text="KEY UPDATED")

        char_limiter = (self.controls_window.register(validate), '%P')
        
        tk.Label(self.controls_window,
                 text="API Key: ",
                 bg="black",
                 fg=NASA_LIGHT_GREY
                 ).grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        key_entry = tk.Entry(self.controls_window,
                             validate="key",
                             validatecommand=char_limiter,
                             width=65
                             )
        key_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        tk.Button(self.controls_window,
                  text="Save",
                  command=update_key
                  ).grid(row=0, column=2, padx=10, pady=10)
        
        #####CONTENT#####
        api_list = ScrollList(self.content_window)
        
        APIListItem(api_list.interior,
                    controller,
                    APOD,
                    api_name="Astronomy Picture of the Day",
                    api_description='Astronomy Picture of the Day is a website provided by NASA and Michigan Technological University. According to the website, "Each day a different image or photograph of our universe is featured, along with a brief explanation written by a professional astronomer."'
                    ).place_item()

        APIListItem(api_list.interior,
                    controller,
                    NEO,
                    api_name="Near Earth Object",
                    api_description="NeoWs (Near Earth Object Web Service) is a RESTful web service for near earth Asteroid information. With NeoWs a user can: search for Asteroids based on their closest approach date to Earth, lookup a specific Asteroid with its NASA JPL small body id, as well as browse the overall data-set."
                    ).place_item()
        
        APIListItem(api_list.interior,
                    controller,
                    APOD
                    ).place_item()

class APIListItem(ListItem):
    def __init__(self, master, controller, handler_page, api_name="New API", api_description="Coming soon!", bg=NASA_GREY):
        super().__init__(master)

        HyperLabel(self,
                   api_name,
                   lambda : controller.show_frame(handler_page),
                   font=("Helvetica", 20),
                   wraplength=600
                   ).pack(anchor="nw", padx=2, pady=6)

        tk.Label(self,
                 text= api_description,
                 font=("Helvetica", 10),
                 wraplength=600,
                 justify="left",
                 bg=bg,
                 fg=NASA_LIGHT_GREY
                 ).pack(anchor="nw", padx=2)


class APIHint(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black")


app = MainApp()
app.mainloop()