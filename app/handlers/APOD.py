import tkinter as tk
from ..gui import Page, ScrollList, ListItem, HyperLabel, NASA_GREY, NASA_LIGHT_GREY
import webbrowser
from .handler import HandlerAPOD
from datetime import datetime


class APOD(Page):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        def leave_page():
            self.go_to_start()
            clear_list()

        def clear_list():
            for widget in content_list.interior.winfo_children():
                widget.destroy()

        tk.Button(self.controls_window, text="API List", command=leave_page).pack(anchor="n", fill="x")
        
        #####MODES#####

        def validate_date(P):
            P = P.replace("-", "")
            if len(P) == 0 or (len(P)<9 and P.isdigit()):
                return True
            
            else:
                return False

        def validate_number(P):
            if len(P) == 0 or (P.isdigit() and len(P)<=2):
                return True

            else:
                return False

        def add_hyphens(event):
            if event.keysym not in ("Left", "Right"):
                current_text = event.widget.get()
                current_text = ''.join(filter(str.isdigit, current_text))
                if len(current_text) > 4 and len(current_text) < 7:
                    current_text = '-'.join([current_text[0:4],current_text[4:]])
                elif len(current_text) > 6:
                    current_text = '-'.join([current_text[0:4],current_text[4:6],current_text[6:]])
                event.widget.delete(0, "end")
                event.widget.insert(0, current_text)
        
        def enable_controls():
            match selected_mode.get():
                case 0:
                    start_date_entry.config(state= "normal")
                    end_date_entry.config(state= "disabled")
                    random_entry.config(state= "disabled")
                case 1:
                    start_date_entry.config(state= "normal")
                    end_date_entry.config(state= "normal")
                    random_entry.config(state= "disabled")
                case 2:
                    start_date_entry.config(state= "disabled")
                    end_date_entry.config(state= "disabled")
                    random_entry.config(state= "normal")
                case _:
                    print("mode_error")
                    
        def unpack(response_item):
            if "code" in response_item.keys():
                if response_item["code"] == 400:
                    controller.message.configure(text="ENTER VALID DATE (YYYY-MM-DD)")
                    return
            
            item_background = ListItem(content_list.interior)
            item_background.place_item()
  
            for i,k in enumerate(response_item):
                tk.Label(item_background,
                         text=str(k).replace('_', ' ')+" -",
                         justify="right",
                         bg=NASA_GREY,
                         fg="white",
                         font=("Helvetica", 12),
                         ).grid(sticky="ne", column=0, row=i)
                if 'url' in k:
                    HyperLabel(item_background,
                               text=response_item[k],
                               justify="left",
                               bg=NASA_GREY,
                               wraplength=550,
                               font=("Helvetica", 12),
                               fg="blue",
                               command= lambda url=response_item[k]: webbrowser.open(url)
                               ).grid(sticky="sw", column=1, row=i)
                else:
                    tk.Label(item_background,
                             text=str(response_item[k]).replace("\n", ""),
                             wraplength=550,
                             justify="left",
                             bg=NASA_GREY,
                             fg=NASA_LIGHT_GREY,
                             font=("Helvetica", 12)
                             ).grid(sticky="sw", column=1, row=i)
                
        def search():   
            match selected_mode.get():
                case 0:
                    apod.single_day_image(start_date.get())
                case 1:
                    if (datetime.strptime(end_date.get(), "%Y-%m-%d") - datetime.strptime(start_date.get(), "%Y-%m-%d")).days > 99:
                        controller.message.configure(text="PLEASE CHOOSE CLOSER DATES")
                        return
                    apod.date2date_images(start_date.get(), end_date.get())
                case 2:
                    apod.random_images(how_many_random.get()) 

            if type(apod.response)==list:
                for item in apod.response:
                    unpack(item)
            else:
                unpack(apod.response)


        today = datetime.now().strftime("%Y-%m-%d")
        start_date = tk.StringVar(value=today)
        end_date = tk.StringVar(value=today)
        how_many_random = tk.IntVar(value=1)

        mode_buttons_container = tk.Frame(self.controls_window, bg=NASA_GREY)
        mode_buttons_container.pack(side="left", padx=10, pady=10)

        mode_buttons_container.grid_rowconfigure(0, weight = 1)
        mode_buttons_container.grid_columnconfigure(0, weight = 1)

        modes = ("Single day","Range of days","Random images")

        selected_mode = tk.IntVar(value=0)

        for i,mode in enumerate(modes):
            tk.Radiobutton(mode_buttons_container,
                           text=mode,
                           variable=selected_mode,
                           value=i,
                           indicatoron=False,
                           width=20,
                           command=enable_controls,
                           fg= "black",
                           selectcolor=NASA_LIGHT_GREY,
                           ).grid(padx=10, pady=10, row=i, column=0)

        inputs_container = tk.Frame(self.controls_window, bg=NASA_GREY)
        inputs_container.pack(side="left", padx=10, pady=10)

        date_validation = (inputs_container.register(validate_date), '%P') 
        number_validation = (inputs_container.register(validate_number), '%P') 

        tk.Label(inputs_container, text="from:", bg=NASA_GREY, fg= NASA_LIGHT_GREY).grid(row=0, column=0, padx=10, pady=10)
        start_date_entry = tk.Entry(inputs_container,
                                    width=10,
                                    textvariable=start_date,
                                    validate="key",
                                    validatecommand=date_validation)
        start_date_entry.grid(row=0, column=1, padx=10, pady=10)
        start_date_entry.bind("<KeyRelease>", add_hyphens)

        tk.Label(inputs_container, text="until:", bg=NASA_GREY, fg= NASA_LIGHT_GREY).grid(row=1, column=0, padx=10, pady=10)
        end_date_entry = tk.Entry(inputs_container,
                                  width=10,
                                  textvariable=end_date,
                                  validate="key",
                                  validatecommand=date_validation)
        end_date_entry.grid(row=1, column=1, padx=10, pady=10)
        end_date_entry.bind("<KeyRelease>", add_hyphens)

        tk.Label(inputs_container, text="amount:", bg=NASA_GREY, fg= NASA_LIGHT_GREY).grid(row=2, column=0, padx=10, pady=10)
        random_entry = tk.Entry(inputs_container,
                                width=10,
                                textvariable=how_many_random,
                                validate="key",
                                validatecommand=number_validation)
        random_entry.grid(row=2, column=1, padx=10, pady=10)

        enable_controls()

        apod = HandlerAPOD(api_id="planetary/apod?")
        content_list = ScrollList(self.content_window)
         
        tk.Button(self.controls_window, text="Search", command = search).pack(side="bottom",padx=10,pady=10, fill="x", anchor="s")
        tk.Button(self.controls_window, text="Clear list", command = clear_list).pack(side="bottom",padx=10,pady=10, fill="x", anchor="s")