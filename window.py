import tkinter as tk
from tkinter import messagebox

def validate_input():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        messagebox.showinfo("Ввод успешен", f"Координаты: X = {x}, Y = {y}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения для координат.")

root = tk.Tk()
root.geometry('600x400')
root.title("Построение траектории Беспилотного летательного аппарата")

label_x = tk.Label(root, text="Окно для ввода координаты Х")
label_x.pack()

entry_x = tk.Entry(root)
entry_x.pack()
label_y = tk.Label(root, text="Окно для ввода координаты У")
label_y.pack()

entry_y = tk.Entry(root)
entry_y.pack()

button = tk.Button(root, text="Ввести", command=validate_input)
button.pack()

root.mainloop()
