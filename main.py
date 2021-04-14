from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def search():
    if not website_entry.get():
        messagebox.showwarning(title='Oops', message="Please don't leave any fields empty!")
        return

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title='Oops', message="No data file found!")
    else:
        if website_entry.get() in data:
            messagebox.showinfo(title=website_entry.get(), message=f"Email: {data[website_entry.get()]['email']} \n"
                                                                   f"Password:  {data[website_entry.get()]['password']}")
        else:
            messagebox.showwarning(title='Oops', message=f"No details for the {website_entry.get()} exists.")
            return


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    if password_entry.get():
        password_entry.delete(0, END)

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    if not website_entry.get() or not email_entry.get() or not password_entry.get():
        messagebox.showwarning(title='Oops', message="Please don't leave any fields empty!")
        return

    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get()
        }
    }
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        with open('data.json', 'w') as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=130, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(65, 100, image=image)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text='Website:')
website_label.grid(row=1, column=0, sticky=E)
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0, sticky=E)
password_label = Label(text='Password:')
password_label.grid(row=3, column=0, sticky=E)

# Entries
website_entry = Entry(width=22)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=41)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, 'deniss@gmail.com')
password_entry = Entry(width=22)
password_entry.grid(row=3, column=1)

# Buttons
generate_pass = Button(text='Generate Password', command=generate)
generate_pass.grid(row=3, column=2, sticky=W)
add_button = Button(text='Add', width=34, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text='Search', width=15, command=search)
search_button.grid(row=1, column=2, sticky=W)

window.mainloop()
