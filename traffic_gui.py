import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ===========================
# Load AI Model
# ===========================

model = load_model("Traffic_Signal_Optimization_Model.keras")
scaler = joblib.load("scaler.pkl")
traffic_encoder = joblib.load("traffic_encoder.pkl")

# ===========================
# Create Window
# ===========================

root = tk.Tk()
root.title("Traffic Signal Timing Optimization")
root.geometry("500x650")

# ===========================
# Input Fields
# ===========================

labels = [
    "Car Count",
    "Bike Count",
    "Bus Count",
    "Truck Count",
    "Hour (0-23)",
    "Day (1-7)"
]

entries = []

for label in labels:
    tk.Label(root, text=label, font=("Arial",12)).pack(pady=3)

    entry = tk.Entry(root, width=20)
    entry.pack()

    entries.append(entry)

# ===========================
# Traffic Light
# ===========================

canvas = tk.Canvas(root, width=150, height=300)
canvas.pack(pady=20)

red = canvas.create_oval(40,20,110,90,fill="gray")
yellow = canvas.create_oval(40,110,110,180,fill="gray")
green = canvas.create_oval(40,200,110,270,fill="gray")

traffic_result = tk.Label(root,font=("Arial",14))
traffic_result.pack()

green_time_result = tk.Label(root,font=("Arial",14))
green_time_result.pack()

# ===========================
# Prediction Function
# ===========================

def predict():

    try:

        car = int(entries[0].get())
        bike = int(entries[1].get())
        bus = int(entries[2].get())
        truck = int(entries[3].get())
        hour = int(entries[4].get())
        day = int(entries[5].get())

        total = car + bike + bus + truck

        sample = [[car,bike,bus,truck,total,hour,day]]

        sample = scaler.transform(sample)

        prediction = model.predict(sample,verbose=0)

        predicted_class = np.argmax(prediction)

        predicted_traffic = traffic_encoder.inverse_transform([predicted_class])[0]

        canvas.itemconfig(red,fill="gray")
        canvas.itemconfig(yellow,fill="gray")
        canvas.itemconfig(green,fill="gray")

        if predicted_traffic.lower()=="low":

            green_time=20
            canvas.itemconfig(green,fill="green")

        elif predicted_traffic.lower()=="normal":

            green_time=40
            canvas.itemconfig(green,fill="green")

        elif predicted_traffic.lower()=="high":

            green_time=60
            canvas.itemconfig(yellow,fill="yellow")

        else:

            green_time=90
            canvas.itemconfig(red,fill="red")

        traffic_result.config(text="Traffic : "+predicted_traffic)

        green_time_result.config(
            text="Recommended Green Time : {} Seconds".format(green_time)
        )

    except Exception as e:

        messagebox.showerror("Error",str(e))

# ===========================
# Button
# ===========================

tk# Predict Button
tk.Button(
    root,
    text="Predict",
    command=predict,
    bg="green",
    fg="white",
    font=("Arial", 13)
).pack(pady=15)

# Start GUI
root.mainloop()

def predict():
    try:
        ...
    except Exception as e:
        messagebox.showerror("Error", str(e))

# <-- No spaces before tk.Button
tk.Button(...)

root.mainloop()

canvas.itemconfig(green, fill="green")

for sec in range(green_time,0,-1):
    green_time_label.config(text=f"Green : {sec}")
    root.update()
    root.after(1000)

canvas.itemconfig(green, fill="gray")
canvas.itemconfig(yellow, fill="yellow")

for sec in range(3,0,-1):
    green_time_label.config(text=f"Yellow : {sec}")
    root.update()
    root.after(1000)

canvas.itemconfig(yellow, fill="gray")
canvas.itemconfig(red, fill="red")

for sec in range(5,0,-1):
    green_time_label.config(text=f"Red : {sec}")
    root.update()
    root.after(1000)