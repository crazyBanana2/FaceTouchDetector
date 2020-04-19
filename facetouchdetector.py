from tkinter import *
from PIL import ImageTk, Image
import os
import time
from Callers import Locate

#MODEL init
a = Locate()
frame = None
lastAlertTime = 10


#UI init
color = "white"
font = "Sans-serif"
settings = {'notif': 0, 'sound': 0}
root = Tk()
notif_var = IntVar()
sound_var = IntVar()

print("/" * 50)
print("/" * 50)
print("Be sure to turn on your notifications")
print("The program will now run and be able to detect if you have touched your face\n")
print("Try to move to well lit area for the application to work best")
print("/" * 50)
print("/" * 50)

def alert():
    if notif_var.get() == 1:
        os.system("""
                      osascript -e 'display notification "Stop touching face" with title "FaceTouchDetector"'
                      """.format("Stop touching your face", "FaceTouchDetector"))
    if sound_var.get() == 1:
        os.system('say "Stop touching your face."')

def center():
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def get_settings():
    file = open("settings.txt", "r")
    data = file.readlines()

    if(data[0].count('1') == 1):
        settings['notif'] = 1
    if(data[1].count('1') == 1):
        settings['sound'] = 1

def init_boxes(notif_var, sound_var):
    if(settings['notif'] == 0):
        notif_var.set(0)
    else:
        notif_var.set(1)
    if(settings['sound'] == 0):
        sound_var.set(0)
    else:
        sound_var.set(1)

def change_notif():
    file = open("settings.txt", "w")
    if(notif_var.get() == 0):
        file.write("'notif': 0")
        settings['notif'] = 0
    else:
        file.write("'notif': 1")
        settings['notif'] = 1
    file.write("\n'sound': " + str(settings['sound']))
    file.close()

def change_sound():
    file = open("settings.txt", "w")
    file.write("'notif': " + str(settings['notif']))
    if(sound_var.get() == 0):
        file.write("\n'sound': 0")
        settings['sound'] = 0
    else:
        file.write("\n'sound': 1")
        settings['sound'] = 1
    file.close()

def main():
    global lastAlertTime
    root.geometry("450x280")
    root.resizable(False, False)
    root.title("Face Touch Detector v0.1.0")
    root.iconbitmap("Logo.ico")
    root.configure(background = color)
    #center()

    warning_image = ImageTk.PhotoImage(Image.open("Warning.png"))
    warning_label = Label(image=warning_image)
    warning_label.place(x = 23, y = 60)

    title = Label(root, text = "Face Touch Detector Settings")
    title.place(x = 28, y = 10)
    title.config(font = (font, 30))
    title.config(bg = color)

    settings_label = Label(root, text = "Enable:")
    settings_label.place(x = 268, y= 100)
    settings_label.config(font = (font, 25))
    settings_label.config(bg = color)
    
    notif = Checkbutton(root, text = "Notifications", variable = notif_var, bg = color, onvalue = 1, offvalue = 0, command = change_notif)
    notif.place(x = 270, y = 135)
    notif.config(font = (font, 20))

    sound = Checkbutton(root, text = "Sound", variable = sound_var, bg = color, onvalue = 1, offvalue = 0, command = change_sound)
    sound.place(x = 270, y = 160)
    sound.config(font = (font, 20))

    root.after(0, task)
    root.mainloop()

def task():
    global lastAlertTime
    while True:
        testImg = a.getpicfromCamera()
        handMap = a.gethandProbMap(frame=testImg)
        faceCoordinate = a.getfacecoordinates(frame=testImg)
        is_touching_face = a.getOverLapDiagnostic(handMap, faceCoordinate)

        if lastAlertTime < time.time() - 7 and is_touching_face:
            alert()
            lastAlertTime = time.time()
        root.update()
get_settings()
init_boxes(notif_var, sound_var)
main()