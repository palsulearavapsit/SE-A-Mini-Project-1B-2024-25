import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import create_connection

class VehicleRecommendationPage:
    def __init__(self, root, on_back):
        """
        Initialize the Vehicle Recommendation page.
        
        Args:
            root: The parent Tkinter window/container
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()

    def create_widgets(self):
        """
        Create and arrange all GUI widgets for the page.
        Sets up a scrollable interface with questions and recommendation results.
        """
        # Configure root grid
        self.root.grid_rowconfigure(1, weight=1)  # Middle row (content) expands
        self.root.grid_columnconfigure(0, weight=1)  # Single column expands
        
        # Fixed header (won't scroll)
        header = tk.Frame(self.root, bg="#4CAF50", height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)  # Center header content
        
        title_label = tk.Label(header, text="Find Your Vehicle", 
                font=("Arial", 22, "bold"), fg="white", bg="#4CAF50")
        title_label.grid(row=0, column=0, pady=15)

        # Scrollable canvas setup
        container = tk.Frame(self.root, bg="#f2f2f2")
        container.grid(row=1, column=0, sticky="nsew")
        
        canvas = tk.Canvas(container, bg="#f2f2f2", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f2f2f2")

        # Configure scroll region when frame size changes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Configure scrollable_frame for centering
        scrollable_frame.columnconfigure(0, weight=1)

        # Centered content container
        content = tk.Frame(scrollable_frame, bg="#f2f2f2")
        content.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        content.columnconfigure(0, weight=1)  # Enable centering of child widgets

        # Introduction text - centered
        intro = tk.Label(content,
                    text="Answer a few questions to get personalized vehicle ",
                    font=("Arial", 12),
                    bg="#f2f2f2",
                    wraplength=500,
                    justify="center")
        intro.grid(row=0, column=0, pady=(0, 20))

        # Form container (centered)
        form = tk.Frame(content, bg="#f2f2f2")
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)  # Enable centering of child widgets

        # Helper function for centered question frames
        def create_question(parent, text):
            """Create a labeled question frame with centered content"""
            frame = tk.LabelFrame(parent, text=text,
                                bg="#f2f2f2", padx=10, pady=5,
                                font=("Arial", 10, "bold"))
            frame.grid(column=0, pady=5, sticky="ew")
            
            inner = tk.Frame(frame, bg="#f2f2f2")
            inner.pack(anchor="center")  # Center the inner frame contents
            return inner

        # Question 1: Purpose
        q1 = create_question(form, "1. Purpose of Rental")
        self.purpose_var = tk.StringVar(value="Leisure")
        for purpose in ["Business", "Leisure", "Family Trip", "Adventure"]:
            ttk.Radiobutton(q1, text=purpose, variable=self.purpose_var,
                        value=purpose).pack(side="left", padx=15, pady=3)

        # Question 2: People
        q2 = create_question(form, "2. Number of People")
        self.people_var = tk.IntVar(value=2)
        ttk.Scale(q2, from_=1, to=10, orient="horizontal",
                variable=self.people_var, length=300,
                command=self.update_people_label).pack(side="left", padx=5)
        self.people_label = tk.Label(q2, text="2 People", bg="#f2f2f2", width=10)
        self.people_label.pack(side="left", padx=5)

        # Question 3: Luggage
        q3 = create_question(form, "3. Luggage Capacity Needed")
        self.luggage_var = tk.IntVar(value=2)
        ttk.Scale(q3, from_=0, to=5, orient="horizontal",
                variable=self.luggage_var, length=300,
                command=self.update_luggage_label).pack(side="left", padx=5)
        self.luggage_label = tk.Label(q3, text="2 Bags", bg="#f2f2f2", width=10)
        self.luggage_label.pack(side="left", padx=5)

        # Question 4: Fuel Type
        q4 = create_question(form, "4. Preferred Fuel Type")
        self.fuel_type_var = tk.StringVar(value="Petrol")
        for fuel in ["Petrol", "Diesel", "Electric"]:
            ttk.Radiobutton(q4, text=fuel, variable=self.fuel_type_var,
                        value=fuel).pack(side="left", padx=15, pady=3)

        # Question 5: Duration
        q5 = create_question(form, "5. Rental Duration (Days)")
        self.duration_var = tk.IntVar(value=3)
        ttk.Scale(q5, from_=1, to=30, orient="horizontal",
                variable=self.duration_var, length=300,
                command=self.update_duration_label).pack(side="left", padx=5)
        self.duration_label = tk.Label(q5, text="3 Days", bg="#f2f2f2", width=10)
        self.duration_label.pack(side="left", padx=5)

        # Question 6: Budget
        q6 = create_question(form, "6. Budget per day (₹)")
        self.budget_var = tk.IntVar(value=2000)
        ttk.Scale(q6, from_=500, to=10000, orient="horizontal",
                variable=self.budget_var, length=300,
                command=self.update_budget_label).pack(side="left", padx=5)
        self.budget_label = tk.Label(q6, text="₹2000", bg="#f2f2f2", width=10)
        self.budget_label.pack(side="left", padx=5)

        # Results section
        results = tk.LabelFrame(form, text="Recommendations",
                            bg="#f2f2f2", padx=10, pady=10,
                            font=("Arial", 10, "bold"))
        results.grid(column=0, pady=15, sticky="ew")
        
        self.results_text = scrolledtext.ScrolledText(results, height=8,
                                                    width=60, wrap=tk.WORD,
                                                    font=("Arial", 10))
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.results_text.insert(tk.END, "Your vehicle recommendations will appear here...")
        self.results_text.config(state=tk.DISABLED)

        # Fixed footer with buttons (won't scroll)
        footer = tk.Frame(self.root, bg="#f2f2f2", height=70)
        footer.grid(row=2, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)  # Center footer content
        
        btn_frame = tk.Frame(footer, bg="#f2f2f2")
        btn_frame.grid(row=0, column=0, pady=10)
        
        ttk.Button(btn_frame, text="Get Recommendations",
                command=self.get_recommendations,
                style="TButton").pack(side="left", padx=10, ipadx=10)
        
        ttk.Button(btn_frame, text="Reset Form",
                command=self.reset_form,
                style="TButton").pack(side="left", padx=10, ipadx=10)
        
        ttk.Button(btn_frame, text="Back to Homepage",
                command=self.on_back,
                style="TButton").pack(side="left", padx=10, ipadx=10) 
    
    # Update label functions
    def update_people_label(self, event=None):
        """
        Update the people count label when slider changes.
        
        Args:
            event: Optional event parameter (unused)
        """
        people = int(float(self.people_var.get()))
        self.people_label.config(text=f"{people} People")
        
    def update_luggage_label(self, event=None):
        """
        Update the luggage count label when slider changes.
        
        Args:
            event: Optional event parameter (unused)
        """
        luggage = int(float(self.luggage_var.get()))
        self.luggage_label.config(text=f"{luggage} Bags")
        
    def update_duration_label(self, event=None):
        """
        Update the duration label when slider changes.
        
        Args:
            event: Optional event parameter (unused)
        """
        duration = int(float(self.duration_var.get()))
        self.duration_label.config(text=f"{duration} Days")
        
    def update_budget_label(self, event=None):
        """
        Update the budget label when slider changes.
        
        Args:
            event: Optional event parameter (unused)
        """
        budget = int(float(self.budget_var.get()))
        self.budget_label.config(text=f"₹{budget}")

    def reset_form(self):
        """
        Reset the form to default values.
        Clears all user inputs and resets the recommendation results.
        """
        self.purpose_var.set("Leisure")
        self.people_var.set(2)
        self.luggage_var.set(2)
        self.fuel_type_var.set("Petrol")
        self.duration_var.set(3)
        self.budget_var.set(2000)
        
        # Update labels
        self.update_people_label()
        self.update_luggage_label()
        self.update_duration_label()
        self.update_budget_label()
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Your vehicle recommendations will appear here...")
        self.results_text.config(state=tk.DISABLED)

    def get_recommendations(self):
        """
        Get vehicle recommendations based on user inputs.
        Queries the database and applies scoring logic to find best matches.
        """
        purpose = self.purpose_var.get()
        num_people = int(self.people_var.get())
        luggage_capacity = int(self.luggage_var.get())
        fuel_type = self.fuel_type_var.get()
        rental_duration = int(self.duration_var.get())
        budget = int(self.budget_var.get())
        
        # Enable text widget for editing
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Build a sophisticated query with filtering
                query = """
                    SELECT 
                        v.id, 
                        v.name, 
                        v.model, 
                        v.type, 
                        v.luggage_capacity, 
                        v.fuel_type, 
                        v.price_per_day,
                        v.vehicle_number
                    FROM 
                        vehicles v
                    WHERE
                        v.price_per_day <= %s
                        AND (v.fuel_type = %s OR %s = '')
                    ORDER BY 
                        (CASE 
                            WHEN v.luggage_capacity >= %s THEN 0
                            ELSE 1
                        END),
                        ABS(v.price_per_day - %s)  -- Sort by closest to budget
                    LIMIT 10
                """
                
                # If any fuel type is acceptable
                actual_fuel_type = fuel_type if fuel_type != "Any" else ""
                
                cursor.execute(query, (budget, actual_fuel_type, actual_fuel_type, luggage_capacity, budget))
                vehicles = cursor.fetchall()
                
                # Apply additional filtering and scoring
                scored_vehicles = []
                
                for vehicle in vehicles:
                    v_id, name, model, v_type, v_luggage, v_fuel, price, v_number = vehicle
                    
                    # Base score starts at 0
                    score = 0
                    
                    # Type matching based on purpose and people
                    if v_type == "SUV" and (purpose in ["Family Trip", "Adventure"] or num_people > 4):
                        score += 30
                    elif v_type == "Sedan" and purpose in ["Business", "Leisure"] and num_people <= 4:
                        score += 30
                    elif v_type == "Hatchback" and purpose in ["Leisure"] and num_people <= 4:
                        score += 30
                    elif v_type == "Bike" and purpose in ["Adventure"] and num_people == 1:
                        score += 30
                    
                    # Luggage capacity
                    if v_luggage >= luggage_capacity:
                        score += 20
                    else:
                        score += max(0, 10 - 5*(luggage_capacity - v_luggage))
                    
                    # Fuel type match
                    if v_fuel == fuel_type:
                        score += 20
                    
                    # Budget match (higher score for prices closer to budget)
                    price_diff_ratio = abs(price - budget) / budget
                    budget_score = 20 * (1 - min(price_diff_ratio, 1))
                    score += budget_score
                    
                    # Add to scored vehicles list
                    scored_vehicles.append({
                        'id': v_id,
                        'name': name,
                        'model': model,
                        'type': v_type,
                        'luggage': v_luggage,
                        'fuel': v_fuel,
                        'price': price,
                        'number': v_number,
                        'score': score
                    })
                
                # Sort by score descending
                scored_vehicles.sort(key=lambda x: x['score'], reverse=True)
                
                # Display results
                if scored_vehicles:
                    self.results_text.insert(tk.END, "Top Recommendations For You:\n\n")
                    
                    for i, vehicle in enumerate(scored_vehicles[:5]):  # Show top 5
                        self.results_text.insert(tk.END, f"{i+1}. {vehicle['name']} {vehicle['model']} ({vehicle['type']})\n")
                        self.results_text.insert(tk.END, f"   • Fuel Type: {vehicle['fuel']}\n")
                        self.results_text.insert(tk.END, f"   • Luggage Capacity: {vehicle['luggage']} bags\n")
                        self.results_text.insert(tk.END, f"   • Price: ₹{vehicle['price']}/day (₹{vehicle['price']*rental_duration} for {rental_duration} days)\n")
                        self.results_text.insert(tk.END, f"   • Vehicle #: {vehicle['number']}\n\n")
                    
                    self.results_text.insert(tk.END, "To rent any of these vehicles, please use the 'Rent Vehicle' option from the menu.")
                else:
                    self.results_text.insert(tk.END, "No suitable vehicles found based on your preferences.\n\n")
                    self.results_text.insert(tk.END, "Try adjusting your criteria to find available vehicles.")
            except Exception as e:
                self.results_text.insert(tk.END, f"Error fetching recommendations: {str(e)}\n")
                print(f"Database error: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            self.results_text.insert(tk.END, "Could not connect to the database. Please try again later.")
            
        # Disable text widget after updating content
        self.results_text.config(state=tk.DISABLED)

    def score_vehicle_for_purpose(self, vehicle_type, purpose, num_people):
        """
        Determine how well a vehicle type fits a given purpose and number of people.
        
        Args:
            vehicle_type: Type of vehicle (SUV, Sedan, etc.)
            purpose: Rental purpose (Business, Leisure, etc.)
            num_people: Number of people in the rental party
            
        Returns:
            int: Score representing how well the vehicle fits the requirements
        """
        score = 0
        
        # SUV scoring
        if vehicle_type == "SUV":
            if purpose in ["Family Trip", "Adventure"]:
                score += 10
            if num_people >= 5 and num_people <= 7:
                score += 10
            elif num_people > 7:
                score -= 5  # Too many people even for an SUV
        
        # Sedan scoring
        elif vehicle_type == "Sedan":
            if purpose in ["Business", "Leisure"]:
                score += 10
            if num_people >= 2 and num_people <= 4:
                score += 10
            elif num_people > 4:
                score -= 10  # Too many people for a sedan
        
        # Hatchback scoring
        elif vehicle_type == "Hatchback":
            if purpose in ["Leisure", "Business"]:
                score += 8
            if num_people >= 1 and num_people <= 4:
                score += 8
            elif num_people > 4:
                score -= 10  # Too many people for a hatchback
        
        # Bike scoring
        elif vehicle_type == "Bike":
            if purpose in ["Adventure", "Leisure"]:
                score += 8
            if num_people == 1:
                score += 10
            elif num_people == 2:
                score += 5  # Possible but not ideal
            else:
                score -= 20  # Not suitable for more than 2
        
        return score