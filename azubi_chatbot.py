from tkinter import *
import tkinter as tk
from tkinter import messagebox
import json
import datetime

#--------------------------------------------------------------------------------------------------------------------
# greetings based on time opening chatbot
current_time = datetime.datetime.now()

if 6 <= current_time.hour <= 12:
    greeting = "Good Morning!"
elif 12 <= current_time.hour <= 16:
    greeting = "Good Afternoon!"
else:
    greeting = "Good Evening!"

#---------------------------------------------------------------------------------------------------------------------
# Load initial responses from a JSON file
responses = {}
try:
    with open('responses.json', 'r') as file:
        responses = json.load(file)
except FileNotFoundError:
    responses = {}

# Create a dictionary to keep track of the last selected response index
last_selected_index = {}

# Create a dictionary to hold the temporary response data
temp_response = {
    "question": "",
    "answer": ""
}

# response answer based on selected question
def random_response():
    selected_response = dropdown.get()
    if selected_response in responses:
        responses_list = responses[selected_response]
        if responses_list:

            # Display the questions in order
            last_index = last_selected_index.get(selected_response, -1)
            last_index = (last_index + 1) % len(responses_list)

            selected_response_text = responses_list[last_index]
            last_selected_index[selected_response] = last_index

            # View answers on the chatbot
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"{selected_response_text}\n\n")
            chat_history.config(state=tk.DISABLED)
        else:
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, "I don't have a response for that.\n\n")
            chat_history.config(state=tk.DISABLED)

# Clear the chat history 
def clear_chat():
    chat_history.config(state=tk.NORMAL)
    chat_history.delete('1.0', tk.END)
    chat_history.config(state=tk.DISABLED)

# exit the chatbot
def exit_chat():
    root.quit()

#------------------------------------------------------------------------------------------------------------------------
# Function to open the login window
def open_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x150")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")  # Use "show" to hide password characters
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), login_window))
    login_button.pack()

# Function to handle login
def login(username, password, login_window):
    # Add your login logic here
    if username == "azubi" and password == "1111":
        add_response_window = tk.Toplevel(root)
        add_response_window.title("Add Response")
        add_response_window.geometry("300x150")

        question_label = tk.Label(add_response_window, text="Question:")
        question_label.pack()
        question_entry = tk.Entry(add_response_window)
        question_entry.pack()

        answer_label = tk.Label(add_response_window, text="Answer:")
        answer_label.pack()
        answer_entry = tk.Entry(add_response_window)
        answer_entry.pack()

# save responses to json file
        def save_response():
            temp_response["question"] = question_entry.get()
            temp_response["answer"] = answer_entry.get()
            responses[temp_response["question"]] = temp_response["answer"]
            with open('responses.json', 'w') as file:
                json.dump(responses, file, indent=4)
            question_entry.delete(0, tk.END)
            answer_entry.delete(0, tk.END)
            add_response_window.destroy()

# save button for save responses to json
        save_button = tk.Button(add_response_window, text="Save Response", command=save_response)
        save_button.pack()

        login_window.destroy()

# Error message when login fails
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

#----------------------------------------------------------------------------------------------------------------------------
# Tkinter UI/UX design
root=Tk()
root.title('Azubi-GPT Chatbot')
root.geometry('700x400+150+100')
root.configure(bg='light blue')
root.resizable(False, False)

# Heading label to inform the user what to do
heading = Label(root, text=f"{greeting} 😄 . I'm Azubi_GPT. Ask me the questions from the drop down menu.", fg='#000', bg='white', font=('Microsoft YaHei UI Light', 10, 'bold'))
heading.place(x=10, y=5)

# Dropdown Menu for the user to select
dropdown = tk.StringVar()
dropdown.set("Select a response")
dropdown_menu = tk.OptionMenu(root, dropdown, "Program Duration", "tips", "Contacts", "Schedule", "Eligibility Criteria", "Curriculum", "Instructors", "Learning Resources", "Tuition fee", "Payment Options", "Career Opportunities", "Refund Policy", "Collaboration")
dropdown_menu.grid(row=1, column=0, padx=100, pady=100)
dropdown_menu.place(x=10, y=40)
dropdown_menu.config(width=70)

#This is where the user responses will be displayed
chat_history = Text(root, fg='black', border=2, bg='white', height=17, width=57, font=("cambria", 11))
chat_history.place(x=10, y=90)

# Button to ask the question
ask = Button(root, command=random_response, width=20, pady=7, text="Ask", fg='black').place(x=500, y=90)

# Button to clear the screen
clear = Button(root, command=clear_chat, width=20, pady=7, text="Clear", fg='black')
clear.place(x=500, y=150)

# Button to add response
add_response = Button(root, command=open_login_window, width=20, pady=7, text="Add Response", fg='black')
add_response.place(x=500, y=210)

# Button to exit the chatbot
exit = Button(root, width=20, pady=7, text="Exit", fg='black', command=exit_chat)
exit.place(x=500, y=270)

root.mainloop()