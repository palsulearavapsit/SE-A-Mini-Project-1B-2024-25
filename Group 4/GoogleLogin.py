import os
import pickle
import mysql.connector
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from tkinter import messagebox

class GoogleAuth:
    def __init__(self):
        """Initialize Google Auth with necessary scopes and token directory."""
        self.SCOPES = [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ]
        self.CLIENT_SECRET_FILE = "client_secret.json"
        self.token_dir = "tokens"  # Directory to store authentication tokens

        if not os.path.exists(self.token_dir):
            os.makedirs(self.token_dir)

    def authenticate_user(self):
        """Handles Google OAuth and returns user info."""
        creds = None

        try:
            flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRET_FILE, self.SCOPES)
            creds = flow.run_local_server(port=0)

            service = build('oauth2', 'v2', credentials=creds)
            user_info = service.userinfo().get().execute()

            if not user_info or "email" not in user_info:
                return None  # Return None if authentication fails

            # Store the authentication token
            token_path = os.path.join(self.token_dir, f"{user_info['email']}.pickle")
            with open(token_path, "wb") as token_file:
                pickle.dump(creds, token_file)

            return user_info  # Return user details

        except Exception as e:
            print("Google authentication failed:", e)
            return None

    def store_or_fetch_user(self, email, name):
        """Stores a new user in the database or logs in an existing user."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if not existing_user:
                # Insert new user
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, "google_auth"))
                conn.commit()
                print("New user registered!")
                messagebox.showinfo("Signup Successful", f"Welcome, {name}!\nYour account has been created.")
            else:
                print("User exists. Logging in...")
                messagebox.showinfo("Login Successful", f"Welcome back, {name}!")

            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
