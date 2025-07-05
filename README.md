This is a BMI (Body Mass Index) Calculator built using Python's customtkinter GUI framework, which helps users calculate their BMI based on height, weight, age, and gender inputs. The app also stores BMI records in an Oracle database and visualizes the trend using matplotlib charts.

 Features:

-> Clean dark-themed UI using customtkinter

-> BMI calculation with automatic classification:

Severe Thinness to Obese Class III

-> Real-time colored slider indicator for BMI category

-> Data storage in Oracle Database (cx_Oracle)

-> View history of BMI records using a line chart (segregated by gender)

-> Option to Clear inputs and Visualize past entries

 Tech Stack:

-> Frontend: Python, customtkinter, Pillow (for images)

-> Backend/DB: cx_Oracle with Oracle XE

-> Data Visualization: matplotlib

 How to Use:

-> Enter your height (cm), weight (kg), age, and select gender.

-> Click Calculate to get your BMI value and category.

-> Click Visualize to see a graph of past BMI entries (stored in the Oracle DB).

-> Click Clear to reset input fields.

