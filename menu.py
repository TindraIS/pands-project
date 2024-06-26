'''
Name: menu.py

Author: Irina Simoes

Description: This file contains a module with the function that computes the GUI with tkinter when analysis.py is run.

'''

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import os
import tools

#____________________________ OPENING MENU ____________________________

def closing_window(root):
    '''
    This function ensures the program exits completely after closing tkinter GUI, without triggering an error.
    https://stackoverflow.com/questions/110923/how-do-i-close-a-tkinter-window
    https://stackoverflow.com/questions/67421583/python-tkinter-window-dont-close-with-root-quit-when-using-os-system
    https://stackoverflow.com/questions/9591350/what-is-difference-between-sys-exit0-and-os-exit0
    https://docs.python.org/3/library/os.html#os._exit
    '''
    if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
        root.destroy()
        os._exit(os.EX_OK) # EX_OK code passed to specify that no error occurred, making this function preferred over sys_exit() 
                          # which raises an exception

def opening_menu(username, df, df_cleaned):
    '''
    This function computes a GUI using the tkinter library, displaying four clickable analysys options. Each of the
    options trigger a different function from tools.py: getting a descriptive summary, identifying and 
    handling outliers, generating pair scatter plots, generating histograms, and compuTe PCA. 
    https://www.geeksforgeeks.org/popup-menu-in-tkinter/
    https://www.geeksforgeeks.org/tkinter-cheat-sheet/
    '''

    # Create the main window
    root = tk.Tk()
    root.title("PETALIST || Iris Dataset Analysis")

    # Handle the menu close event gracefully
    # https://stackoverflow.com/questions/110923/how-do-i-close-a-tkinter-window
    root.protocol("WM_DELETE_WINDOW", lambda: closing_window(root))

    # Load image
    folder = 'images'
    file_name = 'menu_background.png'
    file_path = os.path.join(os.getcwd(), folder, file_name)
    image = tk.PhotoImage(file=file_path)
    image = image.subsample(2, 2)  # Resize by a factor of 2 in both dimensions

    # Create a label to display the image
    image_label = tk.Label(root, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window with the image

    # Create Font object
    # https://pythonexamples.org/python-tkinter-button-change-font/
    # https://www.geeksforgeeks.org/tkinter-fonts/
    font_buttons = font.Font(family='Sitka Small', size=8, weight="bold")
    font_options = font.Font(family='Sitka Small', size=8)
    font_label_heading = font.Font(family='Sitka Small', size=26, weight="bold")
    font_label_text = font.Font(family='Sitka Small', size=10)

    # Create labels for text
    label1 = tk.Label(root, 
                      fg="#5E7F73", bg="white", 
                      text=f"Hello {username},", 
                      font=font_label_heading)
    label1.place(relx=0.50, rely=0.3, anchor="sw")
    label2 = tk.Label(root, 
                      fg="#5E7F73", bg="white", 
                      text="Welcome to Petalist, the Iris dataset analysis \nprogram. Please select one of the options below:", 
                      font=font_label_text, anchor='w')
    label2.place(relx=0.50, rely=0.4, anchor="sw")
    
    # Create buttons
    # Colours: https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
    # https://stackoverflow.com/questions/70406400/understanding-python-lambda-behavior-with-tkinter-button
    # https://tk-tutorial.readthedocs.io/en/latest/button/button.html
    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/button.html

    # Define buttons configurations
    button_height = 1
    button_width = 30
    button_anchor = "w"
    button_justify = "left"
    button_bg = "#5E7F73"
    button_fg = "white"

    # Call button functions
    button_1(root,df,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons)
    button_2(root,df,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons,font_options)
    button_3(root,df,df_cleaned,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons)
    button_4(root,df,df_cleaned,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons)
    button_5(root,df,df_cleaned,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons)

    # Maximize the window
    root.state('zoomed')

    # Run the main event loop
    root.mainloop()


#____________________________ OPENING MENU BUTTONS ____________________________

def button_1(root,df,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons):
    '''
    This function is part of the GUI setup in the opening_menu function, creating and configuring a button within the menu. 
    When clicked, it triggers the descriptive_summary function from the tools module, which performs a descriptive summary 
    of the DataFrame.
    '''

    button1 = tk.Button(root, 
                    text=" I .get descriptive summary", 
                    command=lambda: tools.descriptive_summary(df),
                    width=button_width, 
                    height=button_height, 
                    anchor=button_anchor, 
                    justify=button_justify, 
                    bg=button_bg, 
                    fg=button_fg)
    button1.place(relx=0.60, rely=0.5, anchor="center")  
    button1['font'] = font_buttons

def button_2(root,df,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons,font_options):
    '''
    This function is part of the GUI setup in the opening_menu function, creating and configuring a button within the menu. 
    This option menu allows the user to choose between summarizing outliers or removing them from the dataset. When an option 
    is selected, the corresponding function from the tools module is triggered. 
    '''

    # Create the list of options & a dictionary mapping options to their respective functions
    options_list = ["Get a summary of outliers", "Remove outliers from the dataset"] 
    option_functions = {
        "Get a summary of outliers": tools.outliers_summary,
        "Remove outliers from the dataset": tools.outliers_cleanup
        }
    
    # Variable to keep track of the option selected in tk.OptionMenu() & set the default value of the variable
    value_inside = tk.StringVar(root,"II .identify & handle outliers") 
    
    # Create the optionmenu widget and passing the options_list and value_inside to it 
    # https://www.geeksforgeeks.org/how-to-change-background-color-of-tkinter-optionmenu-widget/
    button2 = tk.OptionMenu(root, value_inside, *options_list) 
    button2['font'] = font_buttons
    button2.place(relx=0.60, rely=0.6, anchor="center")  

    # Se the background color of Options Menu & displayed options
    button2.config(width=23, 
                   height=button_height, 
                   anchor=button_anchor, 
                   justify=button_justify, 
                   bg=button_bg, 
                   fg=button_fg)
    button2["menu"].config(bg="#7A9F92",fg='white',font=font_options)

    # Configure the OptionMenu to call the appropriate function when an option is selected
    for option in options_list:
        button2["menu"].entryconfig(option, command=lambda opt=option: option_functions[opt](df))

def button_3(root,df,df_cleaned,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons):
    '''
    This function is part of the GUI setup in the opening_menu function, creating and configuring a button within the menu. 
    When clicked, it triggers the generate_pairplot_options function from the tools module, which prompts the user to choose 
    whether to create a scatter pair plot with or without ouliers.
    '''
        
    button3 = tk.Button(root, 
                        text="III .generate pair scatter plot", 
                        command=lambda: tools.generate_pairplot_options(df,df_cleaned),
                        width=button_width, 
                        height=button_height, 
                        anchor=button_anchor, 
                        justify=button_justify, 
                        bg=button_bg, 
                        fg=button_fg)
    button3.place(relx=0.60, rely=0.7, anchor="center") 
    button3['font'] = font_buttons

def button_4(root,df,df_cleaned,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons):
    '''
    This function is part of the GUI setup in the opening_menu function, creating and configuring a button within the menu. 
    When clicked, it triggers the generate_histogram_options function from the tools module, which prompts the user to choose 
    whether to create histograms with or without ouliers.
    '''
    
    button4 = tk.Button(root, 
                            text="IV .generate histograms",  
                            command=lambda: tools.generate_histogram_options(df, df_cleaned),
                            width=button_width, 
                            height=button_height, 
                            anchor=button_anchor, 
                            justify=button_justify, 
                            bg=button_bg, 
                            fg=button_fg)
    button4.place(relx=0.60, rely=0.8, anchor="center") 
    button4['font'] = font_buttons

def button_5(root,df,df_cleaned,button_width,button_height,button_anchor,button_justify,button_bg,button_fg,font_buttons):
    '''
    This function is part of the GUI setup in the opening_menu function, creating and configuring a button within the menu. 
    When clicked, it triggers the perform_PCA_options function from the tools module, which prompts the user to choose 
    whether to compute PCA with or without ouliers.
    '''
    
    button5 = tk.Button(root, 
                        text="V .compute PCA",  
                        command=lambda: tools.perform_PCA_options(df, df_cleaned),
                        width=button_width, 
                        height=button_height, 
                        anchor=button_anchor, 
                        justify=button_justify, 
                        bg=button_bg, 
                        fg=button_fg)
    button5.place(relx=0.60, rely=0.9, anchor="center")  
    button5['font'] = font_buttons