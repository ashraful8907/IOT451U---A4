import customtkinter as ctk

# Global Font
global_font = ("Helvetica Neue", 18)

# Initialize Application
ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Project Management App X")
root.geometry("1000x700")
root.configure(bg="#1C1C1E")  # Dark gray background (default)

# Header Section
header_frame = ctk.CTkFrame(root, fg_color="#202124", height=100, corner_radius=15)
header_frame.pack(fill="x", pady=10)
header_label = ctk.CTkLabel(
    header_frame,
    text="Welcome to Project Management X",
    font=("Helvetica Neue", 28, "bold"),
    text_color="white",
)
header_label.pack(pady=20)

# Stats Section
stats_frame = ctk.CTkFrame(root, fg_color="#2E2E33", corner_radius=15)
stats_frame.pack(pady=20, padx=20, fill="x")
stats_label = ctk.CTkLabel(
    stats_frame,
    text="Total Projects: 0 | Total Tasks: 0 | Completed Tasks: 0",
    font=global_font,
    text_color="white",
)
stats_label.pack(pady=10)

# Function to Update Frame Colors Dynamically
def update_frame_colors():
    """Adjust frame colors for light and dark modes."""
    if ctk.get_appearance_mode() == "Light":
        # Light Mode Colors
        root.configure(bg="#F5F5F5")  # Light gray background
        header_frame.configure(fg_color="#E0E0E0")  # Light header box
        stats_frame.configure(fg_color="#FFFFFF")  # White for stats
        button_frame.configure(fg_color="#F0F0F0")  # Light gray button section
        footer_frame.configure(fg_color="#E0E0E0")  # Light footer box
        header_label.configure(text_color="black")  # Dark text in light mode
        stats_label.configure(text_color="black")
        footer_label.configure(text_color="black")
    else:
        # Dark Mode Colors
        root.configure(bg="#1C1C1E")  # Dark background
        header_frame.configure(fg_color="#202124")  # Dark header box
        stats_frame.configure(fg_color="#2E2E33")  # Darker gray for stats
        button_frame.configure(fg_color="#2E2E33")  # Dark gray button section
        footer_frame.configure(fg_color="#202124")  # Dark footer box
        header_label.configure(text_color="white")  # Light text in dark mode
        stats_label.configure(text_color="white")
        footer_label.configure(text_color="#A1A1A6")

# Toggle Light/Dark Mode
def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")
    update_frame_colors()  # Update frame colors dynamically

# Button Section
button_frame = ctk.CTkFrame(root, fg_color="#2E2E33", corner_radius=15)
button_frame.pack(pady=20, padx=20, expand=True)

actions = [
    ("Create Project", lambda: print("Create Project")),
    ("View Projects", lambda: print("View Projects")),
    ("Add Task to Project", lambda: print("Add Task")),
    ("Assign Task to Team Member", lambda: print("Assign Task")),
    ("View Tasks in Project", lambda: print("View Tasks")),
    ("View Team Member Workload", lambda: print("View Workload")),
    ("Filter by Category", lambda: print("Filter Tasks")),
    ("Check Overdue Tasks", lambda: print("Check Overdue")),
]

# Create Buttons
for i, (label, command) in enumerate(actions):
    column = 0 if i < 4 else 1
    row = i if i < 4 else i - 4
    ctk.CTkButton(
        button_frame,
        text=label,
        command=command,
        font=global_font,
        corner_radius=15,
        width=250,
        height=50,
        fg_color="#007AFF",
        hover_color="#005BB5",
    ).grid(row=row, column=column, padx=30, pady=20)

# Add Toggle Button for Light/Dark Mode
toggle_button = ctk.CTkButton(
    stats_frame,
    text="Toggle Light/Dark Mode",
    font=("Helvetica Neue", 14),
    command=toggle_mode,
    corner_radius=10,
    fg_color="#007AFF",
    hover_color="#005BB5",
)
toggle_button.pack(pady=10)

# Footer Section
footer_frame = ctk.CTkFrame(root, fg_color="#202124", height=50, corner_radius=15)
footer_frame.pack(fill="x", pady=10, side="bottom")
footer_label = ctk.CTkLabel(
    footer_frame,
    text="Project Management App X | Version 1.0 | © 2025",
    font=("Helvetica Neue", 12),
    text_color="#A1A1A6",
)
footer_label.pack(pady=10)

# Initial Frame Color Update
update_frame_colors()  # Adjust colors when the app starts

# Run the Application
root.mainloop()
