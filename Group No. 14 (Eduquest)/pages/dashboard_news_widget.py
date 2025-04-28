# First the imports
import customtkinter as ctk
from datetime import datetime, timedelta
import webbrowser
import threading
import requests
import time
import os
import random

# Then debug statements that use imported modules
print("Loading dashboard_news_widget.py - Version: " + str(datetime.now()))

class DashboardNewsWidget(ctk.CTkFrame):
    def __init__(self, master, app):
        print("LOADING DASHBOARD NEWS WIDGET")
        super().__init__(master, fg_color="#2C2C2C", corner_radius=10)
        self.master = master
        self.app = app
        # News API key - you can get a free one at newsapi.org
        self.api_key = "43ac41ed04cc4c37bb645b1eec69a443"
        self.news_items = []
        
        # Create the UI identical to screenshot
        self.create_ui()
        
        # Load news in a separate thread
        threading.Thread(target=self.fetch_news, daemon=True).start()
        
        # Add debug info label
        self.debug_info = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=9),
            text_color="#555555",
            anchor="w"
        )
        self.debug_info.pack(fill="x", padx=10, pady=(0, 5))
        
    def create_ui(self):
        """Create news widget UI identical to the screenshot"""
        # Title - "Latest Exam News"
        title_label = ctk.CTkLabel(
            self,
            text="Latest Exam News",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # News container
        self.news_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color="#3E3E3E",
            scrollbar_button_hover_color="#505050",
            height=400  # Fixed height to match screenshot
        )
        self.news_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self.news_container,
            text="Loading latest news...",
            font=ctk.CTkFont(size=14),
            text_color="#aaaaaa"
        )
        self.loading_label.pack(pady=30)
        
        # Refresh News button at the bottom
        self.refresh_btn = ctk.CTkButton(
            self,
            text="Refresh News",
            command=lambda: threading.Thread(target=self.fetch_news, daemon=True).start(),
            height=36,
            font=ctk.CTkFont(size=14),
            fg_color="#2AB377",
            hover_color="#1C7F50",
            corner_radius=4
        )
        self.refresh_btn.pack(fill="x", padx=15, pady=(0, 15))
        
    def fetch_news(self):
        """Fetch news from API"""
        try:
            # Show loading status
            self.after(0, lambda: self.update_loading_status("Loading latest news..."))
            self.debug_info.configure(text="Starting news fetch...")
            
            # Try to fetch from API
            self.debug_info.configure(text="Fetching from API...")
            if not self.fetch_from_api():
                # If API fails, use backup news
                self.debug_info.configure(text="API fetch failed, using backup")
                self.use_education_backup()
            else:
                self.debug_info.configure(text=f"Loaded {len(self.news_items)} news items from API")
            
            # Update display
            self.after(0, self.update_news_display)
            
        except Exception as e:
            error_msg = f"Error fetching news: {e}"
            print(error_msg)
            self.debug_info.configure(text=error_msg)
            # Use backup on any error
            self.use_education_backup()
            self.after(0, self.update_news_display)

    def fetch_from_api(self):
        """Fetch news from API"""
        try:
            # First attempt: NewsAPI
            url = "https://newsapi.org/v2/everything"
            
            # Try with education-focused query
            params = {
                "apiKey": self.api_key,
                "q": "education OR entrance exam OR JEE OR NEET OR GATE",
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": 10,
                "from": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            }
            
            # Make direct request
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Parse the response
                articles = response.json().get("articles", [])
                
                if not articles:
                    # Try alternate API: Gnews
                    return self.fetch_from_gnews_api()
                
                # Filter articles to ensure they're education-related
                filtered_articles = []
                
                for article in articles:
                    # Basic filtering
                    title = article.get("title", "").lower()
                    
                    # Skip entertainment articles
                    if any(term in title for term in ["movie", "film", "anime", "series", "actor"]):
                        continue
                    
                    # Categorize the article
                    if "jee" in title:
                        category = "JEE"
                    elif "neet" in title:
                        category = "NEET"
                    elif "gate" in title:
                        category = "GATE"
                    else:
                        category = "Education"
                    
                    # Add category to article
                    article["category"] = category
                    filtered_articles.append(article)
                
                if filtered_articles:
                    # Use for display
                    self.news_items = filtered_articles[:4]
                    return True
            
            # If we got here, NewsAPI failed
            return self.fetch_from_gnews_api()
            
        except Exception as e:
            print(f"API request failed: {e}")
            return self.fetch_from_gnews_api()
    
    def fetch_from_gnews_api(self):
        """Alternate API: Gnews"""
        try:
            # Try with Gnews API as backup
            gnews_url = "https://gnews.io/api/v4/search"
            gnews_params = {
                "q": "education exam",
                "lang": "en",
                "max": 10,
                "apikey": "5c2a6ae5c1cd81df5fd960c6089c32cd" # Demo key - replace with your own
            }
            
            response = requests.get(gnews_url, params=gnews_params, timeout=10)
            
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                
                if articles:
                    # Transform to match NewsAPI format
                    transformed_articles = []
                    for article in articles:
                        transformed = {
                            "title": article.get("title", ""),
                            "description": article.get("description", ""),
                            "url": article.get("url", ""),
                            "publishedAt": article.get("publishedAt", ""),
                            "source": {"name": article.get("source", {}).get("name", "")},
                            "category": "Education"
                        }
                        transformed_articles.append(transformed)
                    
                    self.news_items = transformed_articles[:4]
                    return True
            
            # Both APIs failed
            return False
            
        except Exception as e:
            print(f"Gnews API request failed: {e}")
            return False
    
    def use_education_backup(self):
        """Use backup education news when APIs fail"""
        # Get current date for news timestamps
        current_date = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        
        # Create backup news
        backup_news = [
            {
                "title": "JEE Main 2023 Session 2 Application Process Begins Today",
                "description": "The National Testing Agency (NTA) has started the application process for JEE Main 2023 Session 2. Candidates can apply at jeemain.nta.nic.in until March 30.",
                "publishedAt": current_date,
                "source": {"name": "Hindustan Times"},
                "url": "https://www.hindustantimes.com/education/competitive-exams/jee-main-2023-session-2-application",
                "category": "JEE"
            },
            {
                "title": "NEET UG 2023: Important Changes in Exam Pattern Announced",
                "description": "The National Medical Commission has announced key changes to the NEET UG 2023 exam pattern including revised marking scheme and question format.",
                "publishedAt": yesterday,
                "source": {"name": "India Today"},
                "url": "https://www.indiatoday.in/education/medical/story/neet-ug-2023-pattern-changes",
                "category": "NEET"
            },
            {
                "title": "GATE 2023 Results Declared: 18% Candidates Qualify",
                "description": "Indian Institute of Technology (IIT) Kanpur has released the GATE 2023 results. Around 18% of candidates have qualified the exam this year.",
                "publishedAt": two_days_ago,
                "source": {"name": "The Indian Express"},
                "url": "https://indianexpress.com/article/education/gate-2023-results-declared",
                "category": "GATE"
            },
            {
                "title": "New National Education Policy Implementation Updates",
                "description": "The Ministry of Education has released new guidelines for implementing the National Education Policy 2020 at school and higher education levels.",
                "publishedAt": two_days_ago,
                "source": {"name": "The Times of India"},
                "url": "https://timesofindia.indiatimes.com/education/news/new-education-policy-updates",
                "category": "Education"
            }
        ]
        
        # Use for display
        self.news_items = backup_news
    
    def update_loading_status(self, message):
        """Update the loading status message"""
        # Clear existing content
        for widget in self.news_container.winfo_children():
            widget.destroy()
        
        # Show loading message
        self.loading_label = ctk.CTkLabel(
            self.news_container,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#aaaaaa"
        )
        self.loading_label.pack(pady=30)
            
    def update_news_display(self):
        """Update the news display with fetched items"""
        # Clear loading indicator and existing content
        for widget in self.news_container.winfo_children():
            widget.destroy()
            
        if not self.news_items:
            # Show no news message
            no_news = ctk.CTkLabel(
                self.news_container,
                text="No recent news available",
                font=ctk.CTkFont(size=14),
                text_color="#aaaaaa"
            )
            no_news.pack(pady=30)
            return
            
        # Display each news item (matching the format in the screenshot)
        for article in self.news_items:
            self.create_news_item(article)
            
    def create_news_item(self, article):
        """Create a single news item display to match the image format"""
        # Main item frame
        item_frame = ctk.CTkFrame(self.news_container, fg_color="#252525", corner_radius=8, height=120)
        item_frame.pack(fill="x", pady=5, padx=5)
        item_frame.pack_propagate(False)
        
        # Title
        title = article.get('title', '')
        if len(title) > 100:
            title = title[:100] + "..."
            
        title_label = ctk.CTkLabel(
            item_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            justify="left",
            wraplength=280,
            anchor="w"
        )
        title_label.pack(fill="x", padx=12, pady=(12, 5), anchor="w")
        
        # Description (with fixed height)
        description = article.get('description', '')
        if len(description) > 120:
            description = description[:120] + "..."
            
        desc_label = ctk.CTkLabel(
            item_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="#cccccc",
            justify="left",
            wraplength=280,
            anchor="w"
        )
        desc_label.pack(fill="x", padx=12, pady=(0, 5), anchor="w")
        
        # Footer with source and date
        footer_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=12, pady=(0, 8), anchor="w")
        
        # Source and date
        source_name = article.get('source', {}).get('name', '')
        
        # Use provided publishedTime if available, otherwise extract from publishedAt
        if 'publishedTime' in article:
            date_str = article['publishedTime']
        else:
            try:
                date_obj = datetime.strptime(article['publishedAt'][:10], '%Y-%m-%d')
                date_str = date_obj.strftime('%d %b %Y')
            except:
                date_str = ""
        
        source_date_text = f"{source_name} • {date_str}" if source_name and date_str else (source_name or date_str)
        
        source_label = ctk.CTkLabel(
            footer_frame,
            text=source_date_text,
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        source_label.pack(side="left")
        
        # Read More button
        read_more_btn = ctk.CTkButton(
            footer_frame,
            text="Read More",
            command=lambda url=article['url']: self.open_article(url),
            width=80,
            height=25,
            font=ctk.CTkFont(size=11),
            fg_color="#2AB377",
            hover_color="#1C7F50",
            corner_radius=4
        )
        read_more_btn.pack(side="right")
        
        # Make the title and description clickable
        for widget in [item_frame, title_label, desc_label]:
            widget.bind("<Button-1>", lambda e, url=article['url']: self.open_article(url))
        
        # Add hover effect
        def on_enter(e):
            if e.widget != read_more_btn:
                item_frame.configure(fg_color="#303030")
            self.master.config(cursor="hand2")
            
        def on_leave(e):
            if e.widget != read_more_btn:
                item_frame.configure(fg_color="#252525")
            self.master.config(cursor="")
            
        for widget in [item_frame, title_label, desc_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
    def open_article(self, url):
        """Open the article URL in browser"""
        webbrowser.open(url)