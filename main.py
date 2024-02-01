from tkinter import *
import re
import random
import string
from tkinter import messagebox
import json

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg='lightgray')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    # Define the criteria for the password
    min_length = 10
    uppercase_required = True
    lowercase_required = True
    numeric_required = True
    special_char_required = True

    # Define character sets
    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    numeric_chars = string.digits
    special_chars = string.punctuation

    # Ensure at least one character from each set
    password = (
        random.choice(uppercase_chars) if uppercase_required else '' +
        random.choice(lowercase_chars) if lowercase_required else '' +
        random.choice(numeric_chars) if numeric_required else '' +
        random.choice(special_chars) if special_char_required else ''
    )

    # Add random characters to meet the minimum length
    while len(password) < min_length:
        password += random.choice(uppercase_chars + lowercase_chars + numeric_chars + special_chars)

    # Shuffle the password characters to make it more random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)
    
# ---------------------------- FIND PASSWORD FROM THE JSON_FILE ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")  


# ---------------------------- SAVE PASSWORD to JSON  ------------------------------- #

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password":password,
        }
    }
    if len(website) == 0 or len(email) == 0 or  len(password) == 0:
        messagebox.showerror(title="Error", message=f"Please Fill all the fields")
    else:
        try:
            with open("data.json", 'r') as data_file:
                #read the json data file
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                #writing to the data file
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END) 

# ---------------------------- User Interface SETUP ------------------------------- #

canvas=Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

#Labels and buttons and entries for our password manager
website_label = Label(text="Website: ", font=('Arial', 12, 'bold'), fg='green')
website_label.grid(column=0, row=1)
email_label = Label(text="Email: ", font=('Arial', 12, 'bold'), fg="green")
email_label.grid(column=0, row=2)
password_label = Label(text="Password: ", font=('Arial', 12, 'bold'), fg="green")
password_label.grid(column=0, row=3)

#Entries for website, email and password
website_entry = Entry(bg='white', width=25)
website_entry.focus()
website_entry.grid(row=1, column=1)

email_entry = Entry(bg='white', width=40)
email_entry.grid(row=2, column=1, columnspan=3)

password_entry = Entry(bg='white', width=25)
password_entry.grid(row=3, column=1)

#buttons
search_button = Button(text="Search", font=("Arial", 8,'bold'), fg='green', width=15, command=find_password)
search_button.grid(row=1, column=2)

generate_password = Button(text="Generate Password",font=("Arial", 8,'bold'), fg='green', width=15, command=generate_password)
generate_password.grid(row=3, column=2)

add_button = Button(text="Add Password",font=("Arial",10, 'bold'), fg='green', width=38, command=save_password)
add_button.grid(row=4,column=1, columnspan=3)

window.mainloop()