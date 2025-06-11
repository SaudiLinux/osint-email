import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time
import re
from typing import List, Dict

class EmailOSINT:
    def __init__(self):
        self.console = Console()
        self.results = []
        self.setup_browser()

    def setup_browser(self):
        """إعداد متصفح Chrome للتصفح الآلي"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def search_email(self, email: str):
        """البحث عن البريد الإلكتروني في مواقع مختلفة"""
        self.console.print(f"[bold green]بدء البحث عن البريد الإلكتروني: {email}[/bold green]")
        
        # البحث في LinkedIn
        self.search_linkedin(email)
        
        # البحث في Twitter
        self.search_twitter(email)
        
        # البحث في GitHub
        self.search_github(email)

        # البحث في TikTok
        self.search_tiktok(email)

        # البحث في Snapchat
        self.search_snapchat(email)

        # البحث في Jaco.live
        self.search_jaco(email)
        
        # عرض النتائج
        self.display_results()

    def search_linkedin(self, email: str):
        """البحث عن البريد الإلكتروني في LinkedIn"""
        try:
            url = f"https://www.linkedin.com/pub/dir?email={email}"
            self.driver.get(url)
            time.sleep(2)
            
            if "لم يتم العثور على نتائج" not in self.driver.page_source:
                self.results.append({
                    "platform": "LinkedIn",
                    "status": "تم العثور على حساب محتمل",
                    "url": url
                })
        except Exception as e:
            self.console.print(f"[bold red]خطأ في البحث على LinkedIn: {str(e)}[/bold red]")

    def search_twitter(self, email: str):
        """البحث عن البريد الإلكتروني في Twitter"""
        try:
            url = f"https://twitter.com/search?q={email}&src=typed_query"
            self.driver.get(url)
            time.sleep(2)
            
            if email in self.driver.page_source:
                self.results.append({
                    "platform": "Twitter",
                    "status": "تم العثور على تطابقات محتملة",
                    "url": url
                })
        except Exception as e:
            self.console.print(f"[bold red]خطأ في البحث على Twitter: {str(e)}[/bold red]")

    def search_github(self, email: str):
        """البحث عن البريد الإلكتروني في GitHub"""
        try:
            url = f"https://api.github.com/search/users?q={email}"
            response = requests.get(url)
            data = response.json()
            
            if data.get('total_count', 0) > 0:
                self.results.append({
                    "platform": "GitHub",
                    "status": f"تم العثور على {data['total_count']} نتيجة محتملة",
                    "url": f"https://github.com/search?q={email}"
                })
        except Exception as e:
            self.console.print(f"[bold red]خطأ في البحث على GitHub: {str(e)}[/bold red]")

    def display_results(self):
        """عرض نتائج البحث في جدول منسق"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("المنصة")
        table.add_column("الحالة")
        table.add_column("الرابط")

        for result in self.results:
            table.add_row(
                result['platform'],
                result['status'],
                result['url']
            )

        self.console.print(table)

    def search_tiktok(self, email: str):
        """البحث عن البريد الإلكتروني في TikTok"""
        try:
            # استخدام محرك البحث TikTok
            url = f"https://www.tiktok.com/search?q={email}"
            self.driver.get(url)
            time.sleep(3)  # انتظار لتحميل المحتوى الديناميكي
            
            # البحث عن المحتوى في الصفحة
            if email in self.driver.page_source:
                self.results.append({
                    "platform": "TikTok",
                    "status": "تم العثور على تطابقات محتملة",
                    "url": url
                })
        except Exception as e:
            self.console.print(f"[bold red]خطأ في البحث على TikTok: {str(e)}[/bold red]")

    def search_snapchat(self, email: str):
        """البحث عن البريد الإلكتروني في Snapchat"""
        try:
            # استخدام محرك البحث Snapchat
            username = email.split('@')[0]  # استخراج اسم المستخدم من البريد الإلكتروني
            url = f"https://story.snapchat.com/@{username}"
            self.driver.get(url)
            time.sleep(3)  # انتظار لتحميل المحتوى
            
            # التحقق من وجود الحساب
            if "Page Not Found" not in self.driver.page_source:
                self.results.append({
                    "platform": "Snapchat",
                    "status": "تم العثور على حساب محتمل",
                    "url": url
                })
        except Exception as e:
            self.console.print(f"[bold red]خطأ في البحث على Snapchat: {str(e)}[/bold red]")

    def search_jaco(self, email: str):
        """البحث عن البريد الإلكتروني في Jaco.live"""
        try:
            # استخدام محرك البحث Jaco.live
            username = email.split('@')[0]  # استخراج اسم المستخدم من البريد الإلكتروني
            url = f"https://www.jaco.live/@{username}"
            self.driver.get(url)
            time.sleep(3)  # انتظار لتحميل المحتوى
            
            # التحقق من وجود الحساب
            if "User not found" not in self.driver.page_source:
                self.results.append({
                    "platform": "Jaco.live",
                    "status": "تم العثور على حساب محتمل",
                    "url": url
                })
        except Exception as e:
            self.console.print(f"[bold red]خطأ في البحث على Jaco.live: {str(e)}[/bold red]")

    def cleanup(self):
        """تنظيف وإغلاق المتصفح"""
        self.driver.quit()

def main():
    email = input("أدخل البريد الإلكتروني للبحث عنه: ")
    osint = EmailOSINT()
    
    try:
        osint.search_email(email)
    finally:
        osint.cleanup()

if __name__ == "__main__":
    main()