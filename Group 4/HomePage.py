import http.server
import urllib.parse
import urllib.request
import json
import threading
import webbrowser
import os
import io
from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Button, PhotoImage, Label, Frame, messagebox
import mysql.connector
from PIL import Image, ImageTk
import CreateRide
import SearchRide
import SettingsPage
import HistoryPage
import WelcomePage
import WalletPage
import PassengerProfile
import PoolifyBot

class LocationHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/set_location'):
            parsed_url = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed_url.query)
            try:
                lat = float(params.get('lat', ['0'])[0])
                lng = float(params.get('lng', ['0'])[0])

                # Validate coordinates
                if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                    raise ValueError("Invalid coordinates")

                # Use a temporary file and atomic rename to prevent concurrent access
                import tempfile
                import os

                # Create a temporary file in the same directory
                temp_file = tempfile.mktemp(dir=os.path.dirname("location_data.json"))

                # Write to the temporary file with additional safety
                try:
                    with open(temp_file, "w") as f:
                        # Use os.fsync to ensure data is written to disk
                        json.dump({"lat": lat, "lng": lng}, f)
                        f.flush()
                        os.fsync(f.fileno())

                    # Atomically rename the file
                    os.replace(temp_file, "location_data.json")

                except (IOError, OSError) as file_error:
                    # Log the specific file operation error
                    print(f"File operation error: {file_error}")
                    raise

                # Logging for tracking
                print(f"Location updated: Lat {lat}, Lng {lng}")

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b"Location received")

            except ValueError as val_error:
                # Handle coordinate validation errors
                print(f"Validation error: {val_error}")
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(f"Invalid coordinates: {str(val_error)}".encode())

            except Exception as e:
                # Catch-all for unexpected errors with detailed logging
                print(f"Unexpected error in location handling: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(f"Server error: {str(e)}".encode())

        else:
            super().do_GET()



class GoogleMapWidget(tk.Frame):
    def __init__(self, master, width=500, height=450, initial_location=(40.6302, -74.0252), zoom=13, api_key=None):
        super().__init__(master, width=width, height=height)
        self.pack_propagate(False)

        self.width = width
        self.height = height
        self.api_key = api_key
        self.markers = []

        # Default location (Bay Ridge)
        self.latitude = initial_location[0]
        self.longitude = initial_location[1]
        self.zoom = zoom

        # Create canvas to display map
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Default message
        self.canvas.create_text(width / 2, height / 2, text="Loading map...", font=("Arial", 14))

        # Refresh map
        self.update_map()

    def update_map(self):
        if not self.api_key:
            self.canvas.delete("all")
            self.canvas.create_text(self.width / 2, self.height / 2,
                                    text="Google Maps API key not found",
                                    font=("Arial", 14), fill="red")
            return

        # Construct Google Static Maps API URL
        url = "https://maps.googleapis.com/maps/api/staticmap"

        # Add center parameter
        params = {
            "center": f"{self.latitude},{self.longitude}",
            "zoom": self.zoom,
            "size": f"{self.width}x{self.height}",
            "scale": 1,
            "maptype": "roadmap",
            "key": self.api_key
        }

        # Add markers
        markers_param = ""
        for marker in self.markers:
            markers_param += f"&markers=color:red|label:|{marker['lat']},{marker['lng']}"

        # Construct URL with parameters
        request_url = url + "?" + "&".join([f"{k}={v}" for k, v in params.items()]) + markers_param

        try:
            # Download the map image
            with urllib.request.urlopen(request_url) as response:
                data = response.read()

            # Create a PIL Image
            image = Image.open(io.BytesIO(data))

            # Convert to PhotoImage
            self.map_image = ImageTk.PhotoImage(image)

            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.map_image)
        except Exception as e:
            self.canvas.delete("all")
            self.canvas.create_text(self.width / 2, self.height / 2,
                                    text=f"Error loading map: {str(e)}",
                                    font=("Arial", 12), fill="red")

    def set_position(self, lat, lng):
        self.latitude = lat
        self.longitude = lng
        self.update_map()

    def set_zoom(self, zoom):
        self.zoom = zoom
        self.update_map()

    def set_marker(self, lat, lng, text=None):
        marker = {"lat": lat, "lng": lng, "text": text}
        self.markers.append(marker)
        self.update_map()

    def delete_all_marker(self):
        self.markers = []
        self.update_map()




