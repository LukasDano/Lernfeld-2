import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import *
import tkinter.messagebox as messagebox
import tkinter as tk
import ScooterRentalAppUi

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ScooterRentalAppUi.ScooterRentalApp()

root = ctk.CTk()
root.title("ScooTeq App")
root.iconbitmap("UiVersion/scooTecIcon.ico")
root.geometry("550x380")

def getUhrzeit():
    now = datetime.now()
    hours = int(now.strftime("%H"))
    minutes = int(now.strftime("%M"))
    seconds = int(now.strftime("%S"))

    return [hours, minutes, seconds]
  
# Windows
frontPage = None
scooterFahrtUebersicht = None
scooterReservierungsUebersicht = None

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

def update_price(updatingLabel):
    currentScooter = app.getScooterById(app.bearbeiteterScooterId)

    timeDifference = app.getTimeDifferance(currentScooter.getAusleihZeitpunkt(), getUhrzeit())
    hours = timeDifference[0]
    minutes = timeDifference[1]
    seconds = getUhrzeit()[2]

    timeInMinutes = hours * 60 + minutes
    if seconds != 0:
        timeInMinutes += 1

    currentPrice = app.getPrice(timeInMinutes)
    currentScooter.setAktuellerPreis(currentPrice)

    updatingLabel.configure(text=f"Aktueller Preis: {currentPrice}€")
    updatingLabel.after(1000, update_price, updatingLabel)

def update_rentTime(updatingLabel):
    currentScooter = app.getScooterById(app.bearbeiteterScooterId)

    time_difference = app.getTimeDifferance(currentScooter.getAusleihZeitpunkt(), getUhrzeit())

    hours_str = f"{time_difference[0]:02}"
    minutes_str = f"{time_difference[1]:02}"
    seconds_str = f"{time_difference[2]:02}"

    displayedTimeText = f"Dauer aktuelle Fahrt: {hours_str}:{minutes_str}:{seconds_str} h"
    updatingLabel.configure(text=displayedTimeText)
    updatingLabel.after(1000, update_rentTime, updatingLabel)

def update_reserveTime(updatingLabel):
    currentScooter = app.getScooterById(app.bearbeiteterScooterId)

    time_difference = app.getTimeDifferance(getUhrzeit(), currentScooter.getReservierungsZeitpunkt())

    hours_str = f"{time_difference[0]:02}"
    minutes_str = f"{time_difference[1]:02}"
    seconds_str = f"{time_difference[2]:02}"

    displayedTimeText = f"Rest Zeit deiner Reservierung: {hours_str}:{minutes_str}:{seconds_str} h"
    updatingLabel.configure(text=displayedTimeText)
    updatingLabel.after(1000, update_reserveTime, updatingLabel)

    if time_difference[0] == 0 and time_difference[1] == 0 and time_difference[2] == 0:
        scooterAusleihenUi(currentScooter.getId())

def getColorForState(id):
    scooter = app.getScooterById(id)

    if scooter.getScooterAusgeliehen() == True:
        return "red"
    elif scooter.getScooterReserviert() == True:
        return "orange"
    elif scooter.getScooterAusgeliehen() == False:
        return "green"

# Ui - Funktionen
def scooterAusleihenUi(id):
    app.scooterAusleihen(id)
    show_frame(scooterFahrtUebersicht)

def scooterReservierenUi(id):
    app.scooterReservieren(id)
    show_frame(scooterReservierungsUebersicht)

def create_frontPage():
    global frontPage
    frontPage = ctk.CTkFrame(master=root)
    frontPage.grid(row=0, column=0, sticky='nsew', pady=20, padx=60)

    upper_frame = ctk.CTkFrame(frontPage)
    upper_frame.grid(row=0, column=0, sticky='nsew', pady=5, padx=35)

    logo_image = Image.open("UiVersion/scooTecLogo.png")  
    logo_image = logo_image.resize((70, 70), Image.LANCZOS)  
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(upper_frame, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=0, column=0, pady=10, padx=10) 

    label = ctk.CTkLabel(upper_frame, text="Willkommen bei der ScooTeq GmbH!", font=("Helvetica", 15, "bold"))
    label.grid(row=0, column=1, pady=12, padx=10)

    down_frame = ctk.CTkFrame(frontPage)
    down_frame.grid(row=1, column=0, sticky='nsew', pady=5, padx=5)
    label = ctk.CTkLabel(down_frame, text="Wähle eine Option:", font=("Helvetica", 15, "bold"))
    label.grid(row=0, column=0 , pady=12, padx=10)

    ausleihen_button = ctk.CTkButton(down_frame, text="Scooter ausleihen", command=lambda: show_frame(avalibleScooter))
    ausleihen_button.grid(row=0, column=1, pady=12, padx=18)

    reservieren_button = ctk.CTkButton(down_frame, text="Scooter reservieren", command = lambda: show_frame(avalibleScooterReservieren))
    reservieren_button.grid(row=1, column=1, pady=12, padx=18)

    beenden_button  = ctk.CTkButton(down_frame, text="App beenden", command=root.destroy)
    beenden_button.grid(row=3, column=1, pady=12, padx=18)


