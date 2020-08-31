# HT delete notices GUI App 
# Develped by: Ashan Liyanage
# Version 0.2

import threading
import tkinter as tk
import email
from pathlib import Path
from tkinter import filedialog, messagebox


# from tkinter import messagebox

# from tensorflow.python.keras.engine.training_utils import collect_per_output_metric_info


def check_status(dir_name, vol_name, path):
    my_path = path / dir_name

    if not my_path.exists():
        return "No dir: " + str(my_path)
    else:
        dir_root = my_path / 'pairtree_root'
        vol_names = [vol_name[i:i + 2] for i in range(0, len(vol_name), 2)]
        for i in range(0, len(vol_names)):
            dir_root = dir_root / vol_names[i]

        if not dir_root.exists():
            return "No vol: " + str(dir_root)
        else:
            # s = list(dir_root.glob('*' + vol_name + "*"))
            s = list(dir_root.glob("*"))
            if s:
                return s
            else:
                return "Already deleted or nothing inside: " + str(dir_root)


def get_email_data(email_file):
    text_data = ''
    with open(email_file, 'r') as f:
        msg = email.message_from_file(f)
        # print(msg)
        if msg.is_multipart():
            return 'multipart email functionality is not yet defined. Contact Ashan.'
        else:
            payload = msg.get_payload(decode=True)
            strtext = payload.decode()
            # dt = msg.get('date')
            # print(dt)
            # print(strtext)
            # print('single')
            text_data = strtext

    some_useful_data = text_data.split('===')
    if len(some_useful_data) >= 4:
        useful_data = some_useful_data[2].split()
        # print(text_data)
        data_out = []
        for data in useful_data:
            temp_data = data.split('.')
            data_out.append(temp_data[0])
            data_out.append(temp_data[1])
        if len(data_out) == 0:
            return 'Empty ID LIST found in the Email. Tip: check ID LIST in the email'
        else:
            return data_out
    else:
        return 'No ID LIST found in the Email. Tip: check "===BEGIN ID LIST===" and "===END ID LIST===" in the email'


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def delete_files_dirs(delete_files_list):
    for item in delete_files_list:
        if item.is_dir():
            rm_tree(item)
        else:
            item.unlink()


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        BG_COLOR = "#A0A0A0"
        self.title("HT Delete Notices App")
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True)

        self.minsize(800, 500)
        # X_WIDTH = 140
        # self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='hXUrRNqC_400x400.png'))

        # Vertical Frame for the Label
        vertical_frame1 = tk.Frame(main_frame, bg=BG_COLOR)
        label1 = tk.Label(vertical_frame1, text='Load Email', bg=BG_COLOR)
        label1.pack(fill='x', padx=10, pady=(20, 0))
        vertical_frame1.pack(fill="x")

        self.str_email = tk.StringVar()
        self.str_email.set(" Use 'Browse' button to select the email file")

        # Horizontal frame for the Entry and the Button
        horizontal_frame1 = tk.Frame(main_frame, bg=BG_COLOR)

        entry_email = tk.Entry(horizontal_frame1, textvariable=self.str_email)
        entry_email.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        button_email = tk.Button(horizontal_frame1, text="Browse", command=self.browse_email)
        button_email.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        horizontal_frame1.grid_columnconfigure(0, weight=9)
        horizontal_frame1.grid_columnconfigure(1, weight=1)

        horizontal_frame1.pack(fill='x')

        # Vertical Frame for the Label
        vertical_frame2 = tk.Frame(main_frame, bg=BG_COLOR)
        label2 = tk.Label(vertical_frame2, text='Search directory', bg=BG_COLOR)
        label2.pack(fill='x', padx=10, pady=(20, 0))
        vertical_frame2.pack(fill="x")

        self.str_root = tk.StringVar()
        self.str_root.set(" Use 'Browse' button to select the 'Pairtree' Directory.")

        # Horizontal frame for the Entry and the Button
        horizontal_frame2 = tk.Frame(main_frame, bg=BG_COLOR)

        entry_root = tk.Entry(horizontal_frame2, textvariable=self.str_root)
        entry_root.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        button_root = tk.Button(horizontal_frame2, text="Browse", command=self.browse_root)
        button_root.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        horizontal_frame2.grid_columnconfigure(0, weight=9)
        horizontal_frame2.grid_columnconfigure(1, weight=1)

        horizontal_frame2.pack(fill='x')

        # Vertical Frame for the Label
        vertical_frame3 = tk.Frame(main_frame, bg=BG_COLOR)
        label3 = tk.Label(vertical_frame3, text='Console', bg=BG_COLOR)
        label3.pack(fill='x', padx=10, pady=(20, 0))
        vertical_frame3.pack(fill="x")

        # Horizontal frame for the Text box and buttons
        horizontal_frame3 = tk.Frame(main_frame, bg=BG_COLOR)

        vertical_frame_sub1 = tk.Frame(horizontal_frame3, bg=BG_COLOR)
        vertical_frame_sub1.grid(row=0, column=0, sticky="nsew")

        vertical_frame_sub2 = tk.Frame(horizontal_frame3, bg=BG_COLOR)
        vertical_frame_sub2.grid(row=0, column=1, sticky="nsew")

        horizontal_frame3.grid_columnconfigure(0, weight=9)
        horizontal_frame3.grid_columnconfigure(1, weight=1)

        horizontal_frame3.pack(fill='both')

        # Text Box
        self.text_box = tk.Text(vertical_frame_sub1, width=11, yscrollcommand=True)
        self.text_box.pack(fill="x", padx=10, pady=5)

        # Buttons
        button_detect = tk.Button(vertical_frame_sub2, text="Detect", command=self.detect_vols)
        button_detect.pack(fill="x", padx=10, pady=5)

        button_clean = tk.Button(vertical_frame_sub2, wraplength=70, text="Delete Identified Files", bg='#ff3232',
                                 command=self.clean_vols)
        button_clean.pack(fill="x", padx=10, pady=10)

        button_print = tk.Button(vertical_frame_sub2, wraplength=70, text='Save logs to a TXT', command=self.print)
        button_print.pack(fill="x", padx=10, pady=10)

    # command=threading.Thread(target=self.start_clean_vols).start)
    #    self.button_clean.grid(column=1, row=4)

    #    s

    #    def refresh(self):
    #        self._root().update()
    #        self._root().after(1000, self.refresh)#
    #
    #    def start_browse_email(self):
    #        self.refresh()
    #        threading.Thread(target=self.browse_email).start()
    #
    #    def start_clean_vols(self):
    #        print(self.str_email)
    #        print(threading.current_thread())
    #        t1 = threading.currentThread()
    #        t1.daemon

    def print(self):

        file = filedialog.asksaveasfile(initialfile="email_cleaned_log", title="Save Text File as",
                                        defaultextension='.txt',
                                        filetypes=[("Text files", ".txt")])
        if file:

            save_file_data = str(self.text_box.get(1.0, "end-1c"))
            file.write(save_file_data)
            # f = open(self.filename, 'w')
            # f.write(self.text.get('1.0', 'end'))
            file.close()
            messagebox.showinfo('FYI', 'File Saved')
            

    def detect_vols(self):
        email_file = Path(str(self.str_email.get()))
        root_path = Path(str(self.str_root.get()))
        self.text_box.delete('1.0', tk.END)
        if not email_file.exists():
            self.text_box.insert(tk.END, 'Error. Please select a valid email(.eml) file\n'
                                 + "Given Path: " + str(self.str_email.get()) + '\n')
            return None
        elif not root_path.exists():
            self.text_box.insert(tk.END, 'Error. Please select a valid search directory\n'
                                 + "Given Path: " + str(self.str_root.get()) + '\n')
            return None
        else:
            self.text_box.insert(tk.END, 'Email file: ' + str(email_file) + '\n')
            self.text_box.insert(tk.END, 'Given pairtree directory: ' + str(root_path) + '\n')

            email_data = get_email_data(email_file)
            if isinstance(email_data, str):
                self.text_box.insert(tk.END, email_data + '\n')
                return None
            else:
                self.text_box.insert(tk.END, '\ndir\t->\tvol name\t:\tstatus\n')
                delete_ready = []
                for i in range(0, len(email_data), 2):
                    dir_name = email_data[i]
                    vol_name = email_data[i + 1]
                    status_var = check_status(dir_name, vol_name, root_path)
                    if isinstance(status_var, list):
                        status = "Ready to Delete: <listed below> \n" + str('\n'.join(map(str, status_var))) + "\n"
                        delete_ready.append(status_var)
                    else:
                        status = status_var
                    self.text_box.insert(tk.END, dir_name + "\t->" + '\t' + vol_name
                                         + '\t:\t' + status + '\n')
                if len(delete_ready) == 0:
                    return None
                else:
                    return delete_ready

    def clean_vols(self):

        output = self.detect_vols()
        if output:
            delete_files_list = []
            index = 0
            for i in range(0, len(output)):
                # print('123')
                for j in range(0, len(output[i])):
                    delete_files_list.append(output[i][j])
                    index += 1
            if messagebox.askyesno('Verify', str(index) + ' files/directories to delete. Are you sure that you want to '
                                                          'delete ?'):
                # print(delete_files_list)
                delete_files_dirs(delete_files_list)
                self.text_box.insert(tk.END, '\nDeleted file/directory list:\n' + str(
                    '\n'.join(map(str, delete_files_list))) + '\n')

            else:
                self.text_box.insert(tk.END, 'Nothing deleted.\n')
        else:
            messagebox.showwarning('FYI', 'Nothing to delete')

    def browse_root(self):
        directory = filedialog.askdirectory()
        if directory:
            self.str_root.set(directory)

    def browse_email(self):
        file = filedialog.askopenfilename(filetypes=[("E-mail file", ".eml")])
        if file:
            self.str_email.set(file)


window = Window()
window.mainloop()
