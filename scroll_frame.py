import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("500x500")
root.title("Tkinter Notebook with Scrollbar")

cv1 = tk.Canvas(root)
cv1.pack(fill="both",expand=True,side="left")

# Create a scrollbar
scrollbar = ttk.Scrollbar(root, orient='vertical', command=cv1.yview)
scrollbar.pack(side="right",fill=tk.Y)
cv1.configure(yscrollcommand=scrollbar.set)
cv1.bind('<Configure>', lambda e: cv1.configure(scrollregion=cv1.bbox('all')))

sub_frame = tk.Frame(cv1)

for i in range(100):
    lbl = tk.Label(sub_frame, text="aaaaaaaaaaa")
    lbl.pack()

cv1.create_window((0,0), window=sub_frame, anchor='nw')

root.mainloop()


