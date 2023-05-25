import urllib.parse
import requests
import tkinter as tk
from PIL import ImageTk, Image
import textwrap

def send_request():
    clear_response()
    question = input_field.get()
    encoded_question = urllib.parse.quote(question)
    api_url = f"https://serai.pro/thunderbird?key=a49fa4fc7e5f1669771a1af6025511bc&thunderbird={encoded_question}"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            answer = response.text.strip()
            show_processing_gif()
            root.after(3000, lambda: show_response(answer))
        else:
            clear_response()
            answer_label.config(text="Ein Fehler ist aufgetreten beim Verarbeiten der Anfrage.")
    except requests.exceptions.RequestException:
        clear_response()
        answer_label.config(text="Ein Fehler ist aufgetreten beim Verarbeiten der Anfrage.")

def show_processing_gif():
    processing_label.place(x=root.winfo_width() // 2, y=root.winfo_height() // 2, anchor="center")
    animate_processing_gif(0)

def animate_processing_gif(index):
    processing_label.config(image=processing_frames[index])

    index += 1
    if index == len(processing_frames):
        index = 0

    root.after(250, lambda: animate_processing_gif(index))

def show_response(answer):
    processing_label.place_forget()
    wrapped_answer = "\n".join(textwrap.wrap(answer, width=(root.winfo_width() - 100) // 12))
    answer_label.config(text=wrapped_answer)
    answer_label.place(x=root.winfo_width() // 2, y=root.winfo_height() // 2, anchor="center")

def clear_response():
    answer_label.config(text="")

def clear_fields():
    input_field.delete(0, tk.END)
    clear_response()

root = tk.Tk()
root.title("serAI App Example")
root.geometry("800x800")
root.attributes("-fullscreen", False)
root.state('zoomed')
root.configure(bg='white')

processing_frames = []
processing_gif = Image.open("processing.gif")
try:
    while True:
        processing_frames.append(ImageTk.PhotoImage(processing_gif))
        processing_gif.seek(processing_gif.tell() + 1)
except EOFError:
    pass

processing_label = tk.Label(root, image="", bg="white")
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Nachricht:", bg="white")
input_label.pack(side=tk.LEFT)

input_field = tk.Entry(input_frame)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(root, text="Send", command=send_request)
send_button.pack(pady=10)

answer_label = tk.Label(root, text="", bg="white", wraplength=root.winfo_width() - 100, justify="center")
answer_label.pack()

clear_fields()

root.mainloop()
