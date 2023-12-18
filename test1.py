print('hello im python')



from tkinter import ttk
from ttkthemes import ThemedTk

window = ThemedTk(theme="arc")
ttk.Button(window, text="Test", command=window.destroy).pack()
window.mainloop()
