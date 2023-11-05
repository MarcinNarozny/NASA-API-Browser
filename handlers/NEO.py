import tkinter as tk
from gui import Page, ScrollList, ListItem, HyperLabel, NASA_GREY, NASA_LIGHT_GREY
import webbrowser
from handlers.handlers import HandlerNEO_Feed
from datetime import datetime


class NEO(Page):
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
                    end_date_entry.config(state= "disabled")

                case 1:
                    end_date_entry.config(state= "normal")
                    
                case _:
                    print("mode_error")
    
        def unpack(response_item):
            def apply_labels(parent,i,title,text):
                tk.Label(parent,
                         text=title,
                         justify="right",
                         bg=NASA_GREY,
                         fg="white",
                         font=("Helvetica", 12),
                         ).grid(sticky="ne", column=0, row=i)

                if 'url' in title:
                    HyperLabel(parent,
                               text=text,
                               justify="left",
                               bg=NASA_GREY,
                               wraplength=550,
                               font=("Helvetica", 12),
                               fg="blue",
                               command= lambda url=text: webbrowser.open(url)
                               ).grid(sticky="sw", column=1, row=i)
                        
                else:
                    tk.Label(parent,
                             text=str(text).replace("\n", ""),
                             wraplength=550,
                             justify="left",
                             bg=NASA_GREY,
                             fg=NASA_LIGHT_GREY,
                             font=("Helvetica", 12)
                             ).grid(sticky="sw", column=1, row=i)

            if "code" in response_item.keys():
                if response_item["code"] == 400:
                    controller.message.configure(text="ENTER VALID DATE (YYYY-MM-DD)")
                    return
            
            count_item = ListItem(content_list.interior)
            apply_labels(count_item, 0, "Asteroids: ", response_item["element_count"])
            count_item.place_item()

            for day in response_item["near_earth_objects"]:
                for object in response_item["near_earth_objects"][day]:
                    day_item = ListItem(content_list.interior)
                    apply_labels(day_item, 0, "Day: ", day)
                    apply_labels(day_item, 1, "Name: ",object["name"])
                    apply_labels(day_item, 2, "id: ",object["id"])
                    apply_labels(day_item, 3, "neo_id: ",object["neo_reference_id"])
                    apply_labels(day_item, 4, "absolute magnitude: ", object["absolute_magnitude_h"])
                    apply_labels(day_item, 5, "minimum diameter [m]: ", object["estimated_diameter"]["meters"]["estimated_diameter_min"])
                    apply_labels(day_item, 6, "maximum diameter [m]: ", object["estimated_diameter"]["meters"]["estimated_diameter_max"])
                    apply_labels(day_item, 7, "is it hazardous?: ", object["is_potentially_hazardous_asteroid"])
                    apply_labels(day_item, 8, "is it sentry? ", object["is_sentry_object"])
                    apply_labels(day_item, 9, "url: ", object["nasa_jpl_url"])
                    day_item.place_item()


        def search():   
            match selected_mode.get():
                case 0:
                    neo_feed.single_day_objects(start_date.get())

                case 1:
                    if (datetime.strptime(end_date.get(), "%Y-%m-%d") - datetime.strptime(start_date.get(), "%Y-%m-%d")).days > 99:
                        controller.message.configure(text="PLEASE CHOOSE CLOSER DATES")
                        return
                    neo_feed.date2date_objects(start_date.get(), end_date.get())
            
            unpack(neo_feed.response)


        today = datetime.now().strftime("%Y-%m-%d")
        start_date = tk.StringVar(value=today)
        end_date = tk.StringVar(value=today)

        mode_buttons_container = tk.Frame(self.controls_window, bg=NASA_GREY)
        mode_buttons_container.pack(side="left", padx=10, pady=10)

        mode_buttons_container.grid_rowconfigure(0, weight = 1)
        mode_buttons_container.grid_columnconfigure(0, weight = 1)

        modes = ("Single day","Range of days")

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

        enable_controls()

        neo_feed = HandlerNEO_Feed(api_id="neo/rest/v1/feed?")

        content_list = ScrollList(self.content_window)
         
        tk.Button(self.controls_window, text="Search", command = search).pack(side="bottom",padx=10,pady=10, fill="x", anchor="s")
        tk.Button(self.controls_window, text="Clear list", command = clear_list).pack(side="bottom",padx=10,pady=10, fill="x", anchor="s")