def create_scooterFahrtUebersicht():
    global scooterFahrtUebersicht
    scooterFahrtUebersicht = ctk.CTkFrame(root)
    scooterFahrtUebersicht.grid(row=0, column=0, sticky='nsew', pady=20, padx=60)

    headline = f"Du fährst aktuell mit Scooter: {app.bearbeiteterScooterId}"
    rentedScooterField = ctk.CTkLabel(scooterFahrtUebersicht, text=headline, font=("Calibri", 23))
    rentedScooterField.pack(pady=20)

    dauerAusleihenField = ctk.CTkLabel(scooterFahrtUebersicht, text="", font=("Calibri", 18))
    dauerAusleihenField.pack(pady=1)

    update_rentTime(dauerAusleihenField)

    priceDriveField = ctk.CTkLabel(scooterFahrtUebersicht, text="", font=("Calibri", 18))
    priceDriveField.pack(pady=1)

    update_price(priceDriveField)
    switch_button1 = ctk.CTkButton(scooterFahrtUebersicht, text="Ausleihen beenden.")
    switch_button1.pack(pady=10)
    switch_button2 = ctk.CTkButton(scooterFahrtUebersicht, text="Zur Startseite", command=lambda: show_frame(frontPage))
    switch_button2.pack(pady=10)

def create_scooterReservierungsUebersicht():
    global scooterReservierungsUebersicht
    scooterReservierungsUebersicht = ctk.CTkFrame(root)
    scooterReservierungsUebersicht.grid(row=0, column=0, sticky='nsew', pady=20, padx=60)

    headline = f"Du hast erfolgreich Scooter: {app.bearbeiteterScooterId} reserviert"
    reservedScooterField = ctk.CTkLabel(scooterReservierungsUebersicht, text=headline, font=("Calibri", 23))
    reservedScooterField.pack(pady=20)

    dauerReservierungField = ctk.CTkLabel(scooterReservierungsUebersicht, text="", font=("Calibri", 18))
    dauerReservierungField.pack(pady=1)

    update_reserveTime(dauerReservierungField)

    # TODO Preis macht noch keinen Sinn, muss angepasst werden
    priceRentField = ctk.CTkLabel(scooterReservierungsUebersicht, text="", font=("Calibri", 18))
    priceRentField.pack(pady=1)

    update_price(priceRentField)
    switch_button0 = ctk.CTkButton(scooterReservierungsUebersicht, text="Scooter jetzt ausleihen.", command=lambda: scooterAusleihenUi(app.bearbeiteterScooterId))
    switch_button0.pack(pady=10)
    switch_button1 = ctk.CTkButton(scooterReservierungsUebersicht, text="Reservieren beenden.")
    switch_button1.pack(pady=10)
    switch_button2 = ctk.CTkButton(scooterReservierungsUebersicht, text="Zur Startseite", command=lambda: show_frame(frontPage))
    switch_button2.pack(pady=10)

def create_avalibleScooterReservieren():
    global avalibleScooterReservieren
    avalibleScooterReservieren = ctk.CTkFrame(root)
    avalibleScooterReservieren.grid(row=0, column=0, sticky='nsew', pady=20, padx=60)

    left_frame = ctk.CTkFrame(avalibleScooterReservieren)
    left_frame.grid(row=0, column=0, sticky='nsew', pady=20, padx=20)

    statusColorFirstHalf = [getColorForState(1), getColorForState(2), getColorForState(3), getColorForState(4), getColorForState(5)]

    scooter1Button = ctk.CTkButton(left_frame, text="Scooter 1", fg_color=statusColorFirstHalf[0], command = lambda: scooterReservierenUi(1))
    scooter1Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter2Button = ctk.CTkButton(left_frame, text="Scooter 2", fg_color=statusColorFirstHalf[1], command = lambda: scooterReservierenUi(2))
    scooter2Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter3Button = ctk.CTkButton(left_frame, text="Scooter 3", fg_color=statusColorFirstHalf[2], command = lambda: scooterReservierenUi(3))
    scooter3Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter4Button = ctk.CTkButton(left_frame, text="Scooter 4", fg_color=statusColorFirstHalf[3], command = lambda: scooterReservierenUi(4))
    scooter4Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter5Button = ctk.CTkButton(left_frame, text="Scooter 5", fg_color=statusColorFirstHalf[4], command = lambda: scooterReservierenUi(5))
    scooter5Button.pack(side="top", anchor="w", pady=10, padx=10)

    right_frame = ctk.CTkFrame(avalibleScooterReservieren)
    right_frame.grid(row=0, column=1, sticky='nsew', pady=20, padx=20)

    statusColorSecondHalf = [getColorForState(6), getColorForState(7), getColorForState(8), getColorForState(9), getColorForState(10)]

    scooter6Button = ctk.CTkButton(right_frame, text="Scooter 6", fg_color=statusColorSecondHalf[0], command = lambda: scooterReservierenUi(6))
    scooter6Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter7Button = ctk.CTkButton(right_frame, text="Scooter 7", fg_color=statusColorSecondHalf[1], command = lambda: scooterReservierenUi(7))
    scooter7Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter8Button = ctk.CTkButton(right_frame, text="Scooter 8", fg_color=statusColorSecondHalf[2], command = lambda: scooterReservierenUi(8))
    scooter8Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter9Button = ctk.CTkButton(right_frame, text="Scooter 9", fg_color=statusColorSecondHalf[3], command = lambda: scooterReservierenUi(9))
    scooter9Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter9Button = ctk.CTkButton(right_frame, text="Scooter 10", fg_color=statusColorSecondHalf[4], command = lambda: scooterReservierenUi(10))
    scooter9Button.pack(side="top", anchor="w", pady=10, padx=10)

    back_button_frame = ctk.CTkFrame(avalibleScooterReservieren)
    back_button_frame.grid(row=1, column=0, columnspan=2)

    switch_button2 = ctk.CTkButton(back_button_frame, text="Zurück", command=lambda: show_frame(frontPage))
    switch_button2.pack(pady=10)

