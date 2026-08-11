import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load trained model and preprocessing files
model = load_model("Traffic_Signal_Optimization_Model.keras")
scaler = joblib.load("scaler.pkl")
traffic_encoder = joblib.load("traffic_encoder.pkl")

# Create main window
root = tk.Tk()
root.title("Traffic Signal Timing Optimization")
root.geometry("500x650")

# Input fields
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
    tk.Label(
        root,
        text=label,
        font=("Arial", 12)
    ).pack(pady=3)

    entry = tk.Entry(root, width=20)
    entry.pack()

    entries.append(entry)

# Traffic light canvas
canvas = tk.Canvas(root, width=150, height=300)
canvas.pack(pady=20)

red = canvas.create_oval(
    40, 20, 110, 90,
    fill="gray"
)

yellow = canvas.create_oval(
    40, 110, 110, 180,
    fill="gray"
)

green = canvas.create_oval(
    40, 200, 110, 270,
    fill="gray"
)

# Result labels
traffic_result = tk.Label(
    root,
    font=("Arial", 14)
)
traffic_result.pack()

green_time_result = tk.Label(
    root,
    font=("Arial", 14)
)
green_time_result.pack()

# Prediction function
def predict():
    try:
        car = int(entries[0].get())
        bike = int(entries[1].get())
        bus = int(entries[2].get())
        truck = int(entries[3].get())
        hour = int(entries[4].get())
        day = int(entries[5].get())

        # Basic validation
        if hour < 0 or hour > 23:
            raise ValueError("Hour must be between 0 and 23.")

        if day < 1 or day > 7:
            raise ValueError("Day must be between 1 and 7.")

        if min(car, bike, bus, truck) < 0:
            raise ValueError("Vehicle counts cannot be negative.")

        # Calculate total vehicles
        total = car + bike + bus + truck

        # Create input sample
        sample = [[
            car,
            bike,
            bus,
            truck,
            total,
            hour,
            day
        ]]

        # Scale input
        sample = scaler.transform(sample)

        # Model prediction
        prediction = model.predict(
            sample,
            verbose=0
        )

        predicted_class = np.argmax(
            prediction,
            axis=1
        )[0]

        # Convert class number to traffic label
        predicted_traffic = traffic_encoder.inverse_transform(
            [predicted_class]
        )[0]

        # Reset traffic lights
        canvas.itemconfig(red, fill="gray")
        canvas.itemconfig(yellow, fill="gray")
        canvas.itemconfig(green, fill="gray")

        # Traffic timing logic
        if predicted_traffic.lower() == "low":
            green_time = 20
            canvas.itemconfig(
                green,
                fill="green"
            )

        elif predicted_traffic.lower() == "normal":
            green_time = 40
            canvas.itemconfig(
                green,
                fill="green"
            )

        elif predicted_traffic.lower() == "high":
            green_time = 60
            canvas.itemconfig(
                green,
                fill="green"
            )

        else:
            green_time = 90
            canvas.itemconfig(
                green,
                fill="green"
            )

        # Display results
        traffic_result.config(
            text=f"Traffic : {predicted_traffic}"
        )

        green_time_result.config(
            text=f"Recommended Green Time : {green_time} Seconds"
        )

    except ValueError as e:
        messagebox.showerror(
            "Input Error",
            str(e)
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{e}"
        )

# Predict button
tk.Button(
    root,
    text="Predict",
    command=predict,
    bg="green",
    fg="white",
    font=("Arial", 13)
).pack(pady=15)

# Start application
root.mainloop()