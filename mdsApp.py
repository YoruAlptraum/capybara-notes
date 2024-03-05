import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import json
import ctypes as ct
import datetime
import os

class CustomNotebook(ttk.Notebook):
    # A ttk Notebook with close buttons on each tab

    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.inc_tabs = []
        self.__initialize_custom_style()

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        new_tab_button = tk.Button(self,text='+', background=bg_color, foreground=txt_color, activebackground=bg_color, activeforeground=txt_color)
        new_tab_button.bind('<Button-1>',self.add_tab)
        new_tab_button.place(relx = 1, y=10, anchor='e')
        self.add_tab()
        self.root.bind('<Control-n>',self.add_tab)
        self.root.bind('<Control-t>', self.add_tab)

        self.root.bind("<Control-s>", self.save)
        self.root.bind("<Control-w>", lambda e: self.delete_tab(self.index("current")) if self.index("end") != 0 else print("nothing open"))
        
        self.root.bind("<Control-Prior>", self.previous_tab)
        self.root.bind("<Control-Next>", self.next_tab)

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def save(self, e=None):
        if self.index("end") != 0:
            self.inc_tabs[self.index("current")].copy_to_clipboard()

    def delete_tab(self, index):
        if index >= 0:
            self.inc_tabs[index].unbind_and_delete()
            self.inc_tabs.pop(index)
            self.event_generate("<<NotebookTabClosed>>")

    def on_close_press(self, event):
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        if not self.instate(['pressed']):
            # if not closing the tab set focus to tab name entry
            try:
                cur_ind = self.index("@%d,%d" % (event.x, event.y))
                self.inc_tabs[cur_ind].tab_name_entry.focus_set()
            except:
                print("no tabs")
                pass
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.delete_tab(index)

        self.state(["!pressed"])
        self._active = None

    def on_close(self):
        for tab in self.inc_tabs:
            tab.unbind_and_delete()

    def add_tab(self, *args):
        tab = ticket_tabs(self, self.root)
        self.inc_tabs.append(tab)
        tab.tab_name_entry.focus_set()
        return "break"

    def previous_tab(self, e):
        ind = (self.index("current") - 1)%self.index("end")
        self.inc_tabs[ind].tab_name_entry.focus_set()
        self.inc_tabs[ind].change_tab_name()
        self.select(ind)
    
    def next_tab(self, e):
        ind = (self.index("current") + 1)%self.index("end")
        self.inc_tabs[ind].tab_name_entry.focus_set()
        self.inc_tabs[ind].change_tab_name()
        self.select(ind)

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
        )
        if theme in style.theme_names():
            style.theme_use()
        else:
            self.root.option_add("*TCombobox*Listbox*Background", bg_color)
            self.root.option_add("*TCombobox*Listbox*Foreground", txt_color)
            style.theme_create(theme, parent="alt", settings={
                    "CustomNotebook": {
                        "configure": {
                            "background" : bg_color,
                            "bordercolor": txt_color,
                        },
                    },
                    "CustomNotebook.Tab": {
                        "configure": {
                            "background" : bg_color,
                            "foreground" : txt_color,
                            "focuscolor" : field_color,
                            "bordercolor": txt_color,
                        },
                    },
                    'TFrame': {
                        'configure': {
                            'background': bg_color,
                        }
                    },
                    'TLabel': {
                        'configure': {
                            'background': bg_color,
                            'foreground' : txt_color
                        }
                    },
                    'TScrollbar': {
                        'configure': {
                            'background  ': bg_color,
                            'troughcolor ': bg_color,
                            'arrowcolor ' : txt_color,
                            'bordercolor  ': txt_color
                        }
                    },
                    'TButton': {
                        'configure': {
                            'background  ': bg_color,
                            'foreground' : txt_color,
                            'fieldbackground ': field_color,
                            'bordercolor ': bg_color,
                            'insertcolor ': txt_color,
                        }
                    },
                    'TEntry': {
                        'configure': {
                            'background  ': bg_color,
                            'foreground' : txt_color,
                            'fieldbackground ': field_color,
                            'bordercolor ': bg_color,
                            'insertcolor ': txt_color,
                            'selectbackground ': highlight,
                            'selectforeground ': txt_color,
                        }
                    },
                    'TCombobox': {
                        'configure': {
                            'background  ': bg_color,
                            'foreground' : txt_color,
                            'fieldbackground ': field_color,
                            'selectbackground ': highlight,
                            'selectforeground ': txt_color,
                            'bordercolor ': bg_color,
                            'insertcolor ': txt_color,
                            'arrowcolor' : txt_color,
                        }
                    },
                    '*TCombobox*.Listbox.background': {
                        'configure': {
                            'background': bg_color
                        }
                    }
            })

            style.theme_use(theme)

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
        style.configure('CustomNotebook.Tab', font=custom_font) 

