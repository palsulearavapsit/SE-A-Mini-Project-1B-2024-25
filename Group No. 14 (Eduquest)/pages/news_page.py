import customtkinter as ctk
from tkinter import messagebox
import threading
import requests
from PIL import Image, ImageTk
import io
import webbrowser
from datetime import datetime, timedelta
from newsapi import NewsApiClient

class NewsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=("#000000", "#000000"))
        self.controller = controller
        
        # Initialize with your NewsAPI key
        self.api_key = "43ac41ed04cc4c37bb645b1eec69a443"  # Your actual API key
        self.newsapi = NewsApiClient(api_key=self.api_key)
        
        # Configure grid to fill the entire frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header row
        self.grid_rowconfigure(1, weight=1)  # Content row
        
        # Top header bar with back button, title, and refresh button
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#1a1a1a", "#1a1a1a"), height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_propagate(False)
        self.header_frame.grid_columnconfigure(0, weight=0)  # Back button
        self.header_frame.grid_columnconfigure(1, weight=1)  # Title
        self.header_frame.grid_columnconfigure(2, weight=0)  # Refresh button
        
        # Back button
        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="← Back",
            command=self.controller.show_dashboard_page,
            width=100,
            height=36,
            corner_radius=5,
            font=ctk.CTkFont(size=14),
            fg_color=("#2a2a2a", "#2a2a2a"),
            hover_color=("#3a3a3a", "#3a3a3a"),
            text_color=("#ffffff", "#ffffff")
        )
        self.back_button.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Exam News & Updates",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=12)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self.header_frame,
            text="Refresh",
            command=self.refresh_news,
            width=100,
            height=36,
            corner_radius=5,
            font=ctk.CTkFont(size=14),
            fg_color=("#00bd56", "#00bd56"),
            hover_color=("#00a851", "#00a851"),
            text_color=("#ffffff", "#ffffff")
        )
        self.refresh_button.grid(row=0, column=2, padx=20, pady=12, sticky="e")
        
        # Main content area (split into sidebar and content)
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#000000", "#000000"))
        self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar
        self.main_frame.grid_columnconfigure(1, weight=1)  # Content
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Sidebar for filters
        self.sidebar = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=("#000000", "#000000"), width=230)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        self.sidebar.grid_propagate(False)
        
        # Filter News header
        self.filter_header = ctk.CTkLabel(
            self.sidebar,
            text="Filter News",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.filter_header.pack(pady=(0, 20), anchor="w")
        
        # Time period header
        self.time_header = ctk.CTkLabel(
            self.sidebar,
            text="Time Period",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.time_header.pack(pady=(20, 15), anchor="w")
        
        # Time period filters
        self.selected_time = ctk.StringVar(value="week")
        
        # Today Radio Button
        self.today_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="Today",
            value="today",
            variable=self.selected_time,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.today_radio.pack(fill="x", pady=5, anchor="w")
        
        # This Week Radio Button
        self.week_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="This Week",
            value="week",
            variable=self.selected_time,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.week_radio.pack(fill="x", pady=5, anchor="w")
        self.week_radio.select()  # Select by default
        
        # This Month Radio Button
        self.month_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="This Month",
            value="month",
            variable=self.selected_time,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.month_radio.pack(fill="x", pady=5, anchor="w")
        
        # Exam Type Filter header
        self.exam_header = ctk.CTkLabel(
            self.sidebar,
            text="Exam Type",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.exam_header.pack(pady=(20, 15), anchor="w")
        
        # Exam type selection
        self.selected_exam = ctk.StringVar(value="all")
        
        # All Exams Radio Button
        self.all_exams_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="All Exams",
            value="all",
            variable=self.selected_exam,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.all_exams_radio.pack(fill="x", pady=5, anchor="w")
        self.all_exams_radio.select()  # Select by default
        
        # JEE Radio Button
        self.jee_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="JEE",
            value="JEE",
            variable=self.selected_exam,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.jee_radio.pack(fill="x", pady=5, anchor="w")
        
        # NEET Radio Button
        self.neet_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="NEET",
            value="NEET",
            variable=self.selected_exam,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.neet_radio.pack(fill="x", pady=5, anchor="w")
        
        # GATE Radio Button
        self.gate_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="GATE",
            value="GATE",
            variable=self.selected_exam,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.gate_radio.pack(fill="x", pady=5, anchor="w")
        
        # UPSC Radio Button
        self.upsc_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="UPSC",
            value="UPSC",
            variable=self.selected_exam,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.upsc_radio.pack(fill="x", pady=5, anchor="w")
        
        # CET Radio Button
        self.cet_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="CET",
            value="CET",
            variable=self.selected_exam,
            command=self.apply_filters,
            border_width_checked=8,
            fg_color="#00bd56",
            hover_color="#00a851",
            radiobutton_height=22,
            radiobutton_width=22,
            corner_radius=11
        )
        self.cet_radio.pack(fill="x", pady=5, anchor="w")
        
        # Content area with scrolling
        self.content_frame = ctk.CTkScrollableFrame(
            self.main_frame, 
            corner_radius=0,
            fg_color=("#000000", "#000000"),
            scrollbar_fg_color=("#000000", "#000000"),
            scrollbar_button_color=("#3a3a3a", "#3a3a3a"),
            scrollbar_button_hover_color=("#4a4a4a", "#4a4a4a")
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self.content_frame,
            text="Loading news...",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.grid(row=0, column=0, padx=20, pady=40)
        
        # News items list
        self.news_items = []
        
        # Start loading news in a separate thread
        threading.Thread(target=self.load_news, daemon=True).start()
    
    def load_news(self):
        """Load news using both the NewsAPI client and direct API requests"""
        try:
            # Get parameters from filters
            time_filter = self.selected_time.get()
            exam_filter = self.selected_exam.get()
            
            # Calculate date range
            if time_filter == "today":
                from_date = datetime.now().strftime('%Y-%m-%d')
            elif time_filter == "week":
                from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            else:  # month
                from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Try using the NewsAPI client first
            articles = self.fetch_news(from_date, exam_filter)
            
            # Process articles
            self.news_items = []
            for article in articles:
                try:
                    news_item = self.process_article(article, exam_filter)
                    if news_item:
                        self.news_items.append(news_item)
                except Exception as e:
                    print(f"Error processing article: {e}")
            
            # If no articles found, try direct API request as fallback
            if not self.news_items:
                self.try_direct_api_request(from_date, exam_filter)
            else:
                # Update UI in the main thread
                self.after(0, self.display_news)
                
        except Exception as e:
            print(f"Error loading news: {str(e)}")
            # Try direct API as fallback
            self.try_direct_api_request(from_date, exam_filter)
    
    def fetch_news(self, from_date, exam_filter="all"):
        """Fetch news related to competitive exams in India"""
        try:
            # Base query for education news
            base_query = 'education OR "entrance exam" OR "college admission"'
            
            # Add specific exam filter if selected
            if exam_filter != "all":
                query = f'{exam_filter} OR "{exam_filter} exam" OR "{exam_filter} preparation" OR "{exam_filter} result"'
            else:
                query = 'NEET OR JEE OR Graduate Aptitude Test in Engineering OR UPSC OR CET OR "entrance exam" OR "college admission"'
            
            # This approach uses OR operator properly
            news = self.newsapi.get_everything(
                q=query,
                language='en',
                from_param=from_date,
                sort_by='publishedAt',
                page_size=20
            )
            
            return news['articles'] if news['status'] == 'ok' else []
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []
    
    def try_direct_api_request(self, from_date, exam_filter="all"):
        """Try direct API request as fallback"""
        try:
            # Build query based on selected filter
            if exam_filter != "all":
                query = f'{exam_filter} OR "{exam_filter} exam" OR "{exam_filter} preparation" OR "{exam_filter} result"'
            else:
                query = "education OR entrance exam OR college admission OR JEE OR NEET OR Graduate Aptitude Test in Engineering OR UPSC OR CET"
            
            # Encode query
            encoded_query = requests.utils.quote(query)
            
            # Build URL
            url = f"https://newsapi.org/v2/everything?q={encoded_query}&from={from_date}&sortBy=publishedAt&apiKey={self.api_key}&language=en&pageSize=20"
            
            # Make request
            response = requests.get(url, timeout=15)
            
            # Process response
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "ok" and data["articles"]:
                    self.news_items = []
                    
                    # Process articles
                    for article in data["articles"]:
                        try:
                            news_item = self.process_article(article, exam_filter)
                            if news_item:
                                self.news_items.append(news_item)
                        except Exception as e:
                            print(f"Error processing article: {e}")
                    
                    # Display news
                    self.after(0, self.display_news)
                else:
                    # Try headlines as a last resort
                    self.try_headlines(exam_filter)
            else:
                # API error
                self.try_headlines(exam_filter)
                
        except Exception as e:
            print(f"Direct API request error: {str(e)}")
            self.try_headlines(exam_filter)
    
    def try_headlines(self, exam_filter="all"):
        """Try getting top headlines as last resort"""
        try:
            # Get headlines from India
            url = f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={self.api_key}&pageSize=15"
            
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "ok" and data["articles"]:
                    self.news_items = []
                    
                    # Process articles
                    for article in data["articles"]:
                        try:
                            news_item = self.process_article(article, exam_filter)
                            if news_item:
                                self.news_items.append(news_item)
                        except Exception as e:
                            print(f"Error processing headline: {e}")
                    
                    # Display news
                    self.after(0, self.display_news)
                else:
                    # Show no news message
                    self.after(0, lambda: self.show_no_news())
            else:
                # Show no news message
                self.after(0, lambda: self.show_no_news())
                
        except Exception as e:
            print(f"Headlines error: {str(e)}")
            self.after(0, lambda: self.show_no_news())
    
    def process_article(self, article, exam_filter="all"):
        """Process a news article into a standardized format"""
        if not article.get("title") or not article.get("description"):
            return None
            
        try:
            # Parse date
            pub_date_str = article.get("publishedAt", "")
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = pub_date.strftime("%Y-%m-%d")
            except ValueError:
                formatted_date = datetime.now().strftime("%Y-%m-%d")
            
            # Determine category based on content
            category = "Education"
            title = article["title"].upper()
            content = (article.get("description", "") + " " + article.get("content", "")).upper()
            
            # Check for exam keywords in title and content
            if "JEE" in title or "JEE" in content:
                category = "JEE"
            elif "NEET" in title or "NEET" in content:
                category = "NEET"
            elif "Graduate Aptitude Test in Engineering" in title or "Graduate Aptitude Test in Engineering" in content:
                category = "GATE"
            elif "CAT" in title or "CAT EXAM" in content:
                category = "CAT"
            elif "UPSC" in title or "UPSC" in content or "CIVIL SERVICE" in content:
                category = "UPSC"
            elif "CET" in title or "COMMON ENTRANCE TEST" in content:
                category = "CET"
                
            # Filter by exam type if specified
            if exam_filter != "all" and category != exam_filter:
                # Check if the exam filter term appears anywhere in the article content
                if exam_filter not in title and exam_filter not in content:
                    return None
                category = exam_filter
            
            # Create news item
            return {
                "title": article["title"],
                "summary": article.get("description", ""),
                "date": formatted_date,
                "source": article.get("source", {}).get("name", "Unknown"),
                "category": category,
                "url": article.get("url", ""),
                "image_url": article.get("urlToImage")
            }
        except Exception as e:
            print(f"Error processing article data: {e}")
            return None
    
    def display_news(self):
        """Display news items in the UI"""
        # Remove loading indicator
        self.loading_label.grid_forget()
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if not self.news_items:
            # Show message if no news found
            no_news_label = ctk.CTkLabel(
                self.content_frame,
                text="No news found matching your filters.\nTry different filter options or check back later.",
                font=ctk.CTkFont(size=16),
                text_color="#aaaaaa"
            )
            no_news_label.grid(row=0, column=0, padx=20, pady=40)
            return
        
        # Sort news by date (newest first)
        self.news_items.sort(key=lambda x: x["date"], reverse=True)
        
        # Add news items
        for i, news in enumerate(self.news_items):
            self.create_news_card(i, news)
    
    def create_news_card(self, row, news):
        """Create an improved card for a news item with category badge"""
        # Card with dark background
        card = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color=("#1a1a1a", "#1a1a1a"))
        card.grid(row=row, column=0, sticky="ew", padx=10, pady=8)
        card.grid_columnconfigure(0, weight=1)
        
        # Top row with date and category
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
        top_frame.grid_columnconfigure(0, weight=0)  # Date
        top_frame.grid_columnconfigure(1, weight=1)  # Spacer
        top_frame.grid_columnconfigure(2, weight=0)  # Category
        
        # Date at top left
        date_obj = datetime.strptime(news["date"], "%Y-%m-%d")
        date_label = ctk.CTkLabel(
            top_frame,
            text=date_obj.strftime("%d %b %Y"),
            font=ctk.CTkFont(size=12),
            text_color=("#6c757d", "#adb5bd")
        )
        date_label.grid(row=0, column=0, sticky="w")
        
        # Category badge with color
        category_colors = {
            "JEE": "#1976d2",      # Blue
            "NEET": "#388e3c",     # Green
            "GATE": "#d32f2f",     # Red
            "CAT": "#7b1fa2",      # Purple
            "Education": "#f57c00", # Orange
            "UPSC": "#9c27b0",     # Purple
            "CET": "#00796b"       # Teal
        }
        
        category_frame = ctk.CTkFrame(
            top_frame,
            fg_color=category_colors.get(news["category"], "#607d8b"),
            corner_radius=4,
            height=24
        )
        category_frame.grid(row=0, column=2, sticky="e")
        
        category_label = ctk.CTkLabel(
            category_frame,
            text=news["category"],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff",
            height=24
        )
        category_label.pack(padx=10, pady=0)
        
        # News title
        title_label = ctk.CTkLabel(
            card,
            text=news["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            wraplength=900,
            justify="left"
        )
        title_label.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # News summary
        summary_label = ctk.CTkLabel(
            card,
            text=news["summary"],
            font=ctk.CTkFont(size=14),
            anchor="w",
            wraplength=900,
            justify="left"
        )
        summary_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Source and read more button
        footer_frame = ctk.CTkFrame(card, fg_color="transparent")
        footer_frame.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)
        
        source_label = ctk.CTkLabel(
            footer_frame,
            text=f"Source: {news['source']}",
            font=ctk.CTkFont(size=12),
            text_color=("#6c757d", "#adb5bd")
        )
        source_label.grid(row=0, column=0, sticky="w")
        
        read_more_button = ctk.CTkButton(
            footer_frame,
            text="Read Full Article",
            width=120,
            height=28,
            command=lambda url=news["url"]: webbrowser.open(url),
            fg_color=("#00bd56", "#00bd56"),
            hover_color=("#00a851", "#00a851")
        )
        read_more_button.grid(row=0, column=1, sticky="e")
        
        # Make the entire card clickable
        for widget in [card, title_label, summary_label]:
            widget.bind("<Button-1>", lambda e, url=news["url"]: webbrowser.open(url))
            widget.configure(cursor="hand2")
    
    def apply_filters(self):
        """Apply selected filters to news"""
        # Clear existing news items
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show loading indicator
        self.loading_label = ctk.CTkLabel(
            self.content_frame,
            text="Loading news...",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.grid(row=0, column=0, padx=20, pady=40)
        
        # Reload news with new filters
        threading.Thread(target=self.load_news, daemon=True).start()
    
    def show_no_news(self):
        """Show message that no news could be found"""
        # Remove loading indicator if exists
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show message
        message_label = ctk.CTkLabel(
            self.content_frame,
            text="No news found matching your filters.\nTry different filter options or check back later.",
            font=ctk.CTkFont(size=16),
            text_color="#aaaaaa"
        )
        message_label.grid(row=0, column=0, padx=20, pady=40)
    
    def refresh_news(self):
        """Refresh news data"""
        # Clear existing news items
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show loading indicator
        self.loading_label = ctk.CTkLabel(
            self.content_frame,
            text="Loading news...",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.grid(row=0, column=0, padx=20, pady=40)
        
        # Reload news in a separate thread
        threading.Thread(target=self.load_news, daemon=True).start()