import tkinter as tk
from tkinter import ttk, messagebox, font
import pandas as pd
import matplotlib.pyplot as plt
from ttkbootstrap import Style

class EnhancedCPUScheduler:
    def __init__(self, root):
        # Use ttkbootstrap for modern design
        self.style = Style(theme='darkly')
        self.root = root
        self.root.title("Advanced CPU Scheduling Simulator")
        self.root.geometry("1200x800")
        
        # Enhanced color palette
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#e74c3c',
            'background': '#34495e',
            'text': '#ecf0f1'
        }
        
        # Comprehensive Scheduling Algorithms
        self.scheduling_algorithms = {
            "FCFS (Non-Preemptive)": self.fcfs_non_preemptive,
            "FCFS (Preemptive)": self.fcfs_preemptive,
            "SJF (Non-Preemptive)": self.sjf_non_preemptive,
            "SJF (Preemptive)": self.sjf_preemptive,
            "Priority (Non-Preemptive)": self.priority_non_preemptive,
            "Priority (Preemptive)": self.priority_preemptive,
            "Round Robin": self.round_robin
        }
        
        self.create_advanced_ui()
    
    def create_advanced_ui(self):
        # Main container with padding and background
        main_frame = ttk.Frame(self.root, padding=20, style='primary.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Stylish Title
        title_font = font.Font(family='Helvetica', size=20, weight='bold')
        title_label = ttk.Label(
            main_frame, 
            text="CPU Scheduling Simulator", 
            font=title_font, 
            foreground=self.colors['text']
        )
        title_label.pack(pady=20)
        
        # Algorithm Selection with Enhanced Dropdown
        algo_frame = ttk.Frame(main_frame)
        algo_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(algo_frame, text="Select Scheduling Algorithm:", 
                  foreground=self.colors['text']).pack(side=tk.LEFT, padx=10)
        
        self.algorithm_var = tk.StringVar()
        algorithm_dropdown = ttk.Combobox(
            algo_frame, 
            textvariable=self.algorithm_var, 
            values=list(self.scheduling_algorithms.keys()),
            state="readonly",
            width=40,
            style='primary.TCombobox'
        )
        algorithm_dropdown.pack(side=tk.LEFT, padx=10)
        algorithm_dropdown.set("Select an Algorithm")
        
        # Process Input Frame with Modern Design
        input_frame = ttk.LabelFrame(main_frame, text="Process Details", style='primary.TLabelframe')
        input_frame.pack(fill=tk.X, pady=10)
        
        # Input Headers
        headers = ["Process ID", "Arrival Time", "Burst Time", "Priority"]
        for i, header in enumerate(headers):
            ttk.Label(input_frame, text=header, foreground=self.colors['text']).grid(
                row=0, column=i, padx=10, pady=5
            )
        
        # Process Input Entries
        self.process_entries = []
        for i in range(6):  # 6 process rows
            row_entries = []
            for j in range(4):
                entry = ttk.Entry(input_frame, width=15, style='primary.TEntry')
                entry.grid(row=i+1, column=j, padx=10, pady=5)
                row_entries.append(entry)
            self.process_entries.append(row_entries)
        
        # Buttons with Modern Style
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        simulate_btn = ttk.Button(
            button_frame, 
            text="Simulate", 
            command=self.simulate, 
            style='success.TButton'
        )
        simulate_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_inputs, 
            style='danger.TButton'
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Results Display with Scrollbar
        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results", style='primary.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_text = tk.Text(
            results_frame, 
            height=10, 
            wrap=tk.WORD, 
            bg=self.colors['background'], 
            fg=self.colors['text']
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
    
    def simulate(self):
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Validate algorithm selection
        selected_algorithm = self.algorithm_var.get()
        if selected_algorithm == "Select an Algorithm":
            messagebox.showerror("Error", "Please select a scheduling algorithm")
            return
        
        # Get and validate process data
        processes = self.get_process_data()
        if not processes:
            return
        
        # Run selected algorithm
        algorithm_func = self.scheduling_algorithms[selected_algorithm]
        result = algorithm_func(processes)
        
        # Display results
        self.display_results(result, selected_algorithm)
    
    def get_process_data(self):
        processes = []
        for row in self.process_entries:
            # Skip empty rows
            if not row[0].get().strip():
                continue
            
            try:
                pid = row[0].get()
                arrival = float(row[1].get())
                burst = float(row[2].get())
                priority = float(row[3].get()) if row[3].get() else 0
                processes.append([pid, arrival, burst, priority])
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric values")
                return None
        
        return sorted(processes, key=lambda x: x[1])  # Sort by arrival time
    
    def display_results(self, result, algorithm):
        # Display results in text widget
        self.results_text.insert(tk.END, f"Algorithm: {algorithm}\n\n")
        
        # Create DataFrame for results
        df = pd.DataFrame(result['process_details'], 
                          columns=['Process', 'Arrival Time', 'Burst Time', 'Waiting Time', 'Turnaround Time'])
        
        # Display DataFrame
        self.results_text.insert(tk.END, df.to_string(index=False))
        
        # Calculate and display averages
        avg_waiting_time = df['Waiting Time'].mean()
        avg_turnaround_time = df['Turnaround Time'].mean()
        
        self.results_text.insert(tk.END, f"\n\nAverage Waiting Time: {avg_waiting_time:.2f}")
        self.results_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_turnaround_time:.2f}")
    
    def clear_inputs(self):
        # Clear all input entries
        for row in self.process_entries:
            for entry in row:
                entry.delete(0, tk.END)
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        # Reset algorithm selection
        self.algorithm_var.set("Select an Algorithm")
    
    # Implementing all scheduling algorithms (FCFS, SJF, Priority, Round Robin in both Preemptive and Non-Preemptive forms)
    def fcfs_non_preemptive(self, processes):
        current_time = 0
        process_details = []
        
        for process in processes:
            pid, arrival, burst, _ = process
            
            # Wait if process hasn't arrived
            if current_time < arrival:
                current_time = arrival
            
            # Calculate times
            waiting_time = current_time - arrival
            turnaround_time = waiting_time + burst
            
            process_details.append([pid, arrival, burst, waiting_time, turnaround_time])
            
            # Update current time
            current_time += burst
        
        return {'process_details': process_details}
    
    def fcfs_preemptive(self, processes):
        # FCFS is inherently non-preemptive, so we'll use the non-preemptive version
        return self.fcfs_non_preemptive(processes)
    
    def sjf_non_preemptive(self, processes):
        current_time = 0
        process_details = []
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available_processes = [p for p in remaining_processes if p[1] <= current_time]
            
            if not available_processes:
                # If no process has arrived, move time to next arrival
                current_time = remaining_processes[0][1]
                continue
            
            # Select process with shortest burst time
            selected_process = min(available_processes, key=lambda x: x[2])
            
            pid, arrival, burst, _ = selected_process
            
            # Wait if process hasn't arrived
            if current_time < arrival:
                current_time = arrival
            
            # Calculate times
            waiting_time = current_time - arrival
            turnaround_time = waiting_time + burst
            
            process_details.append([pid, arrival, burst, waiting_time, turnaround_time])
            
            # Update current time
            current_time += burst
            
            # Remove processed process
            remaining_processes.remove(selected_process)
        
        return {'process_details': process_details}
    
    def sjf_preemptive(self, processes):
        current_time = 0
        process_details = {}
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available_processes = [p for p in remaining_processes if p[1] <= current_time]
            
            if not available_processes:
                # If no process has arrived, move time to next arrival
                current_time = remaining_processes[0][1]
                continue
            
            # Select process with shortest remaining time
            selected_process = min(available_processes, key=lambda x: x[2])
            
            pid, arrival, burst, _ = selected_process
            
            # Initialize process details if not exists
            if pid not in process_details:
                process_details[pid] = [pid, arrival, burst, 0, 0]
            
            # Allocate 1 time unit
            current_time += 1
            selected_process[2] -= 1  # Reduce remaining burst time
            
            # Remove process if completed
            if selected_process[2] == 0:
                # Calculate waiting and turnaround times
                waiting_time = current_time - arrival - burst
                turnaround_time = current_time - arrival
                
                process_details[pid][3] = waiting_time
                process_details[pid][4] = turnaround_time
                
                remaining_processes.remove(selected_process)
        
        return {'process_details': list(process_details.values())}
    
    def priority_non_preemptive(self, processes):
        current_time = 0
        process_details = []
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available_processes = [p for p in remaining_processes if p[1] <= current_time]
            
            if not available_processes:
                # If no process has arrived, move time to next arrival
                current_time = remaining_processes[0][1]
                continue
            
            # Select process with highest priority (lower number means higher priority)
            selected_process = min(available_processes, key=lambda x: x[3])
            
            pid, arrival, burst, priority = selected_process
            
            # Wait if process hasn't arrived
            if current_time < arrival:
                current_time = arrival
            
            # Calculate times
            waiting_time = current_time - arrival
            turnaround_time = waiting_time + burst
            
            process_details.append([pid, arrival, burst, waiting_time, turnaround_time])
            
            # Update current time
            current_time += burst
            
            # Remove processed process
            remaining_processes.remove(selected_process)
        
        return {'process_details': process_details}
    
    def priority_preemptive(self, processes):
        current_time = 0
        process_details = {}
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available_processes = [p for p in remaining_processes if p[1] <= current_time]
            
            if not available_processes:
                # If no process has arrived, move time to next arrival
                current_time = remaining_processes[0][1]
                continue
            
            # Select process with highest priority (lower number means higher priority)
            selected_process = min(available_processes, key=lambda x: x[3])
            
            pid, arrival, burst, priority = selected_process
            
            # Initialize process details if not exists
            if pid not in process_details:
                process_details[pid] = [pid, arrival, burst, 0, 0]
            
            # Allocate 1 time unit
            current_time += 1
            selected_process[2] -= 1  # Reduce remaining burst time
            
            # Remove process if completed
            if selected_process[2] == 0:
                # Calculate waiting and turnaround times
                waiting_time = current_time - arrival - burst
                turnaround_time = current_time - arrival
                
                process_details[pid][3] = waiting_time
                process_details[pid][4] = turnaround_time
                
                remaining_processes.remove(selected_process)
        
        return {'process_details': list(process_details.values())}
    
    def round_robin(self, processes, quantum=2):
        current_time = 0
        process_details = {}
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available_processes = [p for p in remaining_processes if p[1] <= current_time]
            
            if not available_processes:
                # If no process has arrived, move time to next arrival
                current_time = remaining_processes[0][1]
                continue
            
            # Select first available process
            selected_process = available_processes[0]
            
            pid, arrival, burst, _ = selected_process
            
            # Initialize process details if not exists
            if pid not in process_details:
                process_details[pid] = [pid, arrival, burst, 0, 0]
            
            # Allocate quantum time or remaining burst time
            execution_time = min(quantum, selected_process[2])
            current_time += execution_time
            selected_process[2] -= execution_time
            
            # Remove process if completed
            if selected_process[2] == 0:
                # Calculate waiting and turnaround times
                waiting_time = current_time - arrival - burst
                turnaround_time = current_time - arrival
                
                process_details[pid][3] = waiting_time
                process_details[pid][4] = turnaround_time
                
                remaining_processes.remove(selected_process)
            else:
                # Move process to end of queue
                remaining_processes.remove(selected_process)
                remaining_processes.append(selected_process)
        
        return {'process_details': list(process_details.values())}

def main():
    root = tk.Tk()
    app = EnhancedCPUScheduler(root)
    root.mainloop()

if __name__ == "__main__":
    main()