class CustText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.undo_stack = []
        self.redo_stack = []

class CustEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.undo_stack = []
        self.redo_stack = []

class CustCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.undo_stack = []
        self.redo_stack = []

class ticket_tabs():
    def __init__(self, book, root):
        self.book = book
        self.root = root
        self.book.pack(side="top", fill="both", expand=True)
        self.wcycle = []
        self.main_frame = ttk.Frame(book)

        self.book.add(self.main_frame,text="        ")

        # create the scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical')
        scrollbar.pack(side="right",fill=tk.Y,expand=False)
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0,
                               yscrollcommand=scrollbar.set, background=bg_color)

        self.canvas.pack(side="left",fill="both",expand=True)
        scrollbar.config(command=self.canvas.yview)

        self.sub_frame = ttk.Frame(self.canvas)
        self.sub_frame.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.sub_frame_id = self.canvas.create_window((0,0), window=self.sub_frame, anchor='nw')

        # Change font family
        self.sub_frame.option_add("*Font", custom_font)

        # change the name of the current tab
        tab_name_lbl = ttk.Label(self.sub_frame, text='Ticket')
        tab_name_lbl.pack(side='top', padx=10)
        self.tab_name_entry = CustEntry(self.sub_frame)
        self.tab_name_entry.pack(side='top', padx=10)
        # bind events
        self.previous_focus_widget = None
        self.main_frame.bind('<FocusIn>', self.on_focus_in)
        for i in ("<FocusOut>","<Return>"):
            self.tab_name_entry.bind(i, lambda e: self.change_tab_name())

        # add the content for the tab
        if worknotes_below:
            for q in config["questions"]:
                self.add_question(self.sub_frame, q)
            self.add_worknotes()
        else:
            self.add_worknotes()            
            for q in config["questions"]:
                self.add_question(self.sub_frame, q)

        # retrieve text button
        retrieve_button = tk.Button(self.sub_frame, text=copy_btn_lbl,  command= self.copy_to_clipboard, background=bg_color, foreground=txt_color, activebackground=bg_color, activeforeground=txt_color)
        retrieve_button.pack(side='top', padx=10, pady=10, fill='both', expand=True)

        self.root.bind("<Tab>", lambda e: self.tab_cycle(e, False))
        self.root.bind("<Shift-Tab>", lambda e: self.tab_cycle(e, True))
        # list wcycles on tab
        for widget in self.sub_frame.winfo_children():
            if isinstance(widget, (tk.Text, ttk.Entry, ttk.Combobox)):
                # Check if the widget is a Label or Entry
                self.wcycle.append(widget)
                self.bind_undo_redo(widget)

        self.book.select(self.main_frame)

    def add_question(self,root, q):
        lbl = ttk.Label(root, text=q["question"])
        lbl.pack(side='top', fill='x', anchor='w', padx=10)
        if len(q['default']) > 1:
            entry = CustCombobox(root)
            entry['values'] = q['default']
        else:
            entry = CustEntry(root)
            if len(q['default']) == 1:
                entry.insert(0,q['default']) 
        entry.pack(side='top', fill='x', expand=True, padx=10)

    def add_worknotes(self):
        wn = ttk.Label(self.sub_frame, text=worknotes_lbl)
        wn.pack()
        self.text_box = CustText(
                self.sub_frame, 
                height=worknotes_height,
                wrap=tk.WORD, 
                background=field_color, 
                foreground=txt_color, 
                insertbackground=txt_color,
                selectbackground=highlight,
                selectforeground=txt_color
            )
        self.text_box.pack(side='top',  padx=10, pady=10, fill='both', expand=True)
        self.text_box.bind("<Tab>", lambda e: self.tab_cycle(e, False))
        self.text_box.bind("<Shift-Tab>", lambda e: self.tab_cycle(e, True))
        
        self.text_box.bind('<Control-t>', self.book.add_tab)

    def get_all_text(self) -> str:
        final = ''
        labels = []
        line_separator = f'{line_separator_style} {self.tab_name_entry.get()} {line_separator_style}\n'

        # collect all labels in the tab
        for widget in self.sub_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                labels.append(widget.cget('text'))
        
        # Iterate through all widgets in the tab
        for lbl, txt in zip(labels, self.wcycle):
            if lbl == worknotes_lbl:
                final += f'{line_separator}'
                final += f'L1/L2 {worknotes_lbl}: \n'
                lines = txt.get("1.0", "end-1c").split('\n')
                lines = [f'{worknotes_style} {line.capitalize()}' if line else '\n' for line in lines]
                final += '\n'.join(lines).strip()
                final += f'\n{line_separator}'
            elif lbl == "Ticket":
                pass
            else:
                t = (txt.get() if isinstance(txt, ttk.Entry) else txt.get("1.0", "end-1c")).strip()
                final += f'{list_style} {lbl} {"n/a" if t == "" else t} \n'
        if worknotes_below:
            final = line_separator + final
        else:
            final += line_separator
        return final

    def copy_to_clipboard(self):
        self.save_to_file()
        self.book.clipboard_clear()
        self.book.clipboard_append(self.get_all_text())
        self.book.update()

    def save_to_file(self):
        save_folder_path = os.path.expandvars(config['save-folder-path'])
        if not save_folder_path:
            save_folder_path = "notes"
        self.create_folder_if_not_exists(save_folder_path)
        file_path = f'{save_folder_path}\{datetime.date.today()}.txt' 
        print(file_path)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"\n{datetime.datetime.now().strftime('%m-%d %H:%M:%S')}\n\n")
            file.write(self.get_all_text())

    def create_folder_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        #     print(f"'{folder_path}' created.")
        # else:
        #     print(f"'{folder_path}' already exists.")

    def on_focus_in(self, event):
        # Update the previous focus widget during FocusIn event
        self.previous_focus_widget = event.widget
    
    def change_tab_name(self):
        # check if there is a previous focus widget and change its name
        # this changes the name of the tab where the focus exited
        if self.previous_focus_widget:
            ind = self.book.index(self.previous_focus_widget)
            self.book.tab(ind, text=f'  {self.book.inc_tabs[ind].tab_name_entry.get()}  ')

    def bind_undo_redo(self, widget):
        widget.bind("<Control-z>", self.undo)
        widget.bind("<Control-y>", self.redo)

        widget.bind("<space>", self.stack_undo)
        widget.bind("<Control-v>", self.stack_undo)
        widget.bind("<Control-x>", self.stack_undo)
        widget.bind("<BackSpace>", self.stack_undo)
        widget.bind("<Delete>", self.stack_undo)
        widget.bind("<Return>", self.stack_undo)

    def undo(self, event):
        widget = event.widget
        if widget.undo_stack:
            text = widget.undo_stack.pop()
            if isinstance(widget, tk.Text):
                widget.redo_stack.append(widget.get("1.0", "end-1c"))
                widget.delete("1.0", "end-1c")
                widget.insert("1.0", text)
            else:
                widget.redo_stack.append(widget.get())
                widget.delete(0, tk.END)
                widget.insert(0, text)
        elif isinstance(widget, tk.Text):
            if isinstance(widget, tk.Text):
                widget.redo_stack.append(widget.get("1.0", "end-1c"))
            else:
                widget.redo_stack.append(widget.get())
            widget.delete("1.0","end-1c")
        else:
            if isinstance(widget, tk.Text):
                widget.redo_stack.append(widget.get("1.0", "end-1c"))
            else:
                widget.redo_stack.append(widget.get())
            widget.delete(0,tk.END)

    def redo(widget, event):
        widget = event.widget
        if widget.redo_stack:
            ind = widget.index("insert")
            text = widget.redo_stack.pop()
            if isinstance(widget, tk.Text):
                widget.undo_stack.append(widget.get("1.0", "end-1c"))
                widget.delete("1.0", "end-1c")
                widget.insert("1.0", text)
            else:
                widget.undo_stack.append(widget.get())
                widget.delete(0, tk.END)
                widget.insert(0, text)

    def stack_undo(widget, event):
        widget = event.widget
        if isinstance(widget, tk.Text):
            widget.undo_stack.append(widget.get("1.0", "end-1c"))
        else:
            widget.undo_stack.append(widget.get())
        widget.redo_stack.clear()

    def _configure_interior(self,event):
        # update the scrollbars to match sub frame size
        size = (self.sub_frame.winfo_reqwidth(), self.sub_frame.winfo_reqheight())
        self.canvas.config(scrollregion=(0,0,size[0],size[1]))
        if self.sub_frame.winfo_reqwidth() != self.sub_frame.winfo_width():
            # update canvas width to fit sub frame
            self.canvas.config(width=self.sub_frame.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.sub_frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update sub frame's width to fill canvas
            self.canvas.itemconfigure(self.sub_frame_id, width=self.canvas.winfo_width())

    def tab_cycle(self, event, shift):
        # Cycle focus through the specified widgets
        current_widget = event.widget.focus_get() 
        wcycle = self.book.inc_tabs[self.book.index("current")].wcycle

        if current_widget in wcycle:
            current_index = wcycle.index(current_widget)
            cycle = len(wcycle)
            if not shift and current_index + 1 < cycle:
                next_index = (current_index + 1)
                wcycle[next_index].focus_set()
            if shift and current_index > 0:
                next_index = (current_index - 1)
                wcycle[next_index].focus_set()

        return 'break'

    def unbind_and_delete(self):
        # Unbind all events from each widget in sub frame and destroy it
        for widget in self.sub_frame.winfo_children():
            for e in widget.bind():
                widget.unbind(e)
            #     print(e)
            # print(widget)
            widget.destroy()

        self.sub_frame.unbind('<Configure>')
        self.sub_frame.destroy()
        self.canvas.unbind('<Configure>')
        self.canvas.destroy()

        # Unbind all events from each widget in main frame and destroy it
        for widget in self.main_frame.winfo_children():
            for e in widget.bind():
                widget.unbind(e)
            widget.destroy()

        self.main_frame.unbind('<FocusIn>')
        self.main_frame.destroy()

class app():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.title(app_name)
        self.root.iconbitmap(icon_path)
        self.book = CustomNotebook(self.root, width=400, height=700)

        self.root.bind('<Control-BackSpace>', self.entry_backspace_word)
        self.root.bind('<Control-Delete>', self.entry_delete_word)

        self.book.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # title border darkmode let's gooooooooooooooooooo
        if dark_mode or theme == 'ozw':
            self.root.update()
            set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ct.windll.user32.GetParent
            hwnd = get_parent(self.root.winfo_id())
            value = 2
            value = ct.c_int(value)
            set_window_attribute(hwnd, 20, ct.byref(value),4)
            
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def entry_backspace_word(self,event):
        w = event.widget
        if isinstance(w, ttk.Entry):
            current_pos = w.index(tk.INSERT)
            
            # Find the position of the last space before the current insertion cursor
            start_pos = w.get()[:current_pos].rfind(' ') +1

            # If no space is found, consider the start of the entry
            if start_pos == -1:
                start_pos = 0

            # Delete the text from the last space to the current insertion cursor
            w.delete(start_pos, current_pos)
        else: 
            line, ind = w.index("insert").split('.')
            txt = w.get(f"{line}.0",f"{line}.end")
            
            start_pos = txt[:(int(ind) - 1)].rfind(' ') + 1
            if start_pos == -1:
                start_pos = 0

            w.delete(f"{line}.{start_pos}", f"{line}.{ind}")

        return 'break'

    def entry_delete_word(self, event):
        w = event.widget
        if isinstance(w, ttk.Entry):
            current_pos = w.index(tk.INSERT)
            
            # Find the position of the last space before the current insertion cursor
            end_pos = w.get()[current_pos:].find(' ') 

            # If no space is found, consider the end of the w
            if end_pos == -1:
                end_pos = w.index(tk.END)
            else:
                end_pos += current_pos

            # Delete the text from the last space to the current insertion cursor
            w.delete(current_pos, end_pos)
        else:
            w = event.widget
            line, ind = w.index("insert").split('.')
            txt = w.get(f"{line}.0",f"{line}.end")
            ind = int(ind)

            rel = txt[(ind + 1):].find(' ')

            if rel == -1:
                end_pos = w.index("end-1c").split('.')[1]
            else:
                end_pos = ind + rel + 1

            w.delete(f"{line}.{ind}", f"{line}.{end_pos}")

        return 'break'  # Prevent default behavior (e.g., inserting a character)

    def on_close(self):
        # Destroy widgets before closing the main window
        self.book.on_close()
        for bind in self.root.bind():
            self.root.unbind(bind)
        self.root.destroy()
    
if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    app_name = config['app-name']
    icon_path = config['icon-path']
    worknotes_lbl = config["worknotes-lbl"]
    worknotes_height = config["worknotes-height"]
    worknotes_style = config['worknotes-style']
    list_style = config['list-style']
    line_separator_style = config['line-separator-style']
    worknotes_below = config['worknotes-below']
    copy_btn_lbl = config['copy-btn-lbl']
    dark_mode = config['dark-window']

    font_size = config['font-size']
    font_family = config['font-family']

    custom_font = (font_family, font_size) 

    theme = config['theme']
    if theme == 'ozw':   
        bg_color = '#222'
        field_color = '#111'
        txt_color = '#2afc98'
        highlight = '#2979ff'
    else:
        bg_color = config['bg-color']
        field_color = config['field-color']
        txt_color = config['text-color']
        highlight = config['highlight']

    app = app()

