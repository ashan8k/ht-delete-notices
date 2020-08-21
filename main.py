import threading
import tkinter as tk
import email
from pathlib import Path
from tkinter import filedialog, messagebox


# from tkinter import messagebox

# from tensorflow.python.keras.engine.training_utils import collect_per_output_metric_info


def delete_vol(dir_name, vol_name, path1):
    path = Path(path1)
    my_path = path / dir_name

    def rm_tree(pth):
        pth = Path(pth)
        for child in pth.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                rm_tree(child)
        pth.rmdir()

    if my_path.exists():
        dir_root = my_path / 'pairtree_root'
        vol_names = [vol_name[i:i + 2] for i in range(0, len(vol_name), 2)]
        for i in range(0, len(vol_names)):
            dir_root = dir_root / vol_names[i]
        if dir_root.exists():
            print(dir_root)
            s = list(dir_root.glob('*' + vol_name + "*"))
            print(s)
            if s:
                for item in s:
                    if item.is_dir():
                        rm_tree(item)
                    else:
                        item.unlink()
                    print('Deleted :' + vol_name + " @ " + item)
                    return 'Deleted :' + vol_name + " @ " + item
            else:
                print("Already deleted/ nothing inside")
                return "Already deleted/ nothing inside"

        else:
            print('No pairtree folder or files for ' + vol_name)
            return 'No pairtree folder or files for ' + vol_name
    else:
        print('No dir= ' + str(my_path))
        return 'No dir= ' + str(my_path)


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.title("Title goes here")
        self.minsize(1100, 400)
        X_WIDTH = 170
        # self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='hXUrRNqC_400x400.png'))

        self.label_email = tk.Label(self, text="Load Email")
        self.label_email.grid(column=0, row=0, padx=10, pady=10)

        self.str_email = tk.StringVar()
        self.str_email.set("Use 'Browse' button to select email file")
        self.entry_email = tk.Entry(self, width=X_WIDTH, textvariable=self.str_email)
        self.entry_email.grid(column=0, row=1, padx=10, pady=10)

        self.button_email = tk.Button(self, text="Browse", command=self.browse_email)
        self.button_email.grid(column=1, row=1)

        # root path
        self.label_root = tk.Label(self, text="Search directory")
        self.label_root.grid(column=0, row=2, padx=10, pady=10)

        self.str_root = tk.StringVar()
        self.str_root.set('default search dir is not selected')
        self.entry_root = tk.Entry(self, width=X_WIDTH, textvariable=self.str_root)
        self.entry_root.grid(column=0, row=3, padx=10, pady=10)

        self.button_root = tk.Button(self, text="Browse", command=self.browse_root)
        self.button_root.grid(column=1, row=3)

        self.text_box = tk.Text(self, height=10, width=X_WIDTH - 42)
        self.text_box.grid(column=0, row=4, pady=10)

        self.button_clean = tk.Button(self, text="Clean", command=self.clean_vols)
        # command=threading.Thread(target=self.start_clean_vols).start)
        self.button_clean.grid(column=1, row=4)

        self.button_print = tk.Button(self, text='Print to TXT file', command=self.print)
        self.button_print.grid(column=0, row=5)

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
        self.file_s = filedialog.asksaveasfile(initialfile="email_cleaned_log", title="Save Text File as",
                                                     defaultextension='.txt',
                                                     filetypes=[("Text files", ".txt")])

        save_file = str(self.text_box.get(1.0, "end-1c"))
        self.file_s.write(save_file)
        #f = open(self.filename, 'w')
        #f.write(self.text.get('1.0', 'end'))
        self.file_s.close()
        messagebox.showinfo('FYI', 'File Saved')

    def clean_vols(self):
        email_file = Path(str(self.str_email.get()))
        root_path = Path(str(self.str_root.get()))
        # print(self.str_email.get())
        if not email_file.exists() and not root_path.exists():
            self.text_box.insert(tk.END, 'Error. Please select email(.eml) file & Search directory\n')
        elif not email_file.exists() and root_path.exists():
            self.text_box.insert(tk.END, 'Error. Please select email(.eml) file\n')
        elif email_file.exists() and not root_path.exists():
            self.text_box.insert(tk.END, 'Error. Please select Search directory\n')
        else:
            self.text_box.insert(tk.END, 'Email file: ' + str(email_file) + '\n')
            self.text_box.insert(tk.END, 'Search directory: ' + str(root_path) + '\n')
            text_data = ''

            with open(email_file, 'r') as f:
                msg = email.message_from_file(f)
                # print(msg)
                if msg.is_multipart():
                    print('multi')
                else:
                    payload = msg.get_payload(decode=True)
                    strtext = payload.decode()
                    dt = msg.get('date')
                    # print(dt)
                    # print(strtext)
                    print('single')
                    text_data = strtext

            usefull_data = text_data.split('===')[2].split()
            # print(text_data)
            self.text_box.insert(tk.END, 'dir\t->\tvol name\t:\tstatus\n')
            for data in usefull_data:
                temp_data = data.split('.')
                dir_name = temp_data[0]
                vol_name = temp_data[1]
                status = delete_vol(dir_name, vol_name, root_path)
                # print(dir_name + vol_name + str(root_path))
                self.text_box.insert(tk.END, dir_name + "\t->" + '\t' + vol_name + '\t:\t' + status + '\n')
                #   print(dir_name+"->"+vol_name)

    def browse_root(self):
        directory = filedialog.askdirectory()
        self.str_root.set(directory)

    def browse_email(self):
        file = filedialog.askopenfilename(filetypes=[("E-mail file", ".eml")])
        if file:
            self.str_email.set(file)


window = Window()
window.mainloop()