class HomePage(Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self,user_email):
        super().__init__()
        self.geometry("1280x720")
        self.configure(bg="#000000")
        self.image_references = []  # To store image references and prevent garbage collection
        self.user_email = user_email
        self.user_type = "passenger"
        self.api_key = "AIzaSyDCZYDh2wDMslhEdFFDQp2ctXqTJ8MehjM"
        self.setup_ui()


    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def launch_poolify_bot(self):
        """
        Opens the PoolifyBotApp from a home page button

        Parameters:
        root (tk.Tk): The current Tkinter root window that needs to be closed
        user_email (str): The email of the current user
        """
        # Close the current window
        self.destroy()

        # Import the PoolifyBotApp if not already imported
        import os
        import sys
        # Add the parent directory to sys.path if needed to ensure imports work
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        # Import the module (make sure the import path is correct)
        import PoolifyBot  # adjust this import path if needed

        # Create and run the PoolifyBotApp with both user_email and user_type
        bot_app = PoolifyBot.PoolifyBotApp(self.user_email, self.user_type)
        bot_app.mainloop()


    def poolify(self):
        self.destroy()  # Destroys the current window or frame
        WelcomePage.WelcomePage()

    # def cpp(self):
    #     self.destroy()
    #     ChangePasswordPage.ChangePasswordPage(self.user_email)

    def profile(self):
        self.destroy()
        profile_app = PassengerProfile.PassengerProfileApp(self.user_email)
        profile_app.mainloop()

    def createride(self):
        self.destroy()
        CreateRide.CreateRidePage(self.user_email)

    def searchride(self, city1, city2):
        # Close the current window first
        self.destroy()

        # Create the SearchRide window and pass the user email
        sr_window = SearchRide.RideBookingApp(self.user_email)

        # Clear existing entries
        sr_window.entry_1.delete(0, tk.END)
        sr_window.entry_2.delete(0, tk.END)

        # Insert cities into the entry fields
        sr_window.entry_1.insert(0, city1)
        sr_window.entry_2.insert(0, city2)

        # Start the mainloop for the new window
        sr_window.mainloop()

    def searchlive(self):
        self.destroy()  # Destroys the current window

        # First, check if we have a current location
        if not hasattr(self, 'current_lat') or not hasattr(self, 'current_lng'):
            messagebox.showerror("Location Error", "Please share your location first!")
            return

        # Use a geocoding service to get the city from coordinates
        try:
            import requests

            # Use Google Geocoding API to get the city
            geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={self.current_lat},{self.current_lng}&key={self.api_key}"

            response = requests.get(geocoding_url)
            data = response.json()

            if data['status'] == 'OK':
                # Extract the city from the results
                for component in data['results'][0]['address_components']:
                    if 'locality' in component['types'] or 'administrative_area_level_1' in component['types']:
                        current_city = component['long_name']
                        break
                else:
                    # Fallback if no specific city found
                    current_city = "Unknown"
            else:
                current_city = "Unknown"

            # Create the SearchRide window and pass the user email
            sr_window = SearchRide.RideBookingApp(self.user_email)

            # Clear existing entries
            sr_window.entry_1.delete(0, tk.END)
            sr_window.entry_2.delete(0, tk.END)

            # Insert current city into the first entry field
            sr_window.entry_1.insert(0, current_city)

            # Start the mainloop for the new window
            sr_window.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Could not determine city: {str(e)}")

    def settings(self):
        self.destroy()
        SettingsPage.AppBase(self.user_email,self.user_type)

    def walletpage(self):
        self.destroy()  # Destroys the current window or frame
        wallet_page = WalletPage.WalletApp(self.user_email, self.user_type)
        wallet_page.mainloop()

    def chatbot(self):
        self.destroy()

    def get_location(self):
        if not self.api_key:
            messagebox.showerror("API Key Error", "Google Maps API key not set.")
            return

        # Create a simple HTML file to get location with Google Maps API
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Get Location</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                button {{ padding: 10px 20px; background-color: #3498db; color: white; border: none; cursor: pointer; }}
                #status {{ margin-top: 20px; }}
                #map {{ height: 300px; width: 100%; margin-top: 20px; display: none; }}
            </style>
            <script src="https://maps.googleapis.com/maps/api/js?key={self.api_key}&callback=initMap" async defer></script>
            <script>
                let map;
                let marker;

                function initMap() {{
                    map = new google.maps.Map(document.getElementById('map'), {{
                        center: {{ lat: 40.6302, lng: -74.0252 }},
                        zoom: 12
                    }});
                }}

                function showMap(lat, lng) {{
                    document.getElementById('map').style.display = 'block';
                    map.setCenter({{ lat: lat, lng: lng }});

                    if (marker) {{
                        marker.setMap(null);
                    }}

                    marker = new google.maps.Marker({{
                        position: {{ lat: lat, lng: lng }},
                        map: map,
                        title: 'Your location'
                    }});
                }}

                document.addEventListener('DOMContentLoaded', function() {{
                    document.getElementById('getLocation').addEventListener('click', function() {{
                        var status = document.getElementById('status');
                        status.textContent = 'Requesting location...';

                        if (navigator.geolocation) {{
                            navigator.geolocation.getCurrentPosition(function(position) {{
                                var lat = position.coords.latitude;
                                var lng = position.coords.longitude;
                                status.textContent = 'Location found! Lat: ' + lat + ', Lng: ' + lng;

                                // Save to localStorage for the app to read
                                localStorage.setItem('mapLat', lat);
                                localStorage.setItem('mapLng', lng);

                                // Show location on map
                                showMap(lat, lng);

                                // Show success message
                                status.innerHTML = 'Location shared successfully! <br>You can now close this window and return to the app.';
                                status.style.color = 'green';

                                // Send location back to the app using a file
                                fetch('http://localhost:8000/set_location?lat=' + lat + '&lng=' + lng)
                                    .then(response => response.text())
                                    .then(data => console.log(data))
                                    .catch(error => console.error('Error:', error));
                            }}, function(error) {{
                                status.textContent = 'Error: ' + error.message;
                                status.style.color = 'red';
                            }}, {{
                                enableHighAccuracy: true,
                                timeout: 5000,
                                maximumAge: 0
                            }});
                        }} else {{
                            status.textContent = 'Geolocation is not supported by this browser.';
                            status.style.color = 'red';
                        }}
                    }});
                }});
            </script>
        </head>
        <body>
            <h1>Map Location Access</h1>
            <p>Click the button below to share your location with the app:</p>
            <button id="getLocation">Share My Location</button>
            <div id="status"></div>
            <div id="map"></div>
        </body>
        </html>
        """

        # Write the HTML file
        with open("get_location.html", "w") as f:
            f.write(html_content)

        # Start a simple HTTP server to receive location updates
        import http.server
        import socketserver
        import urllib.parse

        class LocationHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith('/set_location'):
                    parsed_url = urllib.parse.urlparse(self.path)
                    params = urllib.parse.parse_qs(parsed_url.query)

                    try:
                        lat = float(params.get('lat', ['0'])[0])
                        lng = float(params.get('lng', ['0'])[0])

                        # Write to a file that the main app can read
                        with open("location_data.json", "w") as f:
                            json.dump({"lat": lat, "lng": lng}, f)

                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(b"Location received")
                    except Exception as e:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/plain')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(f"Error: {str(e)}".encode())
                else:
                    super().do_GET()

        def run_server():
            with socketserver.TCPServer(("", 8000), LocationHandler) as httpd:
                print("Serving at port 8000")
                httpd.serve_forever()

        # Start server in a separate thread
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

        # Open the HTML file in the browser
        webbrowser.open('http://localhost:8000/get_location.html')

        # Check for location data updates periodically
        self.check_location_updates()

        messagebox.showinfo("Location Request",
                            "Please share your location in the browser window that opened. The app will update with your location shortly.")

    def check_location_updates(self):
        try:
            # Use os.path.exists with additional error handling
            if os.path.exists("location_data.json"):
                # Use a try-except block with file handling
                try:
                    # Open the file with minimal locking attempts
                    with open("location_data.json", "r") as f:
                        try:
                            # Read the file contents
                            data = json.load(f)
                        except json.JSONDecodeError:
                            print("Invalid JSON in location_data.json")
                            # Schedule another check and exit
                            self.after(1000, self.check_location_updates)
                            return

                    lat = data.get("lat")
                    lng = data.get("lng")

                    if lat and lng:
                        # Update our location
                        self.current_lat = lat
                        self.current_lng = lng

                        # Update the UI
                        self.update_location_ui()

                        # Attempt to remove the file safely
                        try:
                            os.remove("location_data.json")
                        except PermissionError:
                            print("Could not remove location_data.json. File may be in use.")
                        except Exception as remove_error:
                            print(f"Error removing location_data.json: {remove_error}")

                        # Return here to stop the recurring check since we got the data
                        return

                except PermissionError:
                    print("Permission denied accessing location_data.json")
                except IOError as e:
                    print(f"IO Error reading location_data.json: {e}")

        except Exception as e:
            print(f"Unexpected error checking location updates: {e}")

        # Schedule another check after 1 second
        try:
            self.after(1000, self.check_location_updates)
        except tk.TclError:
            # This can happen if the window is destroyed
            print("Location update check stopped")

    def update_location_ui(self):
        if hasattr(self, 'current_lat') and hasattr(self, 'current_lng') and self.current_lat and self.current_lng:
            # Update location label if it exists
            if hasattr(self, 'location_label'):
                self.location_label.config(text=f"Current Location: {self.current_lat:.6f}, {self.current_lng:.6f}")
            else:
                # Create location label if it doesn't exist
                self.location_label = tk.Label(
                    self,
                    text=f"Current Location: {self.current_lat:.6f}, {self.current_lng:.6f}",
                    bg="white",
                    font=("Arial", 10)
                )
                self.location_label.place(x=10, y=640)

            # Clear existing markers
            self.map_widget.delete_all_marker()

            # Add new marker
            self.map_widget.set_marker(self.current_lat, self.current_lng)

            # Center the map on the new location
            self.map_widget.set_position(self.current_lat, self.current_lng)

            # Set appropriate zoom level
            self.map_widget.set_zoom(15)

            print(f"Map updated with location: {self.current_lat}, {self.current_lng}")



    def setup_ui(self):
        # Create the main canvas
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Static Elements
        self.canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        self.canvas.create_text(15, 9, anchor="nw", text="POOLIFY", fill="#FFFFFF", font=("Italiana Regular", -36))

        self.map_widget = GoogleMapWidget(
            self,
            width=650,
            height=620,  # Keep the original height
            initial_location=(40.6302, -74.0252),  # Bay Ridge area
            zoom=13,
            api_key=self.api_key
        )
        self.map_widget.place(x=10,y=70)

        # Current location storage
        self.current_lat = None
        self.current_lng = None

        self.share_location_button = tk.Button(self, text="Share My Location", font=("Arial", 10, "bold"),
                                                                                       bg="#2ecc71", fg="white", padx=10, pady=5, command=self.get_location)
        self.share_location_button.place(x=700, y=200)

        self.share_location_button = tk.Button(self, text="Search for Rides", font=("Arial", 10, "bold"),
                                               bg="#2ecc71", fg="white", padx=10, pady=5, command=self.searchlive)
        self.share_location_button.place(x=700, y=400)

        # Profile image button
        profile_img = PhotoImage(file=self.relative_to_assets("ProfileTry.png"))
        self.image_references.append(profile_img)  # Keep a reference

        self.profile_button = Button(
            self,
            image=profile_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            fg="#FFFFFF",
            bg="#000000",
            cursor="hand2",
            command=self.toggle_button
        )
        self.profile_button.place(x=1230, y=5, width=50, height=50)

        button_data = [
            ("MumPune.png", 80.0, "Mumbai", "Pune"),
            ("BanNas.png", 300.0, "Bangalore", "Nashik"),
            ("DelJai.png", 520.0, "Delhi", "Jaipur")
        ]

        buttons = []

        for index, (image_file, y_pos, city1, city2) in enumerate(button_data, start=1):
            button_image = PhotoImage(file=self.relative_to_assets(image_file))

            # Create a lambda function that captures specific city values
            cmd = lambda c1=city1, c2=city2: self.searchride(c1, c2)

            button = Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=cmd,
                relief="flat"
            )
            button.image = button_image  # Keep a reference to avoid garbage collection
            button.place(x=920, y=y_pos, width=324.0, height=162.0)
            buttons.append(button)

    def display_profile_data(self):
        """Fetch and display the user profile data inside menu_frame."""
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root",
                                                 database="carpooling_db")
            cursor = connection.cursor(dictionary=True)
            query = "SELECT name, email, profile_image FROM users WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            user_data = cursor.fetchone()

            # Explicitly consume any remaining results
            while cursor.nextset():
                pass

            cursor.close()
            cursor = None  # Set to None so we don't try to close it again in finally

            if not user_data:
                return  # No user found, skip UI update

            u_name = user_data["name"]
            u_email = user_data["email"]
            u_profile_binary = user_data["profile_image"]  # Binary image data

            # Display user details
            name_label = Label(
                self.menu_frame,
                text=f"Name: {u_name}",
                bg="white",
                font=("Poppins Medium", 12)
            )
            name_label.place(x=15, y=150)

            email_label = Label(
                self.menu_frame,
                text=f"Email: {u_email}",
                bg="white",
                font=("Poppins Medium", 12)
            )
            email_label.place(x=15, y=185)

            # Initialize image_references if it doesn't exist
            if not hasattr(self, 'image_references'):
                self.image_references = []

            # Check if user has a profile image
            if u_profile_binary:
                try:
                    from PIL import Image, ImageTk
                    import io

                    # Convert binary data to image
                    image_stream = io.BytesIO(u_profile_binary)
                    pil_image = Image.open(image_stream)

                    # Resize if needed
                    pil_image = pil_image.resize((80, 80))  # Adjust size as needed

                    # Convert PIL image to Tkinter PhotoImage
                    tk_image = ImageTk.PhotoImage(pil_image)

                    # Keep a reference to prevent garbage collection
                    self.image_references.append(tk_image)

                    # Display the image
                    profile_label = Label(
                        self.menu_frame,
                        image=tk_image,
                        bg="#FFFFFF"
                    )
                    profile_label.place(x=20.0, y=60.0)

                except Exception as e:
                    print(f"Error processing profile image: {e}")
                    self.display_default_profile()
            else:
                self.display_default_profile()

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            self.display_default_profile()
        except Exception as main_error:
            print(f"Error in user profile display: {main_error}")
            self.display_default_profile()
        finally:
            # Always close cursor and connection in finally block
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

            if connection:
                try:
                    # Force close connection without checking is_connected
                    connection.close()
                except:
                    pass

    def display_default_profile(self):
        """Display default profile image as fallback."""
        try:
            default_img = PhotoImage(file=self.relative_to_assets("ProfileImage.png"))
            self.image_references.append(default_img)
            profile_label = Label(
                self.menu_frame,
                image=default_img,
                bg="#FFFFFF"
            )
            profile_label.place(x=20.0, y=60.0)
        except Exception:
            # Last resort if even default image fails
            profile_label = Label(
                self.menu_frame,
                text="[Profile]",
                bg="white",
                font=("Poppins Medium", 12)
            )
            profile_label.place(x=20.0, y=60.0)
            print(f"Unexpected error: {e}")

    def toggle_button(self):
        def close_button():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

        self.profile_button.place_forget()

        # Create menu frame
        self.menu_frame = Frame(self, bg="white", width=550, height=638, bd=2, relief="solid", highlightbackground="black",
                               highlightcolor="black")
        self.menu_frame.place(x=1040, y=60)

        # Profile image in menu
        # profile_img_label = PhotoImage(file=self.relative_to_assets("ProfileImage.png"))
        # self.image_references.append(profile_img_label)
        # profile_label = Label(
        #     self.menu_frame,
        #     image=profile_img_label,
        #     bg="#FFFFFF"
        # )
        # profile_label.place(x=20.0, y=60.0)
        # Button details: (image file, x, y, width, command)
        buttons = [
            ("BackButton.png", 0, 15, 105, close_button),
            ("ProfileHome.png", 0, 243, 105, self.profile),
            ("WalletIcon.png", 0, 303, 105, self.walletpage),
            # ("RideHistory.png", 0, 363, 150, self.history_button),
            ("SettingsButton.png", 0, 363, 120, self.settings),
            ("HelpButton.png", 0, 423, 180, self.launch_poolify_bot),
            ("LogOut.png", 0, 483, 105, self.poolify)
        ]

        # Create buttons dynamically
        for img_file, x, y, width, cmd in buttons:
            button_img = PhotoImage(file=self.relative_to_assets(img_file))

            btn = Button(
                self.menu_frame,
                image=button_img,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                bg="#FFFFFF",
                cursor="hand2",
                command=cmd
            )
            btn.place(x=x, y=y, width=width)

            self.image_references.append(button_img)  # Prevent garbage collection

            separator_positions = [220, 280, 340, 400, 460, 520, 580]

            # Create 8 separator lines
            for sep_y in separator_positions:
                Label(self.menu_frame, bg="#D9D9D9").place(x=0, y=sep_y, width=294, height=1)

        self.display_profile_data()


    def history_button(self):
        self.destroy()
        HistoryPage.HistoryPage(self.user_email)



if __name__ == "__main__":
    user_email = "nikhilanumallagpt@gmail.com"
    app = HomePage(user_email)
    app.resizable(False, False)
    app.mainloop()
