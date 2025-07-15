#!/usr/bin/env python3
"""
简易浏览器框架（Tkinter图形界面版）

本程序使用Python的requests和BeautifulSoup库构建一个简易浏览器，并通过Tkinter提供图形化用户界面。
主要功能包括：
- 通过URL获取网页内容，并在界面上显示
- 支持自定义User-Agent和Cookie设置
- 从网站下载文件

依赖：
- requests
- bs4 (BeautifulSoup)
- tkinter（内置库）
"""

import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

class SimpleBrowser:
    def __init__(self):
        # 创建一个session来保持cookies和headers
        self.session = requests.Session()
        # 默认User-Agent
        self.session.headers.update({
            'User-Agent': 'SimpleBrowser/1.0 (using requests and bs4)'
        })

    def set_user_agent(self, user_agent: str):
        """设置自定义的User-Agent"""
        self.session.headers.update({'User-Agent': user_agent})

    def set_cookies(self, cookies: dict):
        """设置cookies"""
        self.session.cookies.update(cookies)

    def get(self, url: str, params: dict = None):
        """执行GET请求，返回解析后的BeautifulSoup对象"""
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return self.parse_html(response.text)

    def download_file(self, url: str, file_path: str):
        """从指定URL下载文件并保存到给定路径"""
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    @staticmethod
    def parse_html(html: str):
        """使用BeautifulSoup解析HTML"""
        return BeautifulSoup(html, 'html.parser')

class BrowserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('简易浏览器')
        self.browser = SimpleBrowser()
        self.create_widgets()
    
    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # URL输入框
        ttk.Label(frm, text='URL:').grid(row=0, column=0, sticky='w')
        self.url_entry = ttk.Entry(frm, width=60)
        self.url_entry.grid(row=0, column=1, columnspan=3, sticky='ew', pady=5)
        
        # User-Agent输入框
        ttk.Label(frm, text='User-Agent:').grid(row=1, column=0, sticky='w')
        self.ua_entry = ttk.Entry(frm, width=60)
        self.ua_entry.insert(0, self.browser.session.headers.get('User-Agent'))
        self.ua_entry.grid(row=1, column=1, columnspan=3, sticky='ew', pady=5)
        
        # Cookies输入框
        ttk.Label(frm, text='Cookies (格式: key1=value1; key2=value2):').grid(row=2, column=0, columnspan=4, sticky='w')
        self.cookies_entry = ttk.Entry(frm, width=60)
        self.cookies_entry.grid(row=3, column=0, columnspan=4, sticky='ew', pady=5)
        
        # 按钮区域
        self.get_button = ttk.Button(frm, text='GET网页', command=self.get_page)
        self.get_button.grid(row=4, column=0, pady=5)
        
        self.download_button = ttk.Button(frm, text='下载文件', command=self.download_file)
        self.download_button.grid(row=4, column=1, pady=5)
        
        # 显示网页内容的文本区域
        self.text_area = scrolledtext.ScrolledText(frm, wrap=tk.WORD, width=80, height=20)
        self.text_area.grid(row=5, column=0, columnspan=4, pady=10, sticky='nsew')
        frm.rowconfigure(5, weight=1)
        frm.columnconfigure(3, weight=1)
    
    def update_settings(self):
        """更新User-Agent和Cookies设置"""
        ua = self.ua_entry.get().strip()
        if ua:
            self.browser.set_user_agent(ua)
        
        cookies_text = self.cookies_entry.get().strip()
        if cookies_text:
            cookies = {}
            parts = cookies_text.split(';')
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    cookies[key.strip()] = value.strip()
            self.browser.set_cookies(cookies)
    
    def get_page(self):
        """获取网页内容并在文本区域显示解析后的HTML"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning('警告', '请输入URL')
            return
        
        self.update_settings()
        try:
            soup = self.browser.get(url)
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, soup.prettify())
        except Exception as e:
            messagebox.showerror('错误', str(e))
    
    def download_file(self):
        """下载指定URL的文件"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning('警告', '请输入文件下载的URL')
            return
        
        file_path = filedialog.asksaveasfilename(title='保存文件', defaultextension='*.*')
        if not file_path:
            return
        
        self.update_settings()
        try:
            self.browser.download_file(url, file_path)
            messagebox.showinfo('提示', f'文件已成功下载至: {file_path}')
        except Exception as e:
            messagebox.showerror('错误', str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = BrowserGUI(root)
    root.mainloop()
