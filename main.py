from tkinter import *
import math
from PIL import ImageTk, Image
import os
import time
import pygame

PINK="#e2979c"
RED="#e7305b"
GREEN="#9bdeac"
BLACK="#000000"
FONT_NAME="Courier"
WORK_MIN=0.05
SHORT_BREAK_MIN=0.05
LONG_BREAK_MIN=1
reps=0
timer=None
angle=0
total_time=0

#intialize pygame for sound
pygame.mixer.init()

#Function to play sound
def play_sound(file, callback=None): 
    def check_playing():
        if not pygame.mixer.music.get_busy():   # Check if sound has finished
           if callback:
               window.after(2000, callback)      # Call the callback after a delay
        else:
            window.after(100, check_playing)
    def start_playing():
       pygame.mixer.music.load(file)         # Load sound file
       pygame.mixer.music.play()          # Play sound
       window.after(100, check_playing)    # Check sound status  
    if not pygame.mixer.get_init():
        pygame.mixer.init()                # Initialize pygame mixer if not already done
    window.after(2000, start_playing)       # Start sound with a 2-second delay  

#Rotate the pomodoro image continuously
def rotate_pomodoro(elapsed,duration):
    global angle, pomodoro_image, rotated_image
    angle=(elapsed/duration)*360                # Calculate the angle based on elapsed time 
    rotated=pomodoro_image.rotate(angle, resample=Image.Resampling.BICUBIC)        # Rotate the image
    rotated_image=ImageTk.PhotoImage(rotated)             # Convert rotated image for tkinter
    canvas.itemconfig(image_id, image=rotated_image)       # Update image in canvas

#Reset the timer
def reset_timer():
    global timer, angle, reps
    if timer:   
        window.after_cancel(timer)      # Cancel any active timer
    canvas.itemconfig(timer_text, text="00:00")          # Reset displayed time
    title_label.config(text="Timer", font=(FONT_NAME, 50, "bold"), fg=GREEN, bg=BLACK)      # Reset title
    angle=0        # Reset rotation angle  
    reps=0         # Reset number of sessions
    timer=None     # Clear timer
    rotated_image=ImageTk.PhotoImage(pomodoro_image)      # Reset image
    canvas.itemconfig(image_id, image=rotated_image)      # Update canvas image
#Start the timer
def start_timer():
    global reps, total_time
    reps+=1       # Increment the session count
    work_sec=WORK_MIN*60
    short_break_sec=SHORT_BREAK_MIN*60
    long_break_sec=LONG_BREAK_MIN*60
    if reps%8==0:
        title_label.config(text="Break", fg=RED)
        total_time=long_break_sec
        count_down(long_break_sec)
    elif reps%2==0:
        title_label.config(text="BREAK", fg=PINK)
        total_time=short_break_sec
        count_down(short_break_sec)
    else:        
        title_label.config(text="Work", fg=GREEN)
        total_time=work_sec
        count_down(work_sec)

#Countdown mechanism    
def count_down(count):
    global total_time
    minutes=math.floor(count/60)
    seconds=count%60
    if seconds<10:
        seconds=f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")        # Update timer display
    elapsed_time = total_time - count
    rotate_pomodoro(elapsed_time, total_time)    # Rotate image based on time elapsed
    if count>0:
        global timer
        timer=window.after(1000, count_down, count-1)     # Decrease time every second
    else:
        if reps % 8 == 0 or reps % 2 == 0:  # After break phase
            play_sound(r"D:\Python's -- 100 Days of Code\Music\bedside-clock-alarm-95792.mp3", start_timer)
        else:  # After work phase
            play_sound(r"D:\Python's -- 100 Days of Code\Music\cyber-alarms-synthesized-116358.mp3", start_timer)
#Create the main window
window=Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=BLACK)

#Title label
title_label=Label(text="Timer", font=(FONT_NAME, 50, "bold"), fg=GREEN, bg=BLACK)
title_label.grid(column=1, row=0)

#Canvas & image
canvas=Canvas(width=400, height=400, bg=BLACK, highlightthickness=0)
#Load and resize the pomodoro image
pomodoro_image=Image.open(r"D:\Python's -- 100 Days of Code\Python's 100 days of code\Intermediate level\Day 28 - Tkinter, Dynamic Typing and the Pomodoro GUI Application\tomato.png")
pomodoro_image=pomodoro_image.resize((200, 200))
rotated_image=ImageTk.PhotoImage(pomodoro_image)
image_id=canvas.create_image(200, 200, image=rotated_image)
timer_text=canvas.create_text(200, 200, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

#Buttons
start_button=Button(text="Start", highlightbackground=BLACK, command=start_timer)
start_button.grid(column=0, row=2)

reset_button=Button(text="Reset", highlightbackground=BLACK, command=reset_timer)
reset_button.grid(column=2, row=2)

window.mainloop()