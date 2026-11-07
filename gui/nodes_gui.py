#
'''

'''


import tkinter as tk

from cust_logging.logger import Log
Log = Log('nodes_gui.py')

# nodes gui
'''
    print the nodes
'''
def display_nodes_gui(nodes):

    new_root = tk.Toplevel()
    new_root.geometry('900x600')

    # 1. Create Canvas
    canvas = tk.Canvas(new_root)
    canvas.pack(fill=tk.BOTH, expand=True)

    text = tk.Text(canvas, width=900, height=600)
    text.pack(fill=tk.BOTH, expand=True)

    # 5. Add Labels to the Frame
    for i in sorted(nodes, key=lambda x: x.get()['title']):
        text.insert(tk.END, f"\"{i.get()['title']}\" {i.get()['url']}\n\n")
