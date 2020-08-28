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

        BG_COLOR = "#A9A9A9"
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
        horizontal_frame3 = tk.Frame(main_frame, bg='blue')

        #self.text_box = tk.Text(horizontal_frame3)
        #self.text_box.pack(fill='y', expand=True)
        #self.text_box.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        #self.text_box2 = tk.Text(horizontal_frame3)
        #self.text_box2.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        vertical_frame_sub1 = tk.Frame(horizontal_frame3, bg='red')
        vertical_frame_sub1.grid(row=0, column=0,  sticky="nsew")

        vertical_frame_sub2 = tk.Frame(horizontal_frame3, bg='green')
        vertical_frame_sub2.grid(row=0, column=1, sticky="nsew")
        #button_root11 = tk.Button(horizontal_frame3, text="Browse", command=self.browse_root)
        #button_root11.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        #button_root12 = tk.Button(horizontal_frame3, text="Browse", command=self.browse_root)
        #button_root12.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        horizontal_frame3.grid_columnconfigure(0, weight=9)
        horizontal_frame3.grid_columnconfigure(1, weight=1)

        horizontal_frame3.pack(fill='both', expand=True)

        #entry_email2 = tk.Entry(vertical_frame_sub1, textvariable=self.str_email)
        #entry_email2.pack( fill='x', padx=10, pady=5)

        button_root11 = tk.Text(vertical_frame_sub1, width=11, yscrollcommand=True)
        button_root11.pack(fill="x",padx=10, pady=5)

        button_root21 = tk.Button(vertical_frame_sub2, text="Browse", command=self.browse_root)
        button_root21.pack(fill="x", padx=10, pady=5)

    #    self.text_box = tk.Text(self, height=10, width=X_WIDTH )
    #    self.text_box.grid(column=0, row=4, pady=10, padx=10)

    #    self.button_clean = tk.Button(self, text="Clean", command=self.clean_vols)
    # command=threading.Thread(target=self.start_clean_vols).start)
    #    self.button_clean.grid(column=1, row=4)

    #    self.button_print = tk.Button(self, text='Print to TXT file', command=self.print)
    #    self.button_print.grid(column=0, row=5)

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
        # f = open(self.filename, 'w')
        # f.write(self.text.get('1.0', 'end'))
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
        if directory:
            self.str_root.set(directory)

    def browse_email(self):
        file = filedialog.askopenfilename(filetypes=[("E-mail file", ".eml")])
        if file:
            self.str_email.set(file)


window = Window()
window.mainloop()
