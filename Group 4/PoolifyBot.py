import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from threading import Thread
import time
import HomePage
import SettingsPage

# Import your existing backend components
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FAISS_PATH = os.path.join(BASE_DIR, "vectorstore", "db_faiss")
HF_TOKEN = os.environ.get("HF_TOKEN")

# Global caches for resources
_vectorstore = None
_embedding_model = None


def get_embedding_model():
    """Cache and return the embedding model"""
    global _embedding_model
    if _embedding_model is None:
        logger.info("Loading embedding model...")
        _embedding_model = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            cache_folder=os.path.join(BASE_DIR, "model_cache"),  # Local cache
            encode_kwargs={'batch_size': 32}  # Larger batch for efficiency
        )
    return _embedding_model


def get_vectorstore():
    """Cache and return the vectorstore"""
    global _vectorstore
    if _vectorstore is None:
        try:
            # Get cached embedding model
            embedding_model = get_embedding_model()

            if not os.path.exists(os.path.join(DB_FAISS_PATH, "index.faiss")):
                logger.warning(f"FAISS index not found at {DB_FAISS_PATH}")
                return None

            logger.info("Loading vector store...")
            _vectorstore = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
            logger.info("Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    return _vectorstore


def set_custom_prompt(custom_prompt_template):
    prompt = PromptTemplate(
        template=custom_prompt_template,
        input_variables=["context", "question"]
    )
    return prompt


def load_llm(huggingface_repo_id):
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN environment variable is not set")

    try:
        logger.info(f"Initializing LLM: {huggingface_repo_id}")
        llm = HuggingFaceEndpoint(
            repo_id=huggingface_repo_id,
            huggingfacehub_api_token=HF_TOKEN,
            task="text-generation",
            temperature=0.5,
            top_p=0.95,
            max_new_tokens=512,
            timeout=60
        )
        return llm
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise


class LoadingScreen:
    def __init__(self, parent):
        self.parent = parent

        # Center frame for loading content
        self.frame = ttk.Frame(parent, padding=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo/title
        self.title_label = ttk.Label(
            self.frame,
            text="Poolify-Bot 🤖",
            font=("Segoe UI", 28, "bold"),
            foreground="#4a86e8"
        )
        self.title_label.pack(pady=(0, 30))

        # Loading message
        self.message_var = tk.StringVar(value="Initializing application...")
        self.message_label = ttk.Label(
            self.frame,
            textvariable=self.message_var,
            font=("Segoe UI", 12)
        )
        self.message_label.pack(pady=(0, 20))

        # Progress bar - using determinate mode
        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.pack(pady=(0, 30))

        # Status messages
        self.status_var = tk.StringVar(value="Starting...")
        self.status_label = ttk.Label(
            self.frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            foreground="gray"
        )
        self.status_label.pack()

        # For tracking loading progress
        self.total_steps = 3
        self.current_step = 0

    def update_status(self, message):
        self.status_var.set(message)
        self.parent.update()

    def update_message(self, message):
        self.message_var.set(message)
        self.parent.update()

    def next_step(self, message):
        """Update progress to next step with a message"""
        self.current_step += 1
        progress_value = (self.current_step / self.total_steps) * 100
        self.progress["value"] = progress_value
        self.update_status(message)
        self.parent.update()

    def close(self):
        self.frame.destroy()


class PoolifyBotApp(tk.Tk):
    def __init__(self, user_email,user_type):
        super().__init__()
        self.geometry("1280x720")
        self.minsize(800, 600)
        self.configure(bg="white")
        self.title("Poolify-Bot")

        # Store image references to prevent garbage collection
        self.image_references = []

        # Save user email
        self.user_email = user_email
        self.user_type = user_type

        # Initialize loading screen
        self.loading_screen = LoadingScreen(self)

        # Start with Step 1: Initialize minimal data structures
        self.loading_screen.next_step("Configuring application...")

        # Initialize state variables - fast operation
        self.current_category = "General"
        self.vectorstore = None  # Will be loaded in background
        self.faqs_by_category = self.organize_faqs()

        # Move to Step 2: Setup the UI
        self.loading_screen.next_step("Preparing interface...")

        # Start interface setup immediately
        self.after(10, self.setup_main_interface)

    def load_vectorstore_background(self):
        """Background thread to load vectorstore"""
        try:
            # Load vectorstore
            self.vectorstore = get_vectorstore()

            # Update UI based on result (using after to schedule UI updates on main thread)
            if self.vectorstore:
                self.after(0, lambda: self.status_var.set("Ready"))
                self.after(0, lambda: self.status_label.configure(foreground="green"))
                self.after(0, lambda: self.add_message(
                    "Knowledge base loaded successfully! You can now ask questions about Poolify.", "system"))
            else:
                self.after(0, lambda: self.status_var.set("Limited mode (no knowledge base)"))
                self.after(0, lambda: self.status_label.configure(foreground="orange"))
                self.after(0,
                           lambda: self.add_message("Warning: Knowledge base not found. Some features may be limited.",
                                                    "system"))

        except Exception as e:
            logger.error(f"Error loading vector store in background: {str(e)}")
            self.after(0, lambda: self.status_var.set("Error loading knowledge base"))
            self.after(0, lambda: self.status_label.configure(foreground="red"))
            self.after(0, lambda: self.add_message(f"Error loading knowledge base: {str(e)}", "system"))

    def setup_main_interface(self):
        """Set up the main interface without waiting for vectorstore"""
        # Final step in loading screen
        self.loading_screen.next_step("Setting up interface...")

        # Remove loading screen
        self.loading_screen.close()

        # Create the main interface
        self.create_widgets()

        # Launch vectorstore loading in background
        Thread(target=self.load_vectorstore_background, daemon=True).start()

    def organize_faqs(self):
        """Organize FAQs by category"""
        return {
            "General": [
                "What is a carpooling app?",
                "How does a carpooling app work?",
                "Is carpooling safe?",
                "Who can use a carpooling app?",
                "Is the carpooling app free to use?"
            ],
            "Registration": [
                "How do I sign up for the app?",
                "Why do I need to verify my identity?",
                "Can I use the app without verifying my profile?",
                "How do I update my profile information?",
                "Can I delete my account?"
            ],
            "Booking": [
                "How do I book a ride?",
                "Can I schedule a ride in advance?",
                "How do I know if my booking is confirmed?",
                "What happens if a driver cancels my ride?",
                "Can I cancel a booking?"
            ],
            "Payments": [
                "How much does a ride cost?",
                "What payment methods are accepted?",
                "Is there a refund policy?",
                "How do I apply a promo code?",
                "How is the fare calculated for long-distance trips?"
            ],
            "Drivers": [
                "How do I register as a driver?",
                "Can I choose which passengers to pick up?",
                "What should I do if a passenger misbehaves?",
                "How are earnings calculated?",
                "How do I withdraw my earnings?"
            ],
            "Safety": [
                "What safety features does the app have?",
                "Can I share my ride details with someone?",
                "What should I do in case of an emergency?",
                "Are passengers and drivers insured?",
                "How do I report a safety concern?"
            ],
            "Technical": [
                "Why isn't the app working?",
                "I forgot my password. How do I reset it?",
                "The app crashed during a ride. What should I do?",
                "Why am I not receiving notifications?",
                "How do I contact customer support?"
            ],
            "Routes": [
                "What are the popular intercity routes available?",
                "What is the fare from Mumbai to Pune?",
                "How much does a ride from Bangalore to Mysore cost?",
                "What is the distance and fare between Delhi and Agra?",
                "Are there any discounts for frequently traveled routes?"
            ]
        }

    def create_widgets(self):
        # Create main layout using grid to maximize space
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title row
        self.grid_rowconfigure(1, weight=1)  # Chat area (expand to fill space)
        self.grid_rowconfigure(2, weight=0)  # Input row

        # Main container with padding
        main_container = ttk.Frame(self, padding=20)
        main_container.grid(row=0, column=0, rowspan=3, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=3)  # Chat area column
        main_container.grid_columnconfigure(1, weight=1)  # FAQ sidebar column
        main_container.grid_rowconfigure(0, weight=0)  # Back button row
        main_container.grid_rowconfigure(1, weight=0)  # Header row
        main_container.grid_rowconfigure(2, weight=1)  # Content row
        main_container.grid_rowconfigure(3, weight=0)  # Input row
        main_container.grid_rowconfigure(4, weight=0)  # Footer row

        # Back button at top left corner - in its own row for visibility
        back_button_frame = ttk.Frame(main_container)
        back_button_frame.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.back_button = ttk.Button(back_button_frame, text="← Back", command=self.go_home_back)
        self.back_button.pack(side=tk.LEFT)

        # Header section - now in row 1 instead of row 0
        header_frame = ttk.Frame(main_container)
        header_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(header_frame, text="Poolify-Bot 🤖", font=("Segoe UI", 20, "bold"))
        title_label.pack(side=tk.TOP)

        # Status indicator - starts as "Loading..."
        self.status_var = tk.StringVar(value="Initializing...")
        self.status_label = ttk.Label(header_frame, textvariable=self.status_var, foreground="orange")
        self.status_label.pack(side=tk.TOP, pady=(5, 0))

        # Contact Us button at top right
        contact_button_frame = ttk.Frame(main_container)
        contact_button_frame.grid(row=1, column=1, sticky="e", pady=(0, 15))

        self.contact_button = ttk.Button(contact_button_frame, text="Contact Us", command=self.show_contact_info)
        self.contact_button.pack(side=tk.RIGHT)

        # Content section - contains chat area and FAQ sidebar - now in row 2
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Chat area (left side) - Increased size
        chat_container = ttk.Frame(content_frame)
        chat_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)

        self.chat_display = scrolledtext.ScrolledText(chat_container, wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat_display.grid(row=0, column=0, sticky="nsew")
        self.chat_display.config(state=tk.DISABLED)

        # FAQ sidebar (right side)
        faq_container = ttk.Frame(content_frame)
        faq_container.grid(row=0, column=1, sticky="nsew")
        faq_container.grid_rowconfigure(0, weight=0)
        faq_container.grid_rowconfigure(1, weight=1)
        faq_container.grid_columnconfigure(0, weight=1)

        # Category selector
        category_frame = ttk.Frame(faq_container)
        category_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(category_frame, text="FAQ Category:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0, 5))

        self.category_var = tk.StringVar(value="General")
        categories = ["General", "Registration", "Booking", "Payments", "Drivers", "Safety", "Technical", "Routes"]

        category_dropdown = ttk.Combobox(category_frame, textvariable=self.category_var,
                                         values=categories, width=15, state="readonly", font=("Segoe UI", 10))
        category_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        category_dropdown.bind("<<ComboboxSelected>>", self.update_quick_buttons)

        # FAQ buttons container with scrollbar
        faq_scroll_container = ttk.Frame(faq_container)
        faq_scroll_container.grid(row=1, column=0, sticky="nsew")
        faq_scroll_container.grid_rowconfigure(0, weight=1)
        faq_scroll_container.grid_columnconfigure(0, weight=1)

        # Canvas for scrollable content
        faq_canvas = tk.Canvas(faq_scroll_container)
        faq_scrollbar = ttk.Scrollbar(faq_scroll_container, orient="vertical", command=faq_canvas.yview)

        self.quick_frame = ttk.Frame(faq_canvas)

        # Configure scrolling
        faq_canvas.configure(yscrollcommand=faq_scrollbar.set)
        faq_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        faq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create window inside canvas for buttons
        faq_canvas_window = faq_canvas.create_window((0, 0), window=self.quick_frame, anchor="nw")

        # Configure the quick frame to fill the canvas width
        def configure_quick_frame(event):
            faq_canvas.itemconfig(faq_canvas_window, width=event.width)

        faq_canvas.bind("<Configure>", configure_quick_frame)
        self.quick_frame.bind("<Configure>", lambda e: faq_canvas.configure(scrollregion=faq_canvas.bbox("all")))

        # Input area - now in row 3
        input_frame = ttk.Frame(main_container)
        input_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda event: self.send_message())

        # Footer - now in row 4
        footer_frame = ttk.Frame(main_container)
        footer_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        footer_label = ttk.Label(footer_frame, text="Powered by Mistral-7B-Instruct",
                                 foreground="gray", font=("Segoe UI", 8))
        footer_label.pack()

        # Add welcome message
        self.add_message(
            "Welcome to Poolify-Bot! I can answer questions about carpooling and help with your Poolify experience. Select a category above to see common questions, or type your own question below.",
            "assistant")

        # Add loading message
        self.add_message(
            "Knowledge base is loading in the background. You can start asking simple questions right away.", "system")

        # Initialize quick buttons
        self.update_quick_buttons()

    def go_home_back(self):
        self.destroy()
        if self.user_type == "driver":
            import DriverHomePage
            DriverHomePage.HomePage(self.user_email)
        else:  # passenger
            import HomePage
            HomePage.HomePage(self.user_email)

    def show_contact_info(self):
        """Show contact information dialog"""
        result = messagebox.askquestion("Go to Contact Page", "Are you sure you want to go to Contact Page?")
        if result == "yes":
            # Close the current window
            self.destroy()
            # Create a new instance of AppBase with the user's email
            contact_app = SettingsPage.AppBase(self.user_email,self.user_type)
            contact_app.create_contact_us_content()
            contact_app.mainloop()

    def update_quick_buttons(self, event=None):
        """Update quick buttons based on selected category"""
        category = self.category_var.get()

        # Clear existing buttons
        for widget in self.quick_frame.winfo_children():
            widget.destroy()

        # Add new buttons for the selected category
        for question in self.faqs_by_category.get(category, []):
            btn = ttk.Button(self.quick_frame, text=question,
                             command=lambda q=question: self.handle_quick_response(q),
                             style="FAQ.TButton")
            btn.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3)

        # Configure style for FAQ buttons
        style = ttk.Style()
        style.configure("FAQ.TButton", wraplength=200, font=("Segoe UI", 10))

    def add_message(self, text, sender):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)

        if sender == "user":
            self.chat_display.insert(tk.END, "You: ", "user_tag")
            self.chat_display.insert(tk.END, f"{text}\n\n", "user_msg")
        elif sender == "assistant":
            self.chat_display.insert(tk.END, "🤖 Poolify-Bot: ", "bot_tag")
            self.chat_display.insert(tk.END, f"{text}\n\n", "bot_msg")
        elif sender == "system":
            self.chat_display.insert(tk.END, f"System: {text}\n\n", "system_msg")

        # Configure tags
        self.chat_display.tag_config("user_tag", foreground="#4a86e8", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("user_msg", foreground="black", font=("Segoe UI", 11))
        self.chat_display.tag_config("bot_tag", foreground="#4a86e8", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("bot_msg", foreground="black", font=("Segoe UI", 11))
        self.chat_display.tag_config("system_msg", foreground="gray", font=("Segoe UI", 10, "italic"))

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def handle_quick_response(self, text):
        """Handle a quick response button click"""
        self.user_input.delete(0, tk.END)
        self.user_input.insert(0, text)
        self.send_message()

    def send_message(self):
        """Send the user message and get a response"""
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        # Clear input field
        self.user_input.delete(0, tk.END)

        # Display user message
        self.add_message(user_text, "user")

        # Disable input during processing
        self.user_input.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        # Process in background thread
        def process_response():
            try:
                # Only show "Thinking..." if vectorstore is loaded - keeps UI cleaner
                if self.vectorstore:
                    self.add_message("Thinking...", "system")

                # Check if model is ready
                if not self.vectorstore:
                    response = "I'm still loading my knowledge base. I can answer basic questions, but for detailed carpooling information, please wait a moment until loading completes."
                elif not HF_TOKEN:
                    response = "API token not configured. Please set up your HF_TOKEN."
                else:
                    # Your existing code for processing queries
                    custom_prompt_template = """
                    Use the pieces of information provided in the context to answer user's question about Poolify carpooling app.
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.
                    Don't provide anything out of the given context.

                    Context: {context}
                    Question: {question}

                    Start the answer directly. Keep responses concise and helpful.
                    """

                    HUGGING_FACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

                    # Load LLM just when needed (lazy loading)
                    llm = load_llm(huggingface_repo_id=HUGGING_FACE_REPO_ID)

                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": set_custom_prompt(custom_prompt_template)}
                    )

                    result = qa_chain.invoke({'query': user_text})

                    if isinstance(result, dict) and 'result' in result:
                        response = result['result']
                    else:
                        response = str(result)

                # Remove the "Thinking..." message if it exists
                if self.vectorstore:
                    self.chat_display.config(state=tk.NORMAL)
                    # Find and remove the last "Thinking..." message
                    last_pos = self.chat_display.search("System: Thinking...", "1.0", tk.END)
                    if last_pos:
                        line_start = last_pos
                        line_end = self.chat_display.search("\n\n", last_pos, tk.END)
                        if line_end:
                            self.chat_display.delete(line_start, line_end + "+2c")
                    self.chat_display.config(state=tk.DISABLED)

                # Add the bot response
                self.add_message(response, "assistant")

            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                self.add_message("Sorry, I encountered an issue processing your request. Please try again later.",
                                 "system")

            finally:
                # Re-enable input
                self.after(0, lambda: self.user_input.config(state=tk.NORMAL))
                self.after(0, lambda: self.send_button.config(state=tk.NORMAL))
                self.after(0, lambda: self.user_input.focus())

        Thread(target=process_response, daemon=True).start()


if __name__ == "__main__":
    user_email = 'user@example.com'
    user_type = "user"
    app = PoolifyBotApp(user_email,user_type)
    app.mainloop()