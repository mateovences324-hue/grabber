import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
import subprocess
import sys
import tempfile

class WebhookTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Webhook Tester - Educational Tool")
        self.root.geometry("600x400")  # Larger window
        self.root.resizable(True, True)
        
        # Configure grid weights for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Style configuration
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 12, 'bold'), padding=10)
        style.configure('Medium.TButton', font=('Arial', 10, 'bold'), padding=8)
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 10))
    
    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Discord Webhook Tester", 
                               style='Title.TLabel',
                               foreground='#7289DA')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Educational Tool for Learning Webhooks & Python GUI Development",
                                  style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(0, 30), sticky=tk.W)
        
        # Webhook input section
        webhook_frame = ttk.LabelFrame(main_frame, text="Webhook Configuration", padding="15")
        webhook_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        webhook_frame.columnconfigure(0, weight=1)
        
        webhook_label = ttk.Label(webhook_frame, text="Discord Webhook URL:")
        webhook_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.webhook_entry = tk.Entry(webhook_frame, width=70, font=('Arial', 11))
        self.webhook_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Test button - LARGER
        test_btn = ttk.Button(webhook_frame, text="🔍 Test Webhook", 
                            command=self.test_webhook,
                            style='Large.TButton')
        test_btn.grid(row=2, column=0, pady=10)
        
        # Build section
        build_frame = ttk.LabelFrame(main_frame, text="Application Builder", padding="15")
        build_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        build_frame.columnconfigure(0, weight=1)
        
        build_label = ttk.Label(build_frame, text="Create standalone executable:")
        build_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Build button - LARGER
        build_btn = ttk.Button(build_frame, text="🛠️ Build EXE", 
                             command=self.build_exe,
                             style='Large.TButton')
        build_btn.grid(row=1, column=0, pady=10)
        
        # Status section
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=20)
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Ready to test webhooks and build executables", 
                                     font=('Arial', 10),
                                     foreground='#43B581')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Educational disclaimer
        disclaimer_frame = ttk.Frame(main_frame)
        disclaimer_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        disclaimer_frame.columnconfigure(0, weight=1)
        
        disclaimer = ttk.Label(disclaimer_frame, 
                             text="For educational purposes only - Webhook Testing & Python Learning",
                             font=('Arial', 9),
                             foreground='#72767D',
                             justify=tk.CENTER)
        disclaimer.grid(row=0, column=0, pady=10)
    
    def test_webhook(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL")
            return
        
        if not webhook_url.startswith('https://discord.com/api/webhooks/'):
            messagebox.showerror("Error", "Please enter a valid Discord webhook URL")
            return
        
        self.status_label.config(text="Testing webhook...", foreground='#FAA61A')
        self.progress.start()
        self.root.update()
        
        try:
            # Create test message
            data = {
                "content": "Webhook Test Successful! 🎉",
                "embeds": [
                    {
                        "title": "Educational Webhook Test",
                        "description": "This is a test message from the Python Webhook Tester",
                        "color": 5814783,
                        "fields": [
                            {
                                "name": "Status",
                                "value": "✅ Working perfectly!",
                                "inline": True
                            },
                            {
                                "name": "Purpose",
                                "value": "Educational Python Project",
                                "inline": True
                            }
                        ],
                        "footer": {
                            "text": "Made for learning webhooks & GUI development"
                        }
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            
            if response.status_code == 204:
                self.status_label.config(text="✅ Webhook test successful! Ready to build EXE.", foreground='#43B581')
                messagebox.showinfo("Success", "Webhook test successful! Check your Discord channel.\n\nYou can now build the EXE file.")
            else:
                self.status_label.config(text="❌ Webhook test failed - Check URL", foreground='#F04747')
                messagebox.showerror("Error", f"Webhook test failed. Status code: {response.status_code}\n\nPlease check your webhook URL.")
                
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="❌ Connection error - Check internet", foreground='#F04747')
            messagebox.showerror("Error", f"Failed to connect: {str(e)}\n\nPlease check your internet connection and webhook URL.")
        except Exception as e:
            self.status_label.config(text="❌ Unexpected error occurred", foreground='#F04747')
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            self.progress.stop()
    
    def build_exe(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL first")
            return
        
        if not webhook_url.startswith('https://discord.com/api/webhooks/'):
            messagebox.showerror("Error", "Please enter a valid Discord webhook URL")
            return
        
        self.status_label.config(text="Building executable... This may take a minute.", foreground='#FAA61A')
        self.progress.start()
        self.root.update()
        
        try:
            # Create the client script
            client_script = self.create_client_script(webhook_url)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(client_script)
                temp_script_path = f.name
            
            # Ask for save location
            output_path = filedialog.asksaveasfilename(
                defaultextension=".exe",
                filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
                title="Save EXE file as",
                initialfile="WebhookDemo.exe"
            )
            
            if not output_path:
                os.unlink(temp_script_path)
                self.status_label.config(text="Build cancelled", foreground='#72767D')
                self.progress.stop()
                return
            
            # Update status
            self.status_label.config(text="Compiling with PyInstaller... This may take a while.", foreground='#FAA61A')
            self.root.update()
            
            # Get the directory and filename for output
            output_dir = os.path.dirname(output_path)
            output_name = os.path.basename(output_path).replace('.exe', '')
            
            # Build with PyInstaller
            result = subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--windowed',
                '--name', output_name,
                '--distpath', output_dir,
                '--workpath', os.path.join(tempfile.gettempdir(), 'pyinstaller'),
                temp_script_path
            ], capture_output=True, text=True, timeout=120)
            
            # Clean up
            os.unlink(temp_script_path)
            
            if result.returncode == 0:
                self.status_label.config(text="✅ EXE built successfully! Check your selected folder.", foreground='#43B581')
                messagebox.showinfo("Success", 
                                  f"Executable built successfully!\\n\\n"
                                  f"File saved to: {output_path}\\n\\n"
                                  f"You can now distribute the EXE file.")
            else:
                self.status_label.config(text="❌ Build failed - Check PyInstaller", foreground='#F04747')
                messagebox.showerror("Error", 
                                   f"Failed to build executable.\\n\\n"
                                   f"Error: {result.stderr}\\n\\n"
                                   f"Make sure PyInstaller is installed: pip install pyinstaller")
                
        except subprocess.TimeoutExpired:
            self.status_label.config(text="❌ Build timeout - Try again", foreground='#F04747')
            messagebox.showerror("Error", "Build process timed out. Please try again.")
        except Exception as e:
            self.status_label.config(text="❌ Build error occurred", foreground='#F04747')
            messagebox.showerror("Error", f"Build failed: {str(e)}")
        finally:
            self.progress.stop()

    def create_client_script(self, webhook_url):
        return f'''import requests
import tkinter as tk
from tkinter import messagebox
import platform
import socket

def get_system_info():
    """Get basic system information for educational purposes"""
    try:
        hostname = socket.gethostname()
        system = platform.system()
        version = platform.version()
        
        return f"""
**System Information (Educational):**
- Computer Name: {{hostname}}
- Operating System: {{system}}
- Version: {{version}}

*This application demonstrates webhook functionality for educational purposes.*
"""
    except:
        return "**System information unavailable**\\\\n*This application demonstrates webhook functionality for educational purposes.*"

def send_webhook_message():
    """Send a message to the Discord webhook"""
    try:
        system_info = get_system_info()
        
        data = {{
            "embeds": [
                {{
                    "title": "🎓 Educational Webhook Demo",
                    "description": "This is a demonstration of webhook functionality for learning purposes.\\\\n\\\\n" + system_info,
                    "color": 3447003,
                    "fields": [
                        {{
                            "name": "Purpose",
                            "value": "Python Education & Webhook Learning",
                            "inline": True
                        }},
                        {{
                            "name": "Status",
                            "value": "Demo Completed Successfully",
                            "inline": True
                        }}
                    ],
                    "footer": {{
                        "text": "Educational Project - Webhook Demonstrator"
                    }}
                }}
            ]
        }}
        
        response = requests.post("{webhook_url}", json=data, timeout=10)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", 
                              "✅ Educational demo completed!\\\\n\\\\n"
                              "This demonstrates how webhooks work for learning purposes.\\\\n"
                              "Check your Discord channel to see the message.")
        else:
            messagebox.showerror("Error", 
                               "Webhook demo failed.\\\\n"
                               "This might be because the webhook URL is invalid or expired.")
                               
    except Exception as e:
        messagebox.showerror("Error", 
                           f"Failed to send demo message: {{str(e)}}\\\\n\\\\n"
                           "This demonstrates error handling in Python applications.")

def main():
    # Create GUI
    root = tk.Tk()
    root.title("Webhook Educational Demo")
    root.geometry("500x300")  # Larger window
    root.resizable(False, False)
    
    # Configure style
    root.configure(bg='#2C2F33')
    
    # Create widgets
    title_label = tk.Label(root, text="🎓 Webhook Educational Demo", 
                          font=('Arial', 16, 'bold'),
                          fg='#7289DA', bg='#2C2F33')
    title_label.pack(pady=30)
    
    description = tk.Label(root, 
                         text="This application demonstrates how webhooks work\\\\n"
                              "for educational purposes in Python programming.\\\\n\\\\n"
                              "Click the button below to run the demo:",
                         font=('Arial', 11),
                         fg='white', bg='#2C2F33')
    description.pack(pady=20)
    
    demo_btn = tk.Button(root, text="🚀 Run Educational Demo",
                        command=send_webhook_message,
                        bg='#7289DA', fg='white',
                        font=('Arial', 12, 'bold'),
                        width=25, height=2)
    demo_btn.pack(pady=30)
    
    disclaimer = tk.Label(root, 
                        text="For educational purposes only - Learning webhooks & Python",
                        font=('Arial', 9),
                        fg='#72767D', bg='#2C2F33')
    disclaimer.pack(side=tk.BOTTOM, pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTesterApp(root)
    root.mainloop()
