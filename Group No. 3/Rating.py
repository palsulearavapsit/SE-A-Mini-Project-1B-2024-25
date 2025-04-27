import tkinter as tk
from tkinter import messagebox
import mysql.connector

from config import get_db_connection

class RatingPage:
    def __init__(self, parent, recipe_id):
        self.parent = parent
        self.recipe_id = recipe_id
        self.rating = 0  # Default rating

        # Create a top-level window
        self.top = tk.Toplevel(parent)
        self.top.title("Rate This Recipe")
        self.top.geometry("400x300")
        self.top.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Main message
        tk.Label(self.top, text="Rate us!", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Star rating widget
        self.star_frame = tk.Frame(self.top)
        self.star_frame.pack(pady=20)
        
        self.stars = []
        for i in range(5):
            star = tk.Label(self.star_frame, text="☆", font=("Arial", 24))
            star.pack(side=tk.LEFT, padx=2)
            star.bind("<Button-1>", lambda e, idx=i+1: self.set_rating(idx))
            star.bind("<Enter>", lambda e, idx=i+1: self.preview_rating(idx))
            star.bind("<Leave>", lambda e: self.preview_rating(self.rating))
            self.stars.append(star)
        
        # Buttons frame
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Done", command=self.on_done, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="No Thanks", command=self.on_cancel, width=10).pack(side=tk.LEFT, padx=10)
        
        # Initialize stars to empty
        self.preview_rating(0)
    
    def set_rating(self, rating):
        self.rating = rating
        self.preview_rating(rating)
    
    def preview_rating(self, rating):
        for i in range(5):
            if i < rating:
                self.stars[i].config(text="★", fg="gold")
            else:
                self.stars[i].config(text="☆", fg="black")
    
    def on_done(self):
        if self.rating == 0:
            messagebox.showwarning("No Rating", "Please select a rating before submitting.")
            return
        
        conn = None
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # Get current rating from database
                cursor.execute("SELECT ratings FROM recipes WHERE recipe_id = %s", (self.recipe_id,))
                result = cursor.fetchone()
                
                if result:
                    current_rating = float(result[0]) if result[0] else 0.0
                    # Calculate new average rating
                    new_rating = (current_rating + self.rating) / 2
                    
                    # Update database with new rating
                    cursor.execute("UPDATE recipes SET ratings = %s WHERE recipe_id = %s", 
                                (new_rating, self.recipe_id))
                    conn.commit()
                    
                    messagebox.showinfo("Thank You", f"Thank you for your rating!")
                else:
                    messagebox.showerror("Error", "Recipe not found in database.")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        self.top.destroy()
    
    def on_cancel(self):
        self.top.destroy()