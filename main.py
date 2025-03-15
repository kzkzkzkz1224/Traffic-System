# main.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_generator import generate_traffic_data
from model_trainer import train_traffic_model
from traffic_controller import control_traffic_lights
import pandas as pd
from datetime import datetime

def update_plot(date, road, ax, canvas, data):
    """
    Updates the plot based on the selected date and road.
    """
    # Convert the calendar date to the format used in the data
    try:
        # Parse the date in "M/D/YY" format and convert it to "Month Day, Year DayOfWeek"
        formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%B %d, %Y %A")
    except ValueError:
        # If parsing fails, display an error message
        ax.clear()
        ax.text(0.5, 0.5, "Invalid date format", fontsize=14, ha='center', va='center')
        ax.set_title(f'Invalid Date for {road}', fontsize=14, fontweight='bold')
        canvas.draw()
        return

    # Filter data for the selected date and road
    date_data = data[(data['date'] == formatted_date) & (data['road'] == road)]

    # Clear the plot
    ax.clear()

    # Plot congestion levels
    if not date_data.empty:
        ax.plot(date_data['timestamp'], date_data['congestion'], label=f'{road} Congestion', color='royalblue', linewidth=2)
        ax.axhline(y=0.8, color='red', linestyle='--', label='High Congestion Threshold')
        ax.axhline(y=0.5, color='orange', linestyle='--', label='Normal Congestion Threshold')
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Congestion Level', fontsize=12)
        ax.set_title(f'Traffic Congestion on {formatted_date} for {road}', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)  # Rotate timestamps for better readability
        plt.tight_layout()  # Adjust layout to prevent overlap
    else:
        # If no data is found, display a message
        ax.text(0.5, 0.5, "No data available for this date", fontsize=14, ha='center', va='center')
        ax.set_title(f'No Data for {formatted_date} on {road}', fontsize=14, fontweight='bold')

    # Update the canvas
    canvas.draw()

def simulate_traffic_management(models, data):
    """
    Simulates real-time traffic management with roads as tabs and a calendar for date selection.
    """
    # Create the main window
    root = tk.Tk()
    root.title("AI-Powered Traffic Management System")
    root.geometry("1200x800")

    # Create a frame for the calendar
    control_frame = ttk.Frame(root)
    control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Create a calendar widget
    cal = Calendar(control_frame, selectmode="day", year=2025, month=3, day=1)
    cal.pack(side=tk.LEFT, padx=10)

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create a tab for each road
    for road in models.keys():
        # Create a frame for the tab
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=road)

        # Create a matplotlib figure and canvas
        fig, ax = plt.subplots(figsize=(10, 5))
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Function to update the plot for the current road
        def update_road_plot(road=road, ax=ax, canvas=canvas):
            selected_date = cal.get_date()
            update_plot(selected_date, road, ax, canvas, data)

        # Initialize the plot for the current road
        update_road_plot()

        # Bind the calendar to update the plot for the current road
        cal.bind("<<CalendarSelected>>", lambda event, r=road: update_road_plot(road=r))

    # Start the main loop
    root.mainloop()

# Main program
if __name__ == "__main__":
    # Generate traffic data for all 7 days starting from Saturday, March 1, 2025
    traffic_data = pd.DataFrame()
    for day in range(7):  # 0=Saturday, 6=Friday
        start_date = f"2025-03-{1 + day}"  # Start from Saturday, March 01, 2025
        day_data = generate_traffic_data(num_samples=48, start_date=start_date)
        traffic_data = pd.concat([traffic_data, day_data], ignore_index=True)

    print("Generated Traffic Data Sample:")
    print(traffic_data.head())

    # Train the model
    print("\nTraining the model...")
    models = train_traffic_model(traffic_data)
    print("Models trained successfully!")

    # Simulate traffic management
    print("\nSimulating Traffic Management...")
    simulate_traffic_management(models, traffic_data)
    print("Simulation completed successfully!")