import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
import json
import os
import subprocess
import sys
import tempfile
from urllib.parse import urlparse

class CookieSessionTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Cookie & Session Tester")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.session = requests.Session()
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Large.TButton', font=('Arial', 11), padding=10)
    
    def create_widgets(self):
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Webhook Testing Tab
        webhook_frame = ttk.Frame(notebook, padding=10)
        notebook.add(webhook_frame, text="Webhook Testing")
        
        # Session Testing Tab
        session_frame = ttk.Frame(notebook, padding=10)
        notebook.add(session_frame, text="Session & Cookie Testing")
        
        self.create_webhook_tab(webhook_frame)
        self.create_session_tab(session_frame)
    
    def create_webhook_tab(self, parent):
        # Webhook title
        title_label = ttk.Label(parent, text="Discord Webhook Testing", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Webhook input
        webhook_frame = ttk.LabelFrame(parent, text="Webhook Configuration", padding=15)
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(webhook_frame, text="Discord Webhook URL:").pack(anchor=tk.W)
        
        self.webhook_entry = ttk.Entry(webhook_frame, width=80, font=('Arial', 10))
        self.webhook_entry.pack(fill=tk.X, pady=5)
        
        test_btn = ttk.Button(webhook_frame, text="Test Webhook", 
                            command=self.test_webhook, style='Large.TButton')
        test_btn.pack(pady=10)
        
        # Build section
        build_frame = ttk.LabelFrame(parent, text="Application Builder", padding=15)
        build_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(build_frame, text="Create standalone executable:").pack(anchor=tk.W)
        
        build_btn = ttk.Button(build_frame, text="Build EXE", 
                             command=self.build_exe, style='Large.TButton')
        build_btn.pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(parent, text="Ready", font=('Arial', 10))
        self.status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
    
    def create_session_tab(self, parent):
        # Session testing title
        title_label = ttk.Label(parent, text="Educational Session & Cookie Testing", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # URL input
        url_frame = ttk.LabelFrame(parent, text="Website Testing", padding=15)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_frame, text="Website URL (for educational testing):").pack(anchor=tk.W)
        
        self.site_entry = ttk.Entry(url_frame, width=80, font=('Arial', 10))
        self.site_entry.pack(fill=tk.X, pady=5)
        self.site_entry.insert(0, "https://httpbin.org/cookies")  # Educational API
        
        # Buttons
        btn_frame = ttk.Frame(url_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Test Connection", 
                  command=self.test_connection).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="View Cookies", 
                  command=self.view_cookies).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Clear Session", 
                  command=self.clear_session).pack(side=tk.LEFT)
        
        # Results area
        results_frame = ttk.LabelFrame(parent, text="Session Information", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, font=('Consolas', 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Educational info
        info_frame = ttk.LabelFrame(parent, text="Educational Purpose", padding=10)
        info_frame.pack(fill=tk.X)
        
        info_text = (
            "This tool demonstrates how HTTP sessions and cookies work for educational purposes.\n"
            "It shows how websites use cookies to maintain state between requests.\n"
            "Use this to learn about web development, APIs, and HTTP protocols."
        )
        ttk.Label(info_frame, text=info_text, wraplength=650, justify=tk.LEFT).pack(anchor=tk.W)
    
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
                    "title": "Educational Webhook Test",
                    "description": "This demonstrates webhook functionality for learning Python and HTTP requests",
                    "color": 5814783,
                    "fields": [
                        {"name": "Status", "value": "✅ Working!", "inline": True},
                        {"name": "Purpose", "value": "Python Education", "inline": True}
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
    
    def test_connection(self):
        url = self.site_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Testing connection to: {url}\n")
            self.results_text.insert(tk.END, "="*50 + "\n\n")
            
            response = self.session.get(url, timeout=10)
            
            # Display response info
            self.results_text.insert(tk.END, f"Status Code: {response.status_code}\n")
            self.results_text.insert(tk.END, f"Content Type: {response.headers.get('content-type', 'Unknown')}\n\n")
            
            # Display cookies
            cookies = self.session.cookies.get_dict()
            if cookies:
                self.results_text.insert(tk.END, "Cookies in session:\n")
                for name, value in cookies.items():
                    self.results_text.insert(tk.END, f"  {name}: {value}\n")
            else:
                self.results_text.insert(tk.END, "No cookies in session\n")
            
            self.results_text.insert(tk.END, "\n" + "="*50 + "\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def view_cookies(self):
        self.results_text.delete(1.0, tk.END)
        cookies = self.session.cookies.get_dict()
        
        if not cookies:
            self.results_text.insert(tk.END, "No cookies in current session\n")
            return
        
        self.results_text.insert(tk.END, "Current Session Cookies:\n")
        self.results_text.insert(tk.END, "="*50 + "\n\n")
        
        for name, value in cookies.items():
            self.results_text.insert(tk.END, f"Cookie: {name}\n")
            self.results_text.insert(tk.END, f"Value: {value}\n")
            self.results_text.insert(tk.END, f"Domain: {self.session.cookies.list_domains()}\n")
            self.results_text.insert(tk.END, "-" * 30 + "\n")
    
    def clear_session(self):
        self.session = requests.Session()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Session cleared - new session created\n")
        messagebox.showinfo("Success", "Session cleared successfully")
    
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
                title="Save EXE file as",
                initialfile="WebhookDemo.exe"
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
    """Get basic system information for educational purposes"""
    try:
        hostname = socket.gethostname()
        system = platform.system()
        return f"""
**Educational System Info:**
- Computer: {{hostname}}
- OS: {{system}}

*This demonstrates webhook functionality for learning Python.*
"""
    except:
        return "**System info unavailable**\\\\n*Educational webhook demonstration.*"

def send_webhook():
    """Send educational webhook message"""
    try:
        system_info = get_system_info()
        
        data = {{
            "embeds": [{{
                "title": "🎓 Python Learning Demo",
                "description": "This demonstrates webhook integration for educational purposes.\\\\n\\\\n" + system_info,
                "color": 3447003,
                "fields": [
                    {{
                        "name": "Purpose",
                        "value": "Learning Python & Webhooks",
                        "inline": True
                    }},
                    {{
                        "name": "Status", 
                        "value": "Demo Completed",
                        "inline": True
                    }}
                ]
            }}]
        }}
        
        response = requests.post("{webhook_url}", json=data, timeout=10)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", 
                              "✅ Educational demo completed!\\\\n\\\\n"
                              "This shows how webhooks work in Python.\\\\n"
                              "Check your Discord to see the message.")
        else:
            messagebox.showerror("Error", "Webhook demo failed - check URL")
                               
    except Exception as e:
        messagebox.showerror("Error", f"Demo failed: {{str(e)}}")

def main():
    root = tk.Tk()
    root.title("Webhook Educational Demo")
    root.geometry("500x300")
    root.configure(bg='#2C2F33')
    
    title_label = tk.Label(root, text="🎓 Webhook Learning Demo", 
                          font=('Arial', 16, 'bold'),
                          fg='#7289DA', bg='#2C2F33')
    title_label.pack(pady=30)
    
    description = tk.Label(root, 
                         text="This demonstrates webhook functionality\\\\n"
                              "for learning Python programming.",
                         font=('Arial', 11),
                         fg='white', bg='#2C2F33')
    description.pack(pady=20)
    
    demo_btn = tk.Button(root, text="🚀 Run Learning Demo",
                        command=send_webhook,
                        bg='#7289DA', fg='white',
                        font=('Arial', 12, 'bold'),
                        width=20, height=2)
    demo_btn.pack(pady=30)
    
    disclaimer = tk.Label(root, 
                        text="For educational purposes - Learning Python & web development",
                        font=('Arial', 9),
                        fg='#72767D', bg='#2C2F33')
    disclaimer.pack(side=tk.BOTTOM, pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = CookieSessionTester(root)
    root.mainloop()
