# :3
from tkinter import *
from tkinter import ttk
from src.handlers.time_handler import getTimezone

class Chatbot:
    
    def __init__(self, root):
        # Give the window a title
        root.title("World Chatbot")

        # Define the size of the window
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create String Variables for the question and answer
        self.question = StringVar()
        self.answer = StringVar()

        # Initialize pending_timezones to None
        self.pending_timezones = None  

        # Create the button GUI components
        ttk.Label(mainframe, text="Question:").grid(column=1, row=1, sticky=W)
        question_entry = ttk.Entry(mainframe, textvariable=self.question)
        question_entry.grid(column=2, row=1, sticky=(W, E))

        # Allows the user to resize the window while having the components resize with it
        mainframe.columnconfigure(1, weight=0)  
        mainframe.columnconfigure(2, weight=1) 
        
        # Create the button to send the question
        ttk.Button(mainframe, text="Send", command=self.main).grid(column=2, row=2, sticky=W)

        # Create the answer GUI components
        ttk.Label(mainframe, text="Answer:").grid(column=1, row=3, sticky=W)
        answer_entry = ttk.Entry(mainframe, textvariable=self.answer, state="readonly")
        answer_entry.grid(column=2, row=3, sticky=(W, E))
        
        # Creates proper spacing and padding for the GUI components
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
       
       # Sets the enter/return key to call the main function
        question_entry.focus()
        root.bind("<Return>", self.main)

    def main(self, *args):
        # Get the user input from the question entry
        userInput = self.question.get().strip()

        # Check if the user input is not empty
        if userInput:
            if self.pending_timezones:
                self.handleTime([userInput])
                self.question.set("")
                return

            # Split the user input into words
            words = userInput.split()

            # Define handlers for different keywords
            handlers = {
                "time": self.handleTime,
            }

            # Check if any of the keywords are present in the user input and call the corresponding handler
            for word in words:
                if word.lower() in handlers:
                    handlers[word.lower()](words)
                    break
            # If no keyword is found, provide a default response
            else:
                self.answer.set("I don't understand your question.")

            self.question.set("")
        else:
            self.answer.set("Please enter a question.")

    def handleTime(self, words):
        # Rejoins the words that were intially split
        userInput = " ".join(words)

        # Check if the user input is a valid timezone
        if self.pending_timezones:
            if userInput in self.pending_timezones:
                response, self.pending_timezones = getTimezone(userInput, self.pending_timezones)
                self.answer.set(response)
            else:
                # If the user input is not in the pending timezones, provide a message
                self.answer.set(f"'{userInput}' is not a valid timezone. Please choose from: {', '.join(self.pending_timezones)}.")
            return

        # Call the getTimezone function from the time_handler module
        response, self.pending_timezones = getTimezone(userInput)

        # If there are pending timezones, show the first three as examples
        if self.pending_timezones:
            self.answer.set(f"{response} (e.g., {', '.join(self.pending_timezones[:3])}...)")
        else:
            # If there are no pending timezones, show the response directly
            self.answer.set(response)

root = Tk()
Chatbot(root)
root.mainloop()