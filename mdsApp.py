import tkinter as tk
from tkinter import ttk
import json

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

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
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

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

class displayWidget():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MDS")

        self.frames = []
        self.wcycle = []
        self.book = CustomNotebook(width=400, height=700)
        self.book.pack(side="top", fill="both", expand=True)

        self.create_tab()
        new_tab_button = tk.Button(self.book,text='+')
        new_tab_button.bind('<Button-1>',self.add_tab)
        new_tab_button.place(relx = 1, y=10, anchor='e')

        self.root.bind("<Tab>", lambda e: self.tab_cycle(e, False))
        self.root.bind("<Shift-Tab>", lambda e: self.tab_cycle(e, True))

        self.root.mainloop()

    def create_tab(self,*args):
        frame = ttk.Frame(self.book)

        name = '    '
        # change the name of the current tab
        tab_name_lbl = ttk.Label(frame, text='Ticket')
        tab_name_lbl.pack(side='top', padx=10)
        tab_name_entry = ttk.Entry(frame)
        tab_name_entry.pack(side='top', padx=10)
        # self.wcycle.append(tab_name_entry)
        for i in ("<FocusOut>","<Return>"):
            tab_name_entry.bind(i, lambda e: self.change_tab_name())

        # worknotes
        wn = ttk.Label(frame, text="Worknotes")
        wn.pack(side='top', padx=10)
        text_box = tk.Text(frame, height=5, width=30, wrap=tk.WORD)
        text_box.pack(side='top', padx=10, pady=10, fill='both', expand=True)
        # self.wcycle.append(text_box)        
        text_box.bind("<Tab>", lambda e: self.tab_cycle(e, False))
        text_box.bind("<Shift-Tab>", lambda e: self.tab_cycle(e, True))

        # MDS questions
        for q in config["questions"]:
            self.add_question(frame, q)
        
        # add the preview
        retrieve_button = tk.Button(frame, text="Copy to clipboard", command= self.get_all_text)
        retrieve_button.pack(side='top', padx=10, pady=10, fill='both', expand=True)

        # collect all wcycles and labels
        for widget in frame.winfo_children():
            if isinstance(widget, (tk.Text, ttk.Entry)):
                # Check if the widget is a Label or Entry
                self.wcycle.append(widget)

        # set columns to resize horizontally with window
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        # add the frame to the book
        self.book.add(frame,text=name)
        self.book.pack(side=tk.TOP)
        self.frames.append(frame)
        self.book.select(frame)

    def change_tab_name(self):
        cur_tab = self.book.index(self.book.select());
        self.book.tab(cur_tab, text=f'  {self.frames[cur_tab].winfo_children()[1].get()}  ')   

    def tab_cycle(self, event, shift):
        # Cycle focus through the specified widgets
        current_widget = event.widget.focus_get()

        if current_widget in self.wcycle:
            current_index = self.wcycle.index(current_widget)
            if not shift and current_index + 1 < len(self.wcycle):
                next_index = (current_index + 1) % len(self.wcycle)
                self.wcycle[next_index].focus_set()
            if shift and current_index - 1 >= 0:
                next_index = (current_index - 1) % len(self.wcycle)
                self.wcycle[next_index].focus_set()
        else:
            # If the focus is on a widget outside the cycle list, let Tkinter handle it
            event.widget.event_generate('<Tab>')

        return 'break'

    def add_tab(self, *args):
        self.create_tab()

    def add_question(self,root, q):
        lbl = ttk.Label(root, text=q["question"])
        lbl.pack(side='top', fill='x', anchor='w', padx=10)
        if len(q['default']) > 1:
            entry = ttk.Combobox(root)
            entry['values'] = q['default']
        else:
            entry = ttk.Entry(root)
            if len(q['default']) == 1:
                entry.insert(0,q['default']) 
        entry.pack(side='top', fill='x', expand=True, padx=10)
        
    def get_all_text(self):
        final = ''
        line_separator = "\n========================== MDS =========================="
        cur_tab = self.book.index(self.book.select());
        wcycle = []
        labels = []

        # collect all wcycles and labels in the tab
        for widget in self.frames[cur_tab].winfo_children():
            if isinstance(widget, (tk.Text, ttk.Entry)):
                # Check if the widget is a Label or Entry
                wcycle.append(widget)
            if isinstance(widget, ttk.Label):
                labels.append(widget.cget('text'))
        
        # Iterate through all widgets in the tab
        for lbl, txt in zip(labels, wcycle):
            if lbl == "Worknotes":
                final += f'\nL1/L2 Worknotes: \n'
                lines = txt.get("1.0", "end-1c").split('\n')
                lines = [f'{wn_style} {line.capitalize()}' if line else '\n' for line in lines]
                final += '\n'.join(lines).strip()
                final += line_separator
            elif lbl == "Ticket":
                final += f'======================= {txt.get()} ======================='
            else:
                t = (txt.get() if isinstance(txt, ttk.Entry) else txt.get("1.0", "end-1c")).strip()
                final += f' \n{ls_style} {lbl} {"n/a" if t == "" else t}'
        final+=line_separator
        
        self.root.clipboard_clear()
        self.root.clipboard_append(final)
        self.root.update()
        # print(final)

if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    ls_style = config['list-style']
    wn_style = config['work-notes-style']

    app = displayWidget()