def create_avalibleScooter():
    global avalibleScooter
    avalibleScooter = ctk.CTkFrame(root)
    avalibleScooter.grid(row=0, column=0, sticky='nsew', pady=20, padx=60)

    left_frame = ctk.CTkFrame(avalibleScooter)
    left_frame.grid(row=0, column=0, sticky='nsew', pady=20, padx=20)

    statusColorFirstHalf = [getColorForState(1), getColorForState(2), getColorForState(3), getColorForState(4), getColorForState(5)]

    scooter1Button = ctk.CTkButton(left_frame, text="Scooter 1", fg_color=statusColorFirstHalf[0], command = lambda: scooterAusleihenUi(1))
    scooter1Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter2Button = ctk.CTkButton(left_frame, text="Scooter 2", fg_color=statusColorFirstHalf[1], command = lambda: scooterAusleihenUi(2))
    scooter2Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter3Button = ctk.CTkButton(left_frame, text="Scooter 3", fg_color=statusColorFirstHalf[2], command = lambda: scooterAusleihenUi(3))
    scooter3Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter4Button = ctk.CTkButton(left_frame, text="Scooter 4", fg_color=statusColorFirstHalf[3], command = lambda: scooterAusleihenUi(4))
    scooter4Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter5Button = ctk.CTkButton(left_frame, text="Scooter 5", fg_color=statusColorFirstHalf[4], command = lambda: scooterAusleihenUi(5))
    scooter5Button.pack(side="top", anchor="w", pady=10, padx=10)

    right_frame = ctk.CTkFrame(avalibleScooter)
    right_frame.grid(row=0, column=1, sticky='nsew', pady=20, padx=20)

    statusColorSecondHalf = [getColorForState(6), getColorForState(7), getColorForState(8), getColorForState(9), getColorForState(10)]

    scooter6Button = ctk.CTkButton(right_frame, text="Scooter 6", fg_color=statusColorSecondHalf[0], command = lambda: scooterAusleihenUi(6))
    scooter6Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter7Button = ctk.CTkButton(right_frame, text="Scooter 7", fg_color=statusColorSecondHalf[1], command = lambda: scooterAusleihenUi(7))
    scooter7Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter8Button = ctk.CTkButton(right_frame, text="Scooter 8", fg_color=statusColorSecondHalf[2], command = lambda: scooterAusleihenUi(8))
    scooter8Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter9Button = ctk.CTkButton(right_frame, text="Scooter 9", fg_color=statusColorSecondHalf[3], command = lambda: scooterAusleihenUi(9))
    scooter9Button.pack(side="top", anchor="w", pady=10, padx=10)

    scooter10Button = ctk.CTkButton(right_frame, text="Scooter 10", fg_color=statusColorSecondHalf[4], command = lambda: scooterAusleihenUi(10))
    scooter10Button.pack(side="top", anchor="w", pady=10, padx=10)

    back_button_frame = ctk.CTkFrame(avalibleScooter)
    back_button_frame.grid(row=1, column=0, columnspan=2)

    switch_button2 = ctk.CTkButton(back_button_frame, text="Zurück", command=lambda: show_frame(frontPage))
    switch_button2.pack(pady=10)

def popupNachricht():
    messagebox.showinfo("Scooter nicht verfügbar", "Scooter nicht verfügbar, bitte einen grünen Scooter auswählen")    



def show_frame(frame):
    update_frames()

    frame.tkraise()

def update_frames():
    create_frontPage()

    create_scooterFahrtUebersicht()
    create_scooterReservierungsUebersicht()

    create_avalibleScooter()
    create_avalibleScooterReservieren()

def runApp():
    update_frames()

    show_frame(frontPage)
    root.mainloop()

runApp()


# TODO BearbeitungsId ersetzen/verbessern
# TODO Preis bei der Reservierung richtig darstellen