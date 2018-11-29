import tkinter as tk

################### functions #############################
# defining a function that will close the window
def close():
    exit()

# open a window that lets you input nutrition requirements
def open_nutr_req_window():
    nutr_req_win.mainloop()

###########################################################

###########################################################
# define the window that lets you input nutrition requirements
###########################################################
nutr_req_win = tk.Tk()
nutr_req_win.title ('menu_maker: daily nutrition goals')
nutr_req_win.geometry("400x300")

##### instruction message #####
instruction = tk.Label(nutr_req_win, text="Please input your daily nutrition goals", fg='blue', font='helvetica')
instruction.grid(row=0, column=1)

##### quit button #####
# creating a button instance
finishedButton = tk.Button(nutr_req_win, text='Done', font='helvetica', command=close)
# placing the quit button on my window (top left)
finishedButton.grid(row=0, column=0)

###########################################################
# define the main window
###########################################################

##### open the main window #####
root = tk.Tk()
# give the main window a title
root.title ('menu_maker')
# set the main window's size
root.geometry("400x300")

##### quit button #####
# creating a button instance
quitButton = tk.Button(root, text='Exit', font='helvetica', command=close)
# placing the quit button on my window (top left)
quitButton.grid(row=0, column=0)

##### welcome message #####
welcome = tk.Label(root, text="Welcome to menu_maker!", fg='blue', font='helvetica')
welcome.grid(row=0, column=1)

##### define nutr_reqs button #####
# creating a button instance
nutr_rec_button = tk.Button(root, text='Input nutrition requirements', font='helvetica', command=open_nutr_req_window)
# placing the button on my window 
# nutr_rec_button.place(x=50, y=50)
nutr_rec_button.grid(row=2, column=1)

##### initiate main window instance #####
root.mainloop()
