## Written by TomCrey (tom.crey@ibs.fr)
"""
Program to set up a graphical interface for the CryoCARE pipeline

Features :
- Import odd and even files
- List imported files
- Generate train_data_config.json
- Generate train_config.json
- Generate predict_config.json
- Run Prepare training data
- Run Training
- Run Prediction

- Generate output folder
- Output name
- Rename JSON files or delete at end of use
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Menu, Label, Button, ttk
import subprocess
import json
import os
import sys

class CryoCARE_pipeline:

    def __init__(self, master):
        # Initialize application with main window as parameter
        self.master = master
        self.master.title("CryoCARE - setup")
        self.create_widgets()
        self.create_menu()
        self.odd_files_training = []
        self.even_files_training = []
        self.odd_files_prediction = []
        self.even_files_prediction = []
        self.master.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Method to create user interface widgets
        self.create_title_label()
        self.create_tabs()

    def create_title_label(self):
        # Method to create the title label
        title_label = Label(self.master, text="CryoCARE - SETUP", font=('Helvetica', 14, 'bold'), background='dodgerblue1', foreground='white', pady=10, padx=10)
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_label.config(wraplength=500)
        tk.Label(self.master, text="").grid(row=1, column=0, columnspan=2, sticky="nsew")

    def create_tabs(self):
        # Method to create tabs for the various actions
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=2, column=0, columnspan=3, rowspan=7, sticky="nsew")

        ## 1st tab
        self.main_tab = tk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Prepare Training Data")
        self.main_tab.grid_rowconfigure(0, weight=5)
        self.main_tab.grid_columnconfigure(0, weight=1)

        # List of buttons and their associated functions for 1st tab
        buttons_train_data_config = [
            ("Import Odd Files for Training", self.import_odd_files_training),
            ("Import Even Files for Training", self.import_even_files_training),
            ("Generate train_data_config.json", self.generate_train_data_config),
            ("Prepare Training Data", self.prepare_training_data),
        ]

        for i, (button_text, command) in enumerate(buttons_train_data_config):
            Button(self.main_tab, text=button_text, command=command, font=('Helvetica', 10), padx=10, pady=5).grid(row=i+3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Labels to display selected odd and even files
        self.odd_label_training = Label(self.main_tab, text="Odd Files Selected: ")
        self.odd_label_training.grid(row=len(buttons_train_data_config) + 4, column=0, columnspan=2)
        self.even_label_training = Label(self.main_tab, text="Even Files Selected: ")
        self.even_label_training.grid(row=len(buttons_train_data_config) + 5, column=0, columnspan=2)


        ## 2nd tab
        self.training_tab = tk.Frame(self.notebook)
        self.notebook.add(self.training_tab, text="Run Training")
        self.training_tab.grid_rowconfigure(0, weight=5)
        self.training_tab.grid_columnconfigure(0, weight=1)

        # List of buttons and their associated functions for 2nd tab
        buttons_train_config = [
            ("Generate train_config.json", self.generate_train_config),
            ("Run Training", self.run_training),
        ]

        for i, (button_text, command) in enumerate(buttons_train_config):
            Button(self.training_tab, text=button_text, command=command, font=('Helvetica', 10), padx=10, pady=5).grid(row=i+3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")


        ## 3rd tab
        self.predict_tab = tk.Frame(self.notebook)
        self.notebook.add(self.predict_tab, text="Run Predictions")
        self.predict_tab.grid_rowconfigure(0, weight=5)
        self.predict_tab.grid_columnconfigure(0, weight=1)

        # List of buttons and their associated functions for 3rd tab
        buttons_predict = [
            ("Import Odd Files for Denoising", self.import_odd_files_prediction),
            ("Import Even Files for Denoising", self.import_even_files_prediction),
            ("Generate predict_config.json", self.generate_predict_config),
            ("Run Prediction", self.run_prediction)
        ]

        for i, (button_text, command) in enumerate(buttons_predict):
            Button(self.predict_tab, text=button_text, command=command, font=('Helvetica', 10), padx=10, pady=5).grid(row=i+3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Labels to display selected odd and even files in the third tab
        self.odd_label_predict = tk.Label(self.predict_tab, text="Odd Files Selected: ")
        self.odd_label_predict.grid(row=len(buttons_predict) + 3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.even_label_predict = tk.Label(self.predict_tab, text="Even Files Selected: ")
        self.even_label_predict.grid(row=len(buttons_predict) + 4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    def on_resize(self, event):
        # Method called when resizing the window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_menu(self):
        # Method to create the application menu
        menubar = Menu(self.master)
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="About", menu=about_menu)
        self.master.config(menu=menubar)

    def show_about(self):
        # Method to show "About" information in a dialog box
        about_text = '''This Graphical User Interface is designed to help you configure and launch the CryoCARE pipeline. It was created by Tom CREY, M1 trainee at IBS and LPCV (Grenoble, FRANCE).'''
        messagebox.showinfo("About", about_text)

    def import_odd_files_training(self):
        # Method to import odd files for training
        files = filedialog.askopenfilenames(title="Select odd files for training", filetypes=[("All files", "*.*")])
        if files:
            valid_files = [file for file in files if self.validate_file(file)]
            if valid_files:
                self.odd_files_training = valid_files
                self.odd_label_training.config(text=f"Odd Files Selected: {', '.join(valid_files)}")
            else:
                messagebox.showerror("Error", "No valid files selected.")

    def import_even_files_training(self):
        # Method to import even files for training
        files = filedialog.askopenfilenames(title="Select even files for training", filetypes=[("All files", "*.*")])
        if files:
            valid_files = [file for file in files if self.validate_file(file)]
            if valid_files:
                self.even_files_training = valid_files
                self.even_label_training.config(text=f"Even Files Selected: {', '.join(valid_files)}")
            else:
                messagebox.showerror("Error", "No valid files selected.")

    def import_odd_files_prediction(self):
        # Method to import odd files for prediction
        files = filedialog.askopenfilenames(title="Select odd files for prediction", filetypes=[("All files", "*.*")])
        if files:
            valid_files = [file for file in files if self.validate_file(file)]
            if valid_files:
                self.odd_files_prediction = valid_files
                self.odd_label_predict.config(text=f"Odd Files Selected: {', '.join(valid_files)}")
            else:
                messagebox.showerror("Error", "No valid files selected.")

    def import_even_files_prediction(self):
        # Method to import even files for prediction
        files = filedialog.askopenfilenames(title="Select even files for prediction", filetypes=[("All files", "*.*")])
        if files:
            valid_files = [file for file in files if self.validate_file(file)]
            if valid_files:
                self.even_files_prediction = valid_files
                self.even_label_predict.config(text=f"Even Files Selected: {', '.join(valid_files)}")
            else:
                messagebox.showerror("Error", "No valid files selected.")

    def validate_file(self, file_path):
        # Placeholder for a method that validates the file
        return os.path.isfile(file_path)

    def save_json_file(self, data, filename):
        # Method to save a JSON object to a file
        file_path = filedialog.asksaveasfilename(title=f"Save {filename}", defaultextension=".json", initialfile=filename)
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", f"{filename} has been generated and saved successfully.")

    def generate_train_data_config(self):
        # Method to generate the training data configuration file
        if not self.odd_files_training or not self.even_files_training:
            messagebox.showerror("Error", "You must select both odd and even files for training.")
            return
        
        # JSON content creation
        data = {
            "even": self.even_files_training,
            "odd": self.odd_files_training,
            "patch_shape": [72,72,72],
            "num_slices": 1200,
            "split": 0.9,
            "tilt_axis": "Y",
            "n_normalization_samples": 500,
            "path": "./output"
        }
        self.save_json_file(data, "train_data_config.json")

    def prepare_training_data(self):
        # Method to prepare the training data
        try:
            file_path = filedialog.askopenfilename(title="Select train_data_config.json", filetypes=[("JSON files", "*.json")])
            if file_path:
                subprocess.run(["cryoCARE_extract_train_data.py", "--conf", file_path])
                print("Prepare training data completed successfully.")
            messagebox.showinfo("Success", "Training data prepared successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to prepare training data. Error: {str(e)}")

    def generate_train_config(self):
        # Method to generate the training configuration file
        data = {
            "train_data": "./output",
            "epochs": 100,
            "steps_per_epoch": 200,
            "batch_size": 16,
            "unet_kern_size": 3,
            "unet_n_depth": 3,
            "unet_n_first": 16,
            "learning_rate": 0.0004,
            "model_name": "model_test",
            "path": "./output_model",
            "gpu_id": 0
        }
        self.save_json_file(data, "train_config.json")

    def run_training(self):
        # Method to run the training process
        try:

            file_path = filedialog.askopenfilename(title="Select train_config.json", filetypes=[("JSON files", "*.json")])
            if file_path:
                subprocess.run(["cryoCARE_train.py", "--conf", file_path])            
            messagebox.showinfo("Success", "Training completed successfully.")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run training. Error: {str(e)}")

    def generate_predict_config(self):
        # Method to generate the prediction configuration file
        if not self.odd_files_prediction or not self.even_files_prediction:
            messagebox.showerror("Error", "You must select both odd and even files for prediction.")
            return

        # JSON content creation
        data = {
            "path": "./output_model/model_test.tar.gz",
            "even": self.even_files,
            "odd": self.odd_files,
            "n_tiles": [4,4,4],
            "output": "denoised_files",
            "overwrite": False,
            "gpu_id": 0
        }
        self.save_json_file(data, "predict_config.json")

    def run_prediction(self):
        # Method to run the prediction process
        try:
            file_path = filedialog.askopenfilename(title="Select predict_config.json", filetypes=[("JSON files", "*.json")])
            if file_path:
                subprocess.run(["cryoCARE_predict.py", "--conf", file_path])
            messagebox.showinfo("Success", "Prediction completed successfully.")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run prediction. Error: {str(e)}")

def main():
    # Create application instance
    root = tk.Tk()
    app = CryoCARE_pipeline(root)

    # Start GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
