import os, send2trash
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.ttk import Progressbar

window = Tk()

window.resizable(False, False)

win_width = 400
win_height = 360
half_width = win_width/2
half_height = win_height/2

window.geometry(str(win_width) + 'x' + str(win_height))

directory_name = Entry(window, width=62)
directory_name.grid(column=0, row=1, sticky=W, padx=10, pady=10)

file_listbox = Listbox(window, width=62)
file_listbox.grid(column=0, row=3, sticky=W, padx=10, pady=10)

check_sub = BooleanVar()
check_sub.set(False)

window.title("Delete Duplicate files")
    
def get_directory():
    dir_name = askdirectory()
    if not dir_name == '':                 #clear entry if cancel button is pressed on askdirectory dialog
        directory_name.delete(0, 'end')
    directory_name.insert(0, dir_name)
    show_files()
    
def show_files():
    file_listbox.delete(0, 'end')
    files = get_duplicate_files()
    for file in files:
        if os.path.isfile(os.path.join(directory_name.get(), file)):
            file_listbox.insert(0, file)
    
btn_get_directory = Button(window, text="Choose Directory", command=get_directory)
btn_get_directory.grid(column=0, row=2, sticky=N+W, padx=10)

def create_delete_buttons():
    btn_delete_temp = Button(window, text="Move to Recycle Bin", command=delete_temp)
    btn_delete_temp.grid(column=0, row=4, sticky=S+W, padx=10)
    btn_delete_perma = Button(window, text="Delete Permanently", command=delete_perma)
    btn_delete_perma.grid(column=0, row=4, sticky=S+W, padx=140)
    
def create_subfolder_check():
    check_subfolder = Checkbutton(window, text="Include Subfolders", variable=check_sub)
    check_subfolder.grid(column=0, row=4, sticky=S+W, padx=260)
    
def create_progress_bar():
    bar = Progressbar(window, length=380)
    bar.grid(column=0, row=5, sticky=S+W, padx=10, pady=10)
    bar['value'] = 0
    return bar

def create_show_files_button():
    btn_show_files = Button(window, text="Show Files", command=show_files)
    btn_show_files.grid(column=0, row=2, sticky=N+W, padx=125)

def get_duplicate_files():
    os.chdir(directory_name.get())
    files_name = os.listdir()
    check = check_sub.get()
    copy_regex = re.compile(r'.*?( )(-)( )(Copy)|\([0-9]\)')
    duplicate_files = []
    if check:
        for folders, subfolders, files in os.walk(directory_name.get()):
            for file in files:
                curr_file = copy_regex.search(file)
                if(curr_file != None):
                    duplicate_files.append(os.path.join(folders, file))
            
    else:
        for file in files_name:
            curr_file = copy_regex.search(file)
            if(curr_file != None):
                duplicate_files.append(file)
            
    return duplicate_files

def check_path():
    return os.path.exists(directory_name.get())
    
def path_does_not_exist():
    error = messagebox.showerror('Incorrect Path', 'Path does not exist\nPlease choose a correct path')
    
def delete_temp():
    if check_path():
        msg = messagebox.askyesno("Move to Recycle Bin", "Confirm moving files to Recycle Bin")
        if msg:
            prompt = messagebox.askyesnocancel("Prompt for Deletion?", "Do you want to be prompted for each file?")
            bar = create_progress_bar()
            files = get_duplicate_files()
            for file in files:
                bar['value'] += (100/len(files))
                if prompt == True:
                    delete_prompt = messagebox.askyesno("Delete?", "Delete File " + file)
                    if delete_prompt:
                        send2trash.send2trash(file)
                elif prompt == False:
                    send2trash.send2trash(file)
                elif prompt == None:
                    bar['value'] = 0
                    return False
    else:
        path_does_not_exist()
        
def delete_perma():
    if check_path():
        msg = messagebox.askyesno("Permanently Delete?", "These files will be permanently deleted.\nAre you sure you want to continue?")
        if msg:
            prompt = messagebox.askyesnocancel("Prompt for Deletion?", "Do you want to be prompted for each file?")
            bar = create_progress_bar()
            files = get_duplicate_files()
            for file in files:
                bar['value'] += (100/len(files))
                if prompt == True:
                    delete_prompt = messagebox.askyesno("Delete?", "Delete File " + file)
                    if delete_prompt:
                        os.unlink(file)
                elif prompt == False:
                    os.unlink(file)
                elif prompt == None:
                    bar['value'] = 0
                    return False
    else:
        path_does_not_exist()
         
create_delete_buttons()
create_subfolder_check()
create_show_files_button()

window.mainloop()

