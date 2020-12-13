from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as tmsg
import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt 
# import os


p = pyaudio.PyAudio()

fs = 20000       # sampling rate, Hz, must be integer
duration = 1.5   # in seconds, may be float 

graphLeft = [0,0,0,0,0,0]              #list for graph
graphRight = [0,0,0,0,0,0]              #list for graph

freq =[250,500,1000,2000,4000,8000]     #frequency storage 
Int = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]         #intensity storage
# Int = [0.067,0.134,0.201,0.268,0.335,0.402,0.469,0.536,0.603,0.67,0.737,0.804,0.871,0.938,1]         #intensity storage


i = 0        #in func1
f = 0        #frequency index
vol = 0      # intensity index

earStatus = 'left'
button_test = 0  #For submit button 1 purpose
test = 0  #For submit button 2 purpose
tab_test = 0
    

# ===========================

def secWindow():
    # print("This is Func")
    # Label (root, text= 'Func', bg = "orange",fg = "white",font = "lucida 9 ").place(x= 280,y = 70 ) 
    frame_3 = Frame(root, bg = "light gray").place(x = 0,y=0,width= 600, height = 650)
    topFrame = Frame(frame_3,borderwidth=4,bg="grey" ,relief=SUNKEN)
    topFrame.place(x = 0,y=0,width= 600, height = 30)
    Label(topFrame,text= 'Welcome To Audiometry',fg = "orange",font = "lucida 12 bold",bg = "gray").pack()
    Label (frame_3,text= 'Report',fg = "black",font = "lucida 15 bold",bg = "light gray").place(x = 250,y=40)

    infoFrame = Frame(frame_3, bg = "gray")
    infoFrame.place(x = 110,y=150,width= 380, height = 350)
    f = open(f"text_files/{name.get()}_{age.get()}.txt", "r")
    if f.mode == "r":
        cnt = f.read()
        Label(infoFrame, text = cnt , bg = "gray", font = " lucida 12 bold", fg = "yellow").place(x = 10,y=10)
        # print(cnt)



# ===========================

# ====================== Function for 'start Button' =====================
def patientInfo():
    
    global tab_test
    global name
    global age
    global button_test
    if tab_test == 0:
        top = Toplevel()
        # global tab_test
        tab_test = 1
        # Function for 'Submit Button' in second window
        def submitSecwindow():
            global name
            global age
            if name.get() == "" or age.get() == "" :
                tmsg.showerror("Warning.", "Both the fields are mandatory.")
            elif not age.get().isdigit():
                tmsg.showerror("Warning.", "Age must be Integer.")
            else:     
                global button_test
                button_test = 1 
                print(button_test)     
                tmsg.showinfo("Your Responce is recorded", " Please put Head Phone in LEFT EAR to start the Test.")
                Label(root,text="Testing for => Left Ear.", bg ="blue", fg = "white", font="lucida 8 bold" ).place(x = 5 , y = 35 ,width = 133, height = 20)
                text = open(f"text_files//{name.get()}_{age.get()}.txt","w+")
                text.write("Left Ear: \n")
                text.close()
                top.destroy()
        
        top.geometry("300x130")
        top.minsize(300,130)
        top.maxsize(300,130)
        top.title("Patient Information.")
        top.config(bg = "black")
        top.wm_iconbitmap("imageAud//icon11.ico")
    
        Label (top, text= 'Enter your Name: ', bg = "black",fg = "white",font = "lucida 9 ").place(x= 10,y = 10 ) 
        Entry(top, textvariable = name,font = "lucida 10 bold ",bg = "white" ).place(x = 130, y= 10)
        Label (top, text= 'Enter your Age: ',bg = "black",fg = "white",font = "lucida 10 ").place(x= 10,y = 40 )
        Entry(top, textvariable = age,font = " lucida 9 bold ",bg = "white" ).place(x = 130, y = 40)
        Button(top, text = "Submit",bg = "light green" , command = submitSecwindow).place(x= 130,y = 80, width = 70 , height = 30)
        top.mainloop()
    elif tab_test == 1:
        button_test = 1
        tmsg.showwarning("Audiometry","You have already start the test.")

# =========================== Function for 'Play Button'======================
def playFreq():
    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*freq[f]/fs)).astype(np.float32)
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output = True)                                                     
    # play. May repeat with different volume values (if done interactively) 
    if button_test ==1:
        stream.write(Int[vol]*samples)

        can_widget = Canvas(root, width = 20, height = 20, bg = "white")
        can_widget.place(x =285 , y = 320)
        can_widget.create_oval( 5,5,20,20, fill="red")
        can_widget.update()
        time.sleep(0.25)
        can_widget.create_oval(5,5,20,20,fill="white")
    else:
        print(button_test)
        tmsg.showinfo("Audiometry","Click on Start Button first." )        

    

    # ================Function for (Hear Succesfully) button =========================
