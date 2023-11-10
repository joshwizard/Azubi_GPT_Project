import tkinter as tk
from tkinter import scrolledtext

import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

# Load the Tkinter root window
root = tk.Tk()
root.title("Chatbot")

# Configure colors
root.configure(bg='sky blue')

# Create chat history area
chat_history_text = scrolledtext.ScrolledText(root, state='disabled', bg='lightgray', wrap='word', width=40, height=10)
chat_history_text.pack(padx=10, pady=10, fill='both', expand=True)

# Create user input field
user_input_field = tk.Entry(root, bg='white')
user_input_field.pack(padx=10, pady=5, fill='x', expand=True)

# Variable to track conversation status
conversation_active = True

# Create a function to handle user input
def process_user_input(event=None):
    global conversation_active
    
    user_input = user_input_field.get()

    if not user_input:
        return  # Do nothing if the user input is empty

    chat_history_text.configure(state='normal')
    chat_history_text.insert('end', 'You: ' + user_input + '\n')

    # Check if the user wants to end the conversation
    if user_input.lower() == 'exit':
        conversation_active = False
        root.destroy()  # Close the Tkinter window
        return

    # Chatbot logic
    ints = predict_class(user_input)
    
    if ints:
        res = get_response(ints, intents)
        chat_history_text.insert('end', 'Bot: ' + res + '\n')
    else:
        chat_history_text.insert('end', "Bot: I'm sorry, I don't understand that.\n")

    chat_history_text.see('end')  # Scroll to the end
    chat_history_text.configure(state='disabled')

    user_input_field.delete(0, 'end')  # Clear the user input field

    # Check if the conversation is still active
    if not conversation_active:
        root.quit()  # Exit the Tkinter main loop

# Bind the Enter key to the user input field
user_input_field.bind('<Return>', process_user_input)

# Create send button
send_button = tk.Button(root, text='Send', command=process_user_input, bg='lightgreen')
send_button.pack(pady=5)

# Load the chatbot model and data
lemmatizer = WordNetLemmatizer()
with open('intents.json', 'r') as file:
    intents = json.load(file)

words = pickle.load(open('words.pk', 'rb'))
classes = pickle.load(open('classes.pk', 'rb'))
model = load_model('chatbot_model.h5')

# Define chatbot functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25

    # Get the index of the highest probability
    max_prob_index = np.argmax(res)

    # Check if the probability is above the threshold
    if res[max_prob_index] > ERROR_THRESHOLD:
        return_list = [{'intent': classes[max_prob_index], 'probability': str(res[max_prob_index])}]
        return return_list
    else:
        return []

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    # Set a default value for result
    result = "I'm sorry, I don't understand that."

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['response'])
            break

    return result

# Run the Tkinter main loop
root.mainloop()
