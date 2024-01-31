import tkinter as tk
from tkinter import ttk
import json

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    def __init__(self, *args, **kwargs):
        self.__initialize_custom_style()
        self.inc_tabs = []

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        new_tab_button = tk.Button(self,text='+')
        new_tab_button.bind('<Button-1>',self.add_tab)
        new_tab_button.place(relx = 1, y=10, anchor='e')
        self.add_tab()

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            # unbind and delete all widgets on tab
            self.inc_tabs[index].unbind_and_delete()
            self.inc_tabs.pop(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def on_close(self):
        for tab in self.inc_tabs:
            tab.unbind_and_delete()

    def add_tab(self, *args):
        tab = ticket_tabs(self)
        self.inc_tabs.append(tab)

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                ''')
        )

        style.element_create("close", "image", "img_close", border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

class app():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x700')
        self.root.title("MDS")
        self.book = CustomNotebook(width=400, height=700)
        self.book.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        # Destroy widgets before closing the main window
        self.book.on_close()
        self.root.destroy()

class ticket_tabs():
    def __init__(self, book):
        self.book = book
        self.book.pack(side="top", fill="both", expand=True)
        self.wcycle = []
        self.main_frame = ttk.Frame(book)

        self.book.add(self.main_frame,text="    ")

        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.canvas.pack(fill="both",expand=True,side="left")
        # create the scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side="right",fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.sub_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.sub_frame, anchor='nw')
        
        # change the name of the current tab
        tab_name_lbl = ttk.Label(self.sub_frame, text='Ticket')
        tab_name_lbl.pack(side='top', padx=10)
        self.tab_name_entry = ttk.Entry(self.sub_frame)
        self.tab_name_entry.pack(side='top', padx=10)
        # bind events
        self.previous_focus_widget = None
        self.main_frame.bind('<FocusIn>', self.on_focus_in)
        for i in ("<FocusOut>","<Return>"):
            self.tab_name_entry.bind(i, lambda e: self.change_tab_name())        

        # add the content for the tab
        # worknotes
        wn = ttk.Label(self.sub_frame, text="Worknotes")
        wn.pack()
        text_box = tk.Text(self.sub_frame, wrap=tk.WORD)
        text_box.pack(side='top', padx=10, pady=10, fill='both', expand=True)
        # text_box.bind("<Tab>", lambda e: self.tab_cycle(e, False))
        # text_box.bind("<Shift-Tab>", lambda e: self.tab_cycle(e, True))







        for i in range(30):
            filling = tk.Label(self.sub_frame,text="aaaaaaaaaaaa")
            filling.pack()


            

    def on_focus_in(self, event):
        # Update the previous focus widget during FocusIn event
        self.previous_focus_widget = event.widget
    
    def change_tab_name(self):
        # check if there is a previous focus widget and change its name
        # this changes the name of the tab where the focus exited
        if self.previous_focus_widget:
            ind = self.book.index(self.previous_focus_widget)
            self.book.tab(ind, text=f'  {self.book.inc_tabs[ind].tab_name_entry.get()}  ')
        


    def unbind_and_delete(self):
        # Unbind all events from widgets in the frame
        for widget in self.sub_frame.winfo_children():
            widget.unbind_all('<Event>')  # Replace '<Event>' with the specific event you want to unbind

        # Destroy all widgets in the frame
        for widget in self.sub_frame.winfo_children():
            widget.destroy()

        # Destroy the frame itself
        self.sub_frame.destroy()
        self.canvas.destroy()
        self.main_frame.destroy()




        


if __name__ == "__main__":
    with open('config/config.json', 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    ls_style = config['list-style']
    wn_style = config['work-notes-style']

    app = app()