def hearSuccesfully():  
    global f
    global vol
    global i
    global earStatus
    global test

    if button_test ==1:
        with open(f"text_files//{name.get()}_{age.get()}.txt","a") as File:
            File.write(f"frequency {freq[f]} Hz is Audible at Intensity {Int[vol]}.\n") 

        if earStatus == "left":
            graphLeft[i] = Int[vol]
        else:
            graphRight[i] = Int[vol]

        i = i+1
        f = f+1
        test = test +1
        if f == 6:
            f = 0
            i = 0
            test = test -1
            if earStatus == 'left':
                tmsg.showinfo("You are done with Test of LEFT EAR.","Now, Please put Head Phone on RIGHT EAR.")
                Label(root,text="Testing for => Right Ear.", bg ="red", fg = "white", font="lucida 8 bold").place(x = 5 , y = 35 ,width = 133, height = 20)
                earStatus = 'right'
                text = open(f"text_files//{name.get()}_{age.get()}.txt","a")
                text.write("\n Right Ear: \n")
            else:
                tmsg.showinfo("You are done with Test of RIGHT EAR.","Now, Please click on Submit button.")

            # Label (freqDisplay,text= "0",fg = "black",bg = "light gray",font = "lucida 15").place( x= 135,y = 1.5 )
        vol = 0 
        Label (freqDisplay,text= freq[f],fg = "black",bg = "light gray",font = "lucida 15").place( x= 135,y = 1.5,width = 50 )
        Label (intDisplay,text= Int[vol],fg = "black",font = "lucida 15",bg = "light gray").place(x= 135,y = 1.5 )
    else:
        tmsg.showinfo("Audiometry","Click on Start Button first.")

# ====================Function for (Unable to Hear) button =====================
def unableToHear():
    global vol
    global f
    if button_test == 1:
        vol = vol + 1
        if vol == 6:
            f = f+1 
            Label (freqDisplay,text= freq[f],fg = "black",bg = "light gray",font = "lucida 15").place( x= 135,y = 1.5 ,width = 50)
            vol = 0
        Label (intDisplay,text= Int[vol],fg = "black",font = "lucida 15",bg = "light gray").place(x= 135,y = 1.5 )
    else:
        tmsg.showinfo("Audiometry","Click on Start Button first.")

# ============= Submit button function ===============================
def submitButton():
    # addr= f"E:\\Python\\text_files\\{name.get()}_{age.get()}.txt"
    # os.startfile(addr)
    global secWindow
    if test == 10:
        secWindow()
        plt.plot(freq, graphLeft, label = "Left Ear")
        plt.plot(freq, graphRight, label = "Right Ear")
        # naming the x axis 
        plt.xlabel('Frequency') 
        # naming the y axis 
        plt.ylabel('Intensity')
        # giving a title to my graph 
        plt.title('Audiogram') 
        plt.legend() 
        # function to show the plot 
        plt.show()

    else:
        tmsg.showwarning("Warning", "Complete the test first.")
    
#  ======================= Reset Function ==============================
def reset():
    global f
    global vol
    if button_test == 1:
        f = 0
        vol = 0
        graphLeft = [0,0,0,0,0,0]
        graphRight = [0,0,0,0,0,0]
        Label(root,text="Testing for => Left Ear.", bg ="blue", fg = "white", font="lucida 8 bold" ).place(x = 5 , y = 35 ,width = 133, height = 20)
        Label (intDisplay,text= Int[vol],fg = "black",font = "lucida 15",bg = "light gray").place(x= 135,y = 1.5 )
        Label (freqDisplay,text = freq[f],fg = "black",bg = "light gray",font = "lucida 15").place( x= 135,y = 1.5, width = 50 )
    else:
        tmsg.showinfo("Audiometry", "Click on Start Button first.")    
    


# ========================== helpMenu Function ============================

def helpMenu():
    pass




    
# ################################################################################################# 
#  ##################################=== Main Function  ===########################################
# ################################################################################################# 

