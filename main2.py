import tkinter as tk

main_window = tk.Tk()
main_frame = tk.Frame(main_window, bg='#A9A9A9')
main_frame.pack(fill="both", expand=True)

# Vertical layout with data
vertical_frame = tk.Frame(main_frame, bg='blue')

label1 = tk.Label(vertical_frame, text='text1', bg='red', pady=10)
label1.pack(fill='x', padx=10, pady=10)

label2 = tk.Label(vertical_frame, text='text2',  bg='red')
label2.pack(fill='x', padx=10, pady=10)

label3 = tk.Label(vertical_frame, text='text3',  bg='red', fg='white')
label3.pack(fill='x', padx=10, pady=10)

vertical_frame.pack(fill="x")

# End  vertical

# horizontal

horizontal_frame = tk.Frame(main_frame, bg='yellow')

label4 = tk.Label(horizontal_frame, text='This is text4',  bg='green', fg='white')
label4.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label5 = tk.Label(horizontal_frame, text='text5',  bg='green', fg='white')
label5.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

horizontal_frame.grid_columnconfigure(0, weight=9)
horizontal_frame.grid_columnconfigure(1, weight=1)

horizontal_frame.pack(fill='x')


main_window.mainloop()
