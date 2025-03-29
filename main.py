from tkinter import *
from tkinter import ttk
from src.handlers.time_handler import getTimezone

class Chatbot:
    
    def __init__(self, root):
        root.title("World Chatbot")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.question = StringVar()
        self.answer = StringVar()
        self.pending_timezones = None  # Track pending timezones for follow-up queries

        # Question label and entry
        ttk.Label(mainframe, text="Question:").grid(column=1, row=1, sticky=W)
        question_entry = ttk.Entry(mainframe, textvariable=self.question)
        question_entry.grid(column=2, row=1, sticky=(W, E))

        # Configure column weights for resizing
        mainframe.columnconfigure(1, weight=0)  # Label column does not expand
        mainframe.columnconfigure(2, weight=1)  # Entry column expands

        # Send button
        ttk.Button(mainframe, text="Send", command=self.main).grid(column=2, row=2, sticky=W)

        # Answer label and entry
        ttk.Label(mainframe, text="Answer:").grid(column=1, row=3, sticky=W)
        answer_entry = ttk.Entry(mainframe, textvariable=self.answer, state="readonly")
        answer_entry.grid(column=2, row=3, sticky=(W, E))

        # Add padding for all widgets
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # Set focus to the question entry box
        question_entry.focus()
        root.bind("<Return>", self.main)

    def main(self, *args):
        userInput = self.question.get().strip()

        if userInput:
            # Split the input into words
            words = userInput.split()

            # Define handlers for specific keywords
            handlers = {
                "time": self.handleTime,
                # Add more handlers here in the future, e.g., "weather": self.handleWeather
            }

            # Check if any keyword in the input matches a handler
            for word in words:
                if word.lower() in handlers:
                    # Call the corresponding handler and pass the remaining words
                    handlers[word.lower()](words)
                    break
            else:
                # If no keyword matches, respond with a default message
                self.answer.set("I don't understand your question.")

            # Clear the question input box
            self.question.set("")
        else:
            self.answer.set("Please enter a question.")

    def handleTime(self, words):
        # Pass the entire user input to time_handler.py
        userInput = " ".join(words)  # Reconstruct the input string
        response, self.pending_timezones = getTimezone(userInput, self.pending_timezones)

        # Display the response
        self.answer.set(response)

root = Tk()
Chatbot(root)
root.mainloop()