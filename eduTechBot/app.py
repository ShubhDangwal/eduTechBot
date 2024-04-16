import csv
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from chat import load_chatbot_resources, chatbot_response, fallback_answers
from datetime import datetime
import random
import os
import pickle

bot_name = "LearnHub Assistant"
device, patterns_dict, intents, all_words, tags, model = load_chatbot_resources()
fallback_dict = {}
if os.path.exists("fallback_tracing.pkl"):
    with open("fallback_tracing.pkl", "rb") as file:
        fallback_dict = pickle.load(file)
class ChatbotGUI:
    faqs = [
        "Suitable for beginner or advanced users?",
        "Can I learn at my own pace?",
        "What type of assignment do you give?",
        "What are the prerequisites for this course?",
        "How long does this course take to complete?",
        "How much does the course cost?",
        "How is the doubt support?",
        "Does this course offer placement opportunities?",
        "How is the course different from other platform courses?",
        "Is there any money-back guarantee if I do not like the course?",
        "Is this course relevant in today's market?",
        "Is good DSA a prerequisite for this course?",
        "How much can I make after completing this course?",
        "Can I pay in EMI for this course?",
        "Does this course offer financial aid for underprivileged people?",
        "Does this course offer any certificate?",
        "Where can I get testimonials for this course?",
        "Who is the mentor for this course?",
        "Is it an online or offline course?"
    ]

    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        self.popup = None  
        self.get_name_popup()
        self.understanding_count = 0
        self.total_interactions = 0
        self.faq_miss = 0
        self.chat_history_file = None
        self.feedback = "Not responded"

    def encrypt_data(self, data):
        # Simple encryption using a substitution cipher
        encrypted_data = ''.join(chr(ord(char) + 1) for char in data)
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        # Simple decryption for the substitution cipher
        decrypted_data = ''.join(chr(ord(char) - 1) for char in encrypted_data)
        return decrypted_data

    def get_name_popup(self):
        self.popup = tk.Toplevel(self.master)
        self.popup.title("Welcome!")
        self.popup.geometry("300x150")

        label = tk.Label(self.popup, text="Welcome to LearnHub! Please enter your name:")
        label.pack(padx=10, pady=10)

        self.name_entry = tk.Entry(self.popup)
        self.name_entry.pack(padx=10, pady=5)

        submit_button = tk.Button(self.popup, text="Submit", command=self.save_name)
        submit_button.pack(pady=5)

    def save_name(self):
        self.user_name = self.name_entry.get()
        if self.user_name:
            self.master.title(f"Chatbot - Welcome, {self.user_name}!")
            self.init_chatbot_ui()
            self.popup.destroy()  

            # Create CSV file for chat history
            self.chat_history_file = f"{self.user_name}_chat_history.csv"
            with open(self.chat_history_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                encrypted_user_name = self.encrypt_data('User')
                encrypted_message = self.encrypt_data('Message')
                encrypted_response = self.encrypt_data('Bot Response')
                writer.writerow([encrypted_user_name, encrypted_message, encrypted_response])

    def init_chatbot_ui(self):
        self.chat_history = ScrolledText(self.master, state='disabled', height=30, width=150)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.faq_display = ScrolledText(self.master, state='normal', height=10, width=150)
        self.faq_display.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.input_field = tk.Entry(self.master, width=80)
        self.input_field.grid(row=2, column=0, padx=5, pady=5)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=1, padx=5, pady=5)

        self.display_faqs()

    def send_message(self):
        message = self.input_field.get()
        if message:
            self.chat_history.configure(state='normal')
            self.chat_history.insert(tk.END, f"{self.user_name}: {message}\n")  # Add user's name before the message
            self.input_field.delete(0, tk.END)

            # Check if the message is not in FAQs
            if message not in self.faqs:
                self.update_faqs(message)
                self.faq_miss += 1

            response = self.get_bot_response(message)
            if response != f"{bot_name}: I do not understand...":
                self.understanding_count += 1
            else :
                if message in fallback_dict :
                    response = f"{bot_name}: {fallback_dict[message]}"
                    self.understanding_count += 1
                else : 
                    random.shuffle(fallback_answers)
                    response = f"{bot_name}: {fallback_answers[0]}"
                    fallback_dict[message] = fallback_answers[0]
            
            self.chat_history.insert(tk.END, f"{response}\n")  # Add user's name before the response
            self.chat_history.configure(state='disabled')


            # Increment total interactions
            self.total_interactions += 1

            # Append chat history to CSV file
            with open(self.chat_history_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                encrypted_user_name = self.encrypt_data(self.user_name)
                encrypted_message = self.encrypt_data(message)
                encrypted_response = self.encrypt_data(response)
                writer.writerow([encrypted_user_name, encrypted_message, encrypted_response])

    def get_bot_response(self, message):
        return chatbot_response(message, bot_name, device, patterns_dict, intents, all_words, tags, model)

    def display_faqs(self):
        for i, faq in enumerate(self.faqs, start=1):
            self.faq_display.insert(tk.END, f"{faq}\n", f"faq_{i}")
            self.faq_display.tag_bind(f"faq_{i}", "<Button-1>", lambda event, faq=faq: self.select_faq(event, faq))

        self.faq_display.configure(state='disabled')

    def update_faqs(self, new_question):
        # Add the new question to the FAQs list
        self.faqs.append(new_question)
        
        # Clear the current display of FAQs
        self.faq_display.configure(state='normal')
        self.faq_display.delete('1.0', tk.END)
        
        # Display the updated list of FAQs
        for i, faq in enumerate(self.faqs, start=1):
            self.faq_display.insert(tk.END, f"{faq}\n", f"faq_{i}")
            self.faq_display.tag_bind(f"faq_{i}", "<Button-1>", lambda event, faq=faq: self.select_faq(event, faq))

        self.faq_display.configure(state='disabled')

    def select_faq(self, event, faq):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(tk.END, faq.strip())

    def exit_chatbot(self):
        rating = messagebox.askquestion("Rating", "Please rate your experience with the chatbot:")
        if self.total_interactions > 0 :
            understanding_rate = (self.understanding_count / self.total_interactions) * 100
        else :
            understanding_rate = 0
        if self.total_interactions > 0 :
            faq_coverage = (self.faq_miss / self.total_interactions) * 100
        else :
            faq_coverage = 0
        user_rating = 0
        user_satisfaction_rate = 0

        if rating == 'yes':
            rating_popup = tk.Toplevel(self.master)
            rating_popup.title("Rating")
            rating_popup.geometry("300x150")

            label = tk.Label(rating_popup, text="Please rate your experience (out of 5 stars):")
            label.pack(padx=10, pady=10)

            self.rating_entry = tk.Entry(rating_popup, width=5)
            self.rating_entry.pack(padx=10, pady=5)

            submit_button = tk.Button(rating_popup, text="Submit", command=self.show_feedback_popup)
            submit_button.pack(pady=5)

            rating_popup.mainloop()  # Ensure the popup window remains open

            #----.get() causing error due to library malfunction or any other unknown reason----#
            # try:
            #     user_rating = int(self.rating_entry.get())
            #     user_satisfaction_rate = (user_rating / 5) * 100
            # except AttributeError:
            #     pass

        # Store metrics in a CSV file
        with open('chatbot_metrics.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                datetime.now(), 
                understanding_rate, 
                faq_coverage, 
                user_rating, 
                user_satisfaction_rate, 
                self.feedback
            ])

    def rating_popup_closed(self):
        self.rating_popup_closed = True

    def show_feedback_popup(self):
        if hasattr(self, 'rating_popup_closed') and self.rating_popup_closed:
            rating = self.rating_entry.get()
            if rating.isdigit() and 1 <= int(rating) <= 5:
                feedback_popup = tk.Toplevel(self.master)
                feedback_popup.title("Feedback")
                feedback_popup.geometry("300x150")

                label = tk.Label(feedback_popup, text="Please provide your feedback:")
                label.pack(padx=10, pady=10)

                self.feedback_entry = tk.Entry(feedback_popup, width=30)
                self.feedback_entry.pack(padx=10, pady=5)

                submit_button = tk.Button(feedback_popup, text="Submit", command=self.save_feedback)
                submit_button.pack(pady=5)

                feedback_popup.mainloop()  # Ensure the popup window remains open
            else:
                messagebox.showerror("Error", "Please enter a valid rating (1-5 stars).")
        else:
            messagebox.showerror("Error", "Please rate your experience first.")

    def save_feedback(self):
        self.feedback = self.feedback_entry.get()
        # Save feedback to a file or database
        messagebox.showinfo("Thank You!", "Thank you for your feedback!")
        with open("fallback_tracing.pkl", "wb") as file:
            pickle.dump(fallback_dict, file)
        self.master.destroy()  # Close the main window after receiving feedback



root = tk.Tk()
app = ChatbotGUI(root)
root.protocol("WM_DELETE_WINDOW", app.exit_chatbot)
root.mainloop()