if __name__ == "__main__":

    root = Tk()

    root.geometry("600x650")

    root.minsize(600,650)

    root.maxsize(600,650)

    root.title("AudioMetry!")
    root.wm_iconbitmap("imageAud//icon11.ico")
    root.configure( background = "white")

    name = StringVar()
    age = StringVar()

    mainManu = Menu(root)
    m1 = Menu(mainManu,tearoff=0)
    m1.add_command(label='Help',command=helpMenu)
    mainManu.add_cascade(label = "Help")
    root.config(menu=mainManu)

    bottomFrame = Frame(root,borderwidth=4,bg="gray",relief=RIDGE)
    # bottomFrame.pack(side=BOTTOM, anchor='w',fill='x')
    bottomFrame.place(x = 0,y=625,width= 600, height = 25)
    Label (bottomFrame,text= 'Nikhil',bg = "gray",font = "lucida 10 bold").pack(anchor = "e")
    topFrame = Frame(root,borderwidth=4,bg="light gray" ,relief=SUNKEN)
    topFrame.place(x = 0,y=0,width= 600, height = 30)
    Label (topFrame,text= 'Welcome To Audiometry',fg = "red",font = "lucida 12 bold",bg = "light gray").pack()    


# ==================Start Button (Image)====================
    
    image = Image.open("imageAud//st5.png")
    image = image.resize((150, 50), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    Button(root, image = img,bd=0 ,cursor = "hand2",command=patientInfo).place(x= 225,y = 40 )

# ======================  Frequency part =====================
    border = Frame(root,borderwidth=4,bg="gray").place(x= 83,y = 148 ,width = 204, height = 44)
    freqDisplay = Frame(root,borderwidth=4,bg="light gray" )
    freqDisplay.place(x= 85,y = 150 ,width = 200, height = 40)
    Label (freqDisplay,text= 'Frequency: ',fg = "black",bg = "light gray",font = "lucida 15").place(x= 20,y = 1.5 ) 
    Label (freqDisplay,text= freq[f],fg = "black",bg = "light gray",font = "lucida 15").place(x= 135,y = 1.5 , width = 50 ) 


# ========================= Intensity Part  ========================
    border = Frame(root,borderwidth=4,bg="gray").place(x= 313,y = 148 ,width = 204, height = 44)
    intDisplay = Frame(root,borderwidth=4,bg="light gray" )
    intDisplay.place(x= 315,y = 150 ,width = 200, height = 40)
    Label (intDisplay,text= 'Intensity: ',fg = "black",font = "lucida 15",bg = "light gray").place(x= 20,y = 1.5 )
    Label (intDisplay,text= Int[vol],fg = "black",font = "lucida 15",bg = "light gray").place(x= 135,y = 1.5 )

# ========================== play button (image) =================
    playBut = Image.open("imageAud//play1.png") 
    playBut = playBut.resize((130, 70), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(playBut)
    Button(root, image = img2,bd=0 ,cursor = "hand2",command=playFreq).place(x = 230 , y = 210)    

    # =============== play button lable===============
    Label(root, text = "Play Button",font="lucida 8 bold",fg = 'black', bg = "white" ).place(x =265 , y = 290)


# ========================= Varify Section. ==================
    varification = Frame(root,borderwidth=4,bg="dark orange" )
    varification.place(x= 100,y = 390 ,width = 400, height = 50)

    #============= varification lable ====================== 
    Label (varification,text= 'Varification',fg = "black",bg = "dark orange",font = "lucida 17 bold").place(x= 140,y = 2.3 )        

                    # ================Buttons===============
    Button(root,text="Hear Succesfully", bg ="green", fg = "white", font="bold" ,cursor = "hand2",command = hearSuccesfully ).place(x = 150 , y = 460 ,width = 120, height = 70)
    Button(root,text="Unable to Hear", bg ="red", fg = "white", font="bold" ,cursor = "hand2",command = unableToHear).place(x = 350 , y = 460 ,width = 120, height = 70)
    

    # Label (root ,text= 'Responce Rcorded!!! ',fg = "black",font = "lucida 10 bold").place(x=230 ,y = 545)

    # ======================== Sound Indicator(canvas)====================
    can_widget = Canvas(root, width= 20, height= 20, bg = "white", bd = 0)
    can_widget.place(x =285 , y = 320)
    can_widget.create_oval(5,5,20,20,fill="white")

    # =============== Sound Indicator lable===============
    Label(root, text = "Sound Indicator",font="lucida 8 bold",fg = 'black', bg = "white" ).place(x =255 , y = 350)
    
    # ============= Submit Button=====================
    Button(root,text="Submit Test", bg ="sky blue", fg = "black", font="lucida 10 bold" ,cursor = "hand2",command = submitButton).place(x = 225 , y = 560 ,width = 150, height = 40)

    # ============= Reset Button=====================
    Button(root,text="Reset.", bg ="dark red", fg = "white", font="lucida 8 bold" ,cursor = "hand2",command = reset).place(x = 545 , y = 35 ,width = 50, height = 20)
    
    print(earStatus)
    root.mainloop()

# ===============================================================================================================
#  ============================================= End of code ====================================================
# ===============================================================================================================



