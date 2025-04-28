# Hey! This is our booking system for EV charging stations.
# We handle everything from slot selection to bill generation here.
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta

# Our color scheme - keeping it clean and professional
COLORS = {
    'primary': "#4CAF50",    # Nice green for main actions
    'secondary': "#2b2b2b",  # Dark theme background
    'accent': "#d77337",     # Orange pop for highlights
    'text_light': "#ffffff", # White text for dark backgrounds
    'text_dark': "#333333",  # Dark text for light backgrounds
    'warning': "#FFA500",    # Yellow for member-only slots
    'error': "#FF0000",      # Red for booked/unavailable
    'success': "#28a745",    # Green for success messages
    'card_bg': "#ffffff",    # White backgrounds
    'available': "#4CAF50",  # Green for available slots
    'booked': "#FF0000",     # Red for booked slots
    'selected': "#2196F3"    # Blue for selected slots
}

# Font styles to keep everything consistent
STYLES = {
    'title': ('Arial', 24, 'bold'),    # Big headers
    'subtitle': ('Arial', 18),         # Section headers
    'button': ('Arial', 16),           # Button text
    'text': ('Arial', 14),             # Regular text
    'small_text': ('Arial', 12)        # Small details
}

class BookingPage:
    """
    This is our main booking page where users can:
    - Pick a date and time slot
    - Choose between regular and emergency slots
    - See their membership benefits
    - Complete the booking process
    """
    def __init__(self, root, station_data, username):
        # Basic window setup - making it fullscreen
        self.root = root
        
        # Extract station data
        if isinstance(station_data, tuple):
            self.station_name = station_data[0]  # First element is name
            self.selected_state = station_data[4]  # Fifth element is location/state
        else:
            self.station_name = station_data
            self.selected_state = station_data
            
        self.root.title(f"Book Charging Slot - {self.station_name}")
        
        # Make it responsive
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set it to fullscreen with dark theme
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')
        self.root.config(bg=COLORS['secondary'])

        # Store important info
        self.selected_date = datetime.now()
        self.selected_slot = None
        self.username = username
        
        # Check if user is a member (for special slots and discounts)
        self.is_member = self.check_membership()

        # Main container for all our content
        self.container = tk.Frame(self.root, bg=COLORS['secondary'])
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Build our UI piece by piece
        self.create_header()
        self.content = tk.Frame(self.container, bg=COLORS['secondary'])
        self.content.pack(fill=tk.BOTH, expand=True, pady=20)
        self.create_booking_sections()

    def check_membership(self):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Shardul203",
                database="ev_station"
            )
            cursor = conn.cursor()
            
            current_date = datetime.now().date()
            cursor.execute("""SELECT up.is_member, up.membership_end_date FROM users u JOIN user_profiles up ON u.id = up.user_id WHERE u.username = %s""", (self.username,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result and result[0] and result[1] >= current_date:
                return True
            return False
            
        except mysql.connector.Error as e:
            print(f"Error checking membership: {e}")
            return False

    def create_header(self):
        header_frame = tk.Frame(self.container, bg=COLORS['secondary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(
            header_frame,
            text=f"Book Charging Slot at {self.station_name}",
            font=STYLES['title'],
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        title.pack(side=tk.LEFT)

        exit_btn = tk.Button(
            header_frame,
            text="Exit",
            font=STYLES['button'],
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            command=self.root.destroy
        )
        exit_btn.pack(side=tk.RIGHT)

    def create_booking_sections(self):
        # Main container split into left and right
        left_frame = tk.Frame(self.content, bg=COLORS['secondary'], width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(self.content, bg=COLORS['secondary'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Create date selection in left frame
        self.create_date_selection(left_frame)

        # Split right frame into three parts: slots, summary, and button
        slots_frame = tk.Frame(right_frame, bg=COLORS['secondary'])
        slots_frame.pack(fill=tk.BOTH, expand=True)

        summary_frame = tk.Frame(right_frame, bg=COLORS['card_bg'], height=150)
        summary_frame.pack(fill=tk.X, pady=5)
        summary_frame.pack_propagate(False)

        button_frame = tk.Frame(right_frame, bg=COLORS['card_bg'], height=80)
        button_frame.pack(fill=tk.X, pady=5)
        button_frame.pack_propagate(False)

        # Create sections
        self.create_time_slots_section(slots_frame)
        self.create_booking_summary(summary_frame)
        self.create_confirm_button(button_frame)

    def create_date_selection(self, parent):
        date_frame = tk.Frame(parent, bg=COLORS['card_bg'], padx=20, pady=20)
        date_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            date_frame,
            text="Select Date",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 10))

        date_select_frame = tk.Frame(date_frame, bg=COLORS['card_bg'])
        date_select_frame.pack(fill=tk.X, pady=10)

        dates = [(datetime.now() + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7)]
        
        self.date_var = tk.StringVar(value=dates[0])
        date_combo = ttk.Combobox(
            date_select_frame,
            values=dates,
            textvariable=self.date_var,
            state="readonly",
            font=STYLES['text'],
            width=15
        )
        date_combo.pack(pady=10)
        date_combo.bind('<<ComboboxSelected>>', self.update_time_slots)

        legend_frame = tk.Frame(date_frame, bg=COLORS['card_bg'])
        legend_frame.pack(fill=tk.X, pady=20)

        legends = [
            ("Available", COLORS['available']),
            ("Booked", COLORS['booked']),
            ("Members Only", COLORS['warning'])
        ]

        for text, color in legends:
            legend_item = tk.Frame(legend_frame, bg=COLORS['card_bg'])
            legend_item.pack(side=tk.LEFT, padx=10)

            tk.Label(
                legend_item,
                width=2,
                bg=color
            ).pack(side=tk.LEFT, padx=5)

            tk.Label(
                legend_item,
                text=text,
                font=STYLES['small_text'],
                bg=COLORS['card_bg'],
                fg=COLORS['text_dark']
            ).pack(side=tk.LEFT)

    def create_time_slots_section(self, parent):
        self.slots_frame = tk.Frame(parent, bg=COLORS['card_bg'])
        self.slots_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title frame
        title_frame = tk.Frame(self.slots_frame, bg=COLORS['card_bg'])
        title_frame.pack(fill=tk.X, pady=(0, 10))

        # Add tabs for Regular and Emergency slots
        tab_frame = tk.Frame(title_frame, bg=COLORS['card_bg'])
        tab_frame.pack(fill=tk.X)

        self.booking_type = tk.StringVar(value="regular")
        
        # Regular booking tab
        tk.Radiobutton(
            tab_frame,
            text="Regular Slots",
            variable=self.booking_type,
            value="regular",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            command=self.update_time_slots
        ).pack(side=tk.LEFT, padx=20)

        # Emergency booking tab
        tk.Radiobutton(
            tab_frame,
            text="Emergency Slots",
            variable=self.booking_type,
            value="emergency",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['error'],
            command=self.update_time_slots
        ).pack(side=tk.LEFT, padx=20)

        # Create scrollable frame for slots
        canvas = tk.Canvas(self.slots_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.slots_frame, orient="vertical", command=canvas.yview)
        
        self.slots_grid = tk.Frame(canvas, bg=COLORS['card_bg'])
        
        # Configure the canvas
        self.slots_grid.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.slots_grid, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configure mouse wheel scrolling
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass  # Silently handle the error if canvas is destroyed
        
        # Change this line
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Add this line to unbind when window closes
        self.root.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        self.update_time_slots()

    def get_booked_slots(self, date):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Shardul203",
                database="ev_station"
            )
            cursor = conn.cursor()
            
            # Get station_id first
            cursor.execute("SELECT station_id FROM stations WHERE name = %s", (self.station_name,))
            station_result = cursor.fetchone()
            
            if station_result:
                station_id = station_result[0]
                cursor.execute("""
                    SELECT time_slot 
                    FROM bookings 
                    WHERE booking_date = %s AND station_id = %s
                """, (date, station_id))
                
                booked_slots = [row[0] for row in cursor.fetchall()]
                cursor.close()
                conn.close()
                return booked_slots
            
            cursor.close()
            conn.close()
            return []
            
        except mysql.connector.Error as e:
            print(f"Error getting booked slots: {e}")
            return []

    def update_time_slots(self, event=None):
        for widget in self.slots_grid.winfo_children():
            widget.destroy()

        booked_slots = self.get_booked_slots(self.date_var.get())

        if self.booking_type.get() == "regular":
            self.create_regular_slots(booked_slots)
        else:
            self.create_emergency_slots(booked_slots)

    def create_regular_slots(self, booked_slots):
        regular_slots = [
            "06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", 
            "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM"
        ]

        tk.Label(
            self.slots_grid,
            text="Regular Slots (₹200)",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        for i, time in enumerate(regular_slots):
            slot_frame = tk.Frame(
                self.slots_grid,
                bg=COLORS['card_bg'],
                padx=10,
                pady=5
            )
            slot_frame.grid(row=(i//3)+1, column=i%3, padx=5, pady=5, sticky='nsew')

            if time in booked_slots:
                status = "booked"
            elif i % 3 == 2:  # Every third slot is members-only
                status = "members_only"
            else:
                status = "available"

            self.create_slot_button(slot_frame, time, status, "regular")

    def create_emergency_slots(self, booked_slots):
        emergency_slots = [
            "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM", "08:00 PM"
        ]

        # Add emergency slots header with price
        tk.Label(
            self.slots_grid,
            text="Emergency Slots (₹350)",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['error']
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Add emergency booking information
        info_frame = tk.Frame(self.slots_grid, bg=COLORS['warning'], padx=10, pady=5)
        info_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=5, pady=5)

        tk.Label(
            info_frame,
            text="• Priority access slots\n• Higher price includes emergency handling\n• Available for urgent charging needs",
            font=STYLES['small_text'],
            bg=COLORS['warning'],
            fg=COLORS['text_dark'],
            justify=tk.LEFT
        ).pack()

        for i, time in enumerate(emergency_slots):
            slot_frame = tk.Frame(
                self.slots_grid,
                bg=COLORS['card_bg'],
                padx=10,
                pady=5
            )
            slot_frame.grid(row=(i//3)+2, column=i%3, padx=5, pady=5, sticky='nsew')

            if time in booked_slots:
                status = "booked"
            else:
                status = "available"

            self.create_slot_button(slot_frame, time, status, "emergency")

    def create_slot_button(self, parent, time, status, slot_type):
        if status == "available":
            bg_color = COLORS['available']
            slot_command = lambda t=time, st=slot_type: self.select_slot(t, st)
            slot_text = time
        elif status == "booked":
            bg_color = COLORS['booked']
            slot_command = lambda t=time: self.show_booked_message()
            slot_text = f"{time}\n(Booked)"
        else:  # members_only
            bg_color = COLORS['warning']
            if self.is_member:
                slot_command = lambda t=time, st=slot_type: self.select_slot(t, st)
            else:
                slot_command = lambda t=time: self.show_members_only_message()
            slot_text = f"{time}\n(Members Only)"

        price_text = "₹350" if slot_type == "emergency" else "₹200"
        if status == "available":
            slot_text = f"{time}\n{price_text}"

        btn = tk.Button(
            parent,
            text=slot_text,
            font=STYLES['text'],
            bg=bg_color,
            fg=COLORS['text_light'],
            command=slot_command,
            wraplength=120,
            height=3
        )
        btn.pack(fill=tk.BOTH, expand=True)

    def select_slot(self, time, slot_type):
        self.selected_slot = time
        self.slot_type = slot_type
        self.update_summary()
        self.confirm_order_button.config(state='normal')

    def update_summary(self):
        if self.selected_slot:
            price = 350 if self.slot_type == "emergency" else 200
            if self.is_member and self.slot_type == "regular":
                price = 160  # 20% discount for members on regular slots

            summary_text = f"""Selected Date: {self.date_var.get()}
Selected Time: {self.selected_slot}
Slot Type: {"Emergency" if self.slot_type == "emergency" else "Regular"}
Location: {self.station_name}
Duration: 1 hour
Membership Status: {"Active" if self.is_member else "Non-member"}
{"Member Discount Applied" if self.is_member and self.slot_type == "regular" else ""}
Price: ₹{price}"""
            self.summary_details.config(text=summary_text)

    def show_booked_message(self):
        messagebox.showwarning("Slot Unavailable", "This slot is already booked.")

    def show_members_only_message(self):
        messagebox.showwarning(
            "Members Only",
            "This slot is reserved for membership users only.\n\n"
            "To access these slots:\n"
            "1. Go to your profile page\n"
            "2. Purchase a membership\n"
            "3. Return to booking after activation"
        )

    def create_booking_summary(self, parent):
        # Title
        tk.Label(
            parent,
            text="Booking Summary",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(pady=(10, 5))

        # Summary details
        self.summary_details = tk.Label(
            parent,
            text="Select a date and time slot to proceed",
            font=STYLES['text'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            justify=tk.LEFT,
            wraplength=400
        )
        self.summary_details.pack(padx=20, pady=5)

    def create_confirm_button(self, parent):
        # Confirm Order button in its own frame
        self.confirm_order_button = tk.Button(
            parent,
            text="Confirm Order",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            state='disabled',
            command=self.confirm_and_generate_bill,
            width=20,
            height=2
        )
        self.confirm_order_button.pack(pady=10)

    def confirm_and_generate_bill(self):
        if not self.selected_slot:
            messagebox.showerror("Error", "Please select a time slot first")
            return

        # Calculate price
        price = 350.00 if self.slot_type == "emergency" else (160.00 if self.is_member else 200.00)

        message = f"""Confirm booking for:
Date: {self.date_var.get()}
Time: {self.selected_slot}
Location: {self.station_name}
Price: ₹{price:.2f}"""
        
        if messagebox.askyesno("Confirm Booking", message):
            booking_id = self.save_booking()
            if booking_id:
                try:
                    bill_data = {
                        'bill_number': f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'booking_id': booking_id,
                        'customer': self.username,
                        'date': self.date_var.get(),
                        'time': self.selected_slot,
                        'location': self.station_name,
                        'total_amount': price
                    }
                    # Create a boolean flag to track if bill window is closed
                    self.bill_closed = False
                    
                    def on_bill_close():
                        self.bill_closed = True
                        bill_window.destroy()
                        messagebox.showinfo("Success", "Booking confirmed successfully!")
                        self.root.destroy()
                    
                    # Show bill window
                    bill_window = tk.Toplevel(self.root)
                    bill_window.title("Booking Bill")
                    bill_window.geometry("500x700")
                    bill_window.configure(bg=COLORS['card_bg'])
                    
                    # Center the window on screen
                    screen_width = bill_window.winfo_screenwidth()
                    screen_height = bill_window.winfo_screenheight()
                    x = (screen_width - 500) // 2
                    y = (screen_height - 700) // 2
                    bill_window.geometry(f"500x700+{x}+{y}")
                    
                    # Make the bill window modal
                    bill_window.transient(self.root)
                    bill_window.grab_set()
                    bill_window.focus_set()
                    
                    # Prevent closing the window with the X button
                    bill_window.protocol("WM_DELETE_WINDOW", lambda: None)

                    # Main container with padding
                    main_container = tk.Frame(bill_window, bg=COLORS['card_bg'], padx=30, pady=20)
                    main_container.pack(fill=tk.BOTH, expand=True)

                    # Title with company name
                    tk.Label(
                        main_container,
                        text="EV CHARGING STATION",
                        font=('Arial', 24, 'bold'),
                        bg=COLORS['card_bg'],
                        fg=COLORS['primary']
                    ).pack(pady=(0, 20))

                    # Separator
                    tk.Frame(main_container, height=2, bg=COLORS['primary']).pack(fill=tk.X, pady=10)

                    # Bill content
                    details = f"""
Bill Number: {bill_data['bill_number']}
Booking ID: {bill_data['booking_id']}

Booking Details:
---------------
Customer: {bill_data['customer']}
Date: {bill_data['date']}
Time: {bill_data['time']}
Location: {bill_data['location']}
Duration: 1 hour

Payment Details:
---------------
Membership Status: {"Active" if self.is_member else "Non-member"}
Amount: ₹{bill_data['total_amount']:.2f}
---------------

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Thank you for choosing our service!
"""
                    # Create a frame for bill details with white background
                    details_frame = tk.Frame(main_container, bg=COLORS['card_bg'], relief='ridge', bd=1)
                    details_frame.pack(fill=tk.BOTH, expand=True, pady=10)

                    # Add bill details with proper formatting
                    bill_text = tk.Label(
                        details_frame,
                        text=details,
                        font=('Courier', 12),
                        bg=COLORS['card_bg'],
                        fg=COLORS['text_dark'],
                        justify=tk.LEFT,
                        padx=20,
                        pady=20
                    )
                    bill_text.pack(fill=tk.BOTH, expand=True)

                    # Bottom separator
                    tk.Frame(main_container, height=2, bg=COLORS['primary']).pack(fill=tk.X, pady=10)

                    # Buttons frame
                    button_frame = tk.Frame(main_container, bg=COLORS['card_bg'])
                    button_frame.pack(pady=20)

                    # Print button
                    tk.Button(
                        button_frame,
                        text="Print",
                        font=STYLES['button'],
                        bg=COLORS['primary'],
                        fg=COLORS['text_light'],
                        command=lambda: self.print_bill(details),
                        width=10
                    ).pack(side=tk.LEFT, padx=10)

                    # OK button
                    tk.Button(
                        button_frame,
                        text="OK",
                        font=STYLES['button'],
                        bg=COLORS['accent'],
                        fg=COLORS['text_light'],
                        command=on_bill_close,
                        width=10
                    ).pack(side=tk.LEFT, padx=10)

                    # Wait for the bill window to be closed
                    self.root.wait_window(bill_window)
                    
                except Exception as e:
                    print(f"Error showing bill: {e}")
                    messagebox.showinfo("Success", "Booking confirmed! Check your profile for details.")
                    self.root.destroy()
            else:
                messagebox.showerror("Error", "Failed to save booking. Please try again.")

    def print_bill(self, bill_text):
        try:
            # You can implement actual printing here
            # For now, just show a message
            messagebox.showinfo("Print", "Bill sent to printer")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")

    def save_booking(self):
        conn = None
        cursor = None
        try:
            # Connect to database
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Shardul203",
                database="ev_station"
            )
            cursor = conn.cursor()

            # Get user_id
            cursor.execute("""
                SELECT u.id 
                FROM users u 
                WHERE u.username = %s AND u.status = 'active'
            """, (self.username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise Exception("Active user not found")
            user_id = user_result[0]

            # Get station_id using station name instead of state
            cursor.execute("""
                SELECT station_id 
                FROM stations 
                WHERE name = %s
            """, (self.station_name,))
            station_result = cursor.fetchone()

            if not station_result:
                raise Exception("Station not found")
            station_id = station_result[0]

            # Calculate price
            price = 350.00 if self.slot_type == "emergency" else (160.00 if self.is_member else 200.00)

            # Convert date string to date object
            booking_date = datetime.strptime(self.date_var.get(), '%Y-%m-%d').date()

            # Save booking
            cursor.execute("""
                INSERT INTO bookings 
                (user_id, station_id, booking_date, time_slot, price, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                station_id,
                booking_date,
                self.selected_slot,
                price,
                'confirmed'
            ))
            
            booking_id = cursor.lastrowid

            # Generate bill data
            bill_number = f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Save bill
            cursor.execute("""
                INSERT INTO booking_bills 
                (bill_id, booking_id, username, booking_date, booking_time, 
                location, amount, booking_type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                bill_number,
                booking_id,
                self.username,
                booking_date,
                self.selected_slot,
                self.station_name,
                price,
                'emergency' if self.slot_type == 'emergency' else 'regular'
            ))

            # Update available chargers
            cursor.execute("""
                UPDATE stations 
                SET available_chargers = available_chargers - 1 
                WHERE station_id = %s AND available_chargers > 0
            """, (station_id,))

            conn.commit()
            return booking_id

        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            print(f"Database error in save_booking: {e}")
            messagebox.showerror("Database Error", f"Failed to save booking: {str(e)}")
            return None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error in save_booking: {e}")
            messagebox.showerror("Error", f"Failed to save booking: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def main(root, station_data="Default Station", username=None):
    if username is None:
        messagebox.showerror("Error", "Please log in to book a slot")
        root.destroy()
        return
    booking_page = BookingPage(root, station_data, username)

if __name__ == "__main__":
    root = tk.Tk()
    main(root, "test_station", "test_user")
    root.mainloop()