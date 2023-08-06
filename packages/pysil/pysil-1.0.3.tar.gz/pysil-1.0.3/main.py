import random
import string

# module mot de passe
from tkinter import *

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def generate_random_password():
    global characters
    min = 12
    max = 13
    length = int(random.randint(min, max))
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    print("".join(password))


generate_random_password()

# créer la fenêtre

window = Tk()

# personnaliser la fenêtre

window.title("Générateur de mot de passe ")
window.geometry("1920x1080")
window.iconbitmap("Logo_lfp.ico")
window.config(background='#ff4145')

# créer la frame principal
main_frame = Frame(window, bg='#ff4145')

# insérer une image
width = 512
height = 512
image1 = PhotoImage(file="hacker.png")
canvas = Canvas(main_frame, width=width, height=height, bg='#ff4145', bd=0, highlightthickness=0)
canvas.create_image(width / 2, height / 2, image=image1)
canvas.grid(row=0, column=0, sticky=W)

# sous-boite
right_frame = Frame(main_frame, bg='#ff4145', bd=1, relief=SUNKEN)

# titre
label_title = Label(right_frame, text="Mot de passe : ", font=("Helvetica", 20), bd=0, bg='#ff4145', fg='black')
label_title.pack(pady=25)
# créer un champs
passworld_entry = Entry(right_frame, font=("Helvetica", 20), bd=0, bg='#e9efff', fg='black')
passworld_entry.pack()
# créer un bouton
button_generator = Button(right_frame, text="Générer", font=("Helvetica", 20), bd=0, bg='#d3dcfb', fg='black',
                          command=generate_random_password)
button_generator.pack(pady=25, fill=X)
# on place la sous-boite à droite de la frame principal
right_frame.grid(row=0, column=1, sticky=W)

# ouvrir la fenêtre :
main_frame.pack(expand=YES)
window.mainloop()
label_title.pack()
