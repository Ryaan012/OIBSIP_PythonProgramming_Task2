from tkinter import *
import customtkinter
import cx_Oracle
from PIL import Image , ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

customtkinter.set_appearance_mode("dark")

window = customtkinter.CTk()
window.title("BMI CALCULATOR (ADVANCED)")
window.geometry("500x700")

def clear() :
    Height_entry.delete(0,END)
    Weight_entry.delete(0,END)
    Age_entry.delete(0,END)
    results.configure(text="")

def save_to_db(gender, height, weight, age, bmi, bmi_class):
    try:
        conn = cx_Oracle.connect("SYSTEM/dbms123@localhost/XE")
        cursor = conn.cursor()
        cursor.execute("""""    
            INSERT INTO bmi_records (gender, height_cm, weight_kg, age, bmi_value, bmi_class)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (gender, height, weight, age, bmi, bmi_class))
        conn.commit()
        cursor.close()
        conn.close()
    except cx_Oracle.DatabaseError as e:
        print("Database Error:", e)

def bmi_cal():
    try:
        height = int(Height_entry.get())
        weight = int(Weight_entry.get())
        age = int(Age_entry.get())
        gender = Gender_var.get()

        cal_height = height * height
        cal_weight = weight
        bmi = (cal_weight / cal_height) * 10000
        rounded = round(bmi, 1)
        category = ""

        results.configure(text=f"{str(rounded)}")
        bmi_slider.set(rounded)

        if (rounded < 16):
            category = "Severe Thinness"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#800000")
            bmi_slider.configure(progress_color="#800000")
        elif (16 <= rounded < 17):
            category = "Moderate Thinness"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#ff6600")
            bmi_slider.configure(progress_color="#ff6600")
        elif (17 <= rounded <= 18.4):
            category = "Mild Thinness"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#fdab32")
            bmi_slider.configure(progress_color="#fdab32")
        elif (18.5 <= rounded <= 24.9):
            category = "Normal"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#47c0f4")
            bmi_slider.configure(progress_color="#47c0f4")
        elif (25 <= rounded <= 29.9):
            category = "Overweight"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="green")
            bmi_slider.configure(progress_color="green")
        elif (30 <= rounded <= 34.9):
            category = "Obese Class I"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#fdab32")
            bmi_slider.configure(progress_color="#fdab32")
        elif (35 <= rounded <= 39.9):
            category = "Obese Class II"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#ff6600")
            bmi_slider.configure(progress_color="#ff6600")
        else:
            category = "Obese Class III"
            results.configure(text=f"{str(rounded)}\n{category}", text_color="#800000")
            bmi_slider.configure(progress_color="#800000")

        save_to_db(gender, height, weight, age, rounded, category)

    except Exception as e:
        results.configure(text="Error!", text_color="red")
        print("Error:", e)

def show_bmi_graph():
    try:
        conn = cx_Oracle.connect("SYSTEM/dbms123@localhost/XE")
        cursor = conn.cursor()
        cursor.execute("SELECT TO_CHAR(ROWNUM), bmi_value, gender FROM bmi_records ORDER BY ROWNUM")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not data:
            results.configure(text="No Data Found", text_color="yellow")
            return

        x_male = []
        y_male = []
        x_female = []
        y_female = []

        count_male = 1
        count_female = 1

        for i in data:
            if i[2] == "Male":
                x_male.append(str(count_male))
                y_male.append(float(i[1]))
                count_male += 1
            elif i[2] == "Female":
                x_female.append(str(count_female))
                y_female.append(float(i[1]))
                count_female += 1

        fig, ax = plt.subplots(figsize=(5, 6), dpi=100)
        if x_male:
            ax.plot(x_male, y_male, marker='o', label='Male', color='blue')
        if x_female:
            ax.plot(x_female, y_female, marker='o', label='Female', color='magenta')

        ax.set_title("BMI Trend by Gender")
        ax.set_xlabel("Entry Number")
        ax.set_ylabel("BMI Value")
        ax.grid(True)
        ax.legend()

        chart_window = Toplevel(window)
        chart_window.title("BMI History Chart")
        chart_window.geometry("520x350")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except cx_Oracle.DatabaseError as e:
        print("Database Error:", e)
        results.configure(text="DB Error!", text_color="red")

height_frame = customtkinter.CTkFrame(master=window, fg_color="transparent")
height_frame.pack(pady=10)

height_label = customtkinter.CTkLabel(master=height_frame, text="Height:", width=50, anchor="w")
height_label.pack(side="left", padx=10)

Height_entry = customtkinter.CTkEntry(master=height_frame,
placeholder_text="Height in cm",
height=40,
width=200,
corner_radius=10,
border_width=1,
border_color="white")
Height_entry.pack(side = "left")

Weight_frame = customtkinter.CTkFrame(master=window, fg_color="transparent")
Weight_frame.pack(pady=10)

Weight_label = customtkinter.CTkLabel(master=Weight_frame, text="Weight:", width=50, anchor="w")
Weight_label.pack(side="left", padx=10)

Weight_entry = customtkinter.CTkEntry(master=Weight_frame,
placeholder_text="Weight in KG",
height=40,
width=200,
corner_radius=10,
border_width=1,
border_color="white")
Weight_entry.pack(side = "left")

Age_frame = customtkinter.CTkFrame(master=window, fg_color="transparent")
Age_frame.pack(pady=10)

Age_label = customtkinter.CTkLabel(master=Age_frame, text="Age:", width=50, anchor="w")
Age_label.pack(side="left", padx=10)

Age_entry = customtkinter.CTkEntry(master=Age_frame,
placeholder_text="Age",
height=40,
width=200,
corner_radius=10,
border_width=1,
border_color="white")
Age_entry.pack(side = "left")

Gender_frame = customtkinter.CTkFrame(master=window, fg_color="transparent")
Gender_frame.pack(pady=10)

Gender_label = customtkinter.CTkLabel(master=Gender_frame, text="Gender:", width=50, anchor="w")
Gender_label.pack(side="left", padx=10)

Gender_var = StringVar(value="Male")

M_radio = customtkinter.CTkRadioButton(master=Gender_frame, text="Male", variable=Gender_var, value="Male")
M_radio.pack(side="left", padx=10)

F_radio = customtkinter.CTkRadioButton(master=Gender_frame, text="Female", variable=Gender_var, value="Female")
F_radio.pack(side="left", padx=10)

button_frame = customtkinter.CTkFrame(master=window, fg_color="transparent")
button_frame.pack(pady=20)

b_1 = customtkinter.CTkButton(master=button_frame,
text="Calculate",
width=150,
height=30,
border_width=1,
border_color="white",
hover_color="#7898C7",
command=bmi_cal)
b_1.pack(side="left", padx=10)

b_2 = customtkinter.CTkButton(master=button_frame,
text="Clear",
width=150,
height=30,
border_width=1,
border_color="white",
fg_color="#800000",
hover_color="#C77C78",
command=clear)
b_2.pack(side="left", padx=20)

b_3 = customtkinter.CTkButton(master=button_frame,
text="Visualize",
width=150,
height=30,
border_width=1,
border_color="white",
fg_color="#1E90FF",
hover_color="#6495ED",
command=show_bmi_graph)
b_3.pack(side="left", padx=10)

results = customtkinter.CTkLabel(master = window,
text = "",
font=("Helvetica",28))
results.pack(pady=20)

bmi_slider = customtkinter.CTkSlider(master=window, from_=10, to=50, width=400, number_of_steps=400, progress_color="gray")
bmi_slider.set(0)
bmi_slider.pack(pady=10)

O_img = Image.open("C:/Users/ryaan/OneDrive/Pictures/bmipic.png")
img = ImageTk.PhotoImage(O_img)
img_img = Label(window, image=img, bd=0)
img_img.pack(pady=20)

window.mainloop()
