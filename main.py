# Imports

import os # Operating system
import sys  # importing system
import requests # it sends requests to the server
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                              QLineEdit, QPushButton, QVBoxLayout)

# Description of the modules imported from PyQt5:
# Class	            What it does
# QApplication:	    Starts the application, handles events (must be created once in every    PyQt app).
# QWidget:	        A basic window or container (the base for all UI).
# QLabel:	        Displays text or images in your window.
# QLineEdit:	    A text input field (user can type into it).
# QPushButton:	    A clickable button.
# QVBoxLayout:	    Arranges widgets vertically (one on top of another).

from PyQt5.QtCore import Qt # will let you build applications with windows, buttons,      menus, text fields, etc.

def configure():
    load_dotenv()
# Object Oriented Programming is used:
class WeatherApp(QWidget):

    # Defining self variables or attributes
    def __init__(self):

        super().__init__()
        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather Now!", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.InitUI()

    # Shows these variables on the User Interface
    def InitUI(self):

        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button, alignment = Qt.AlignCenter)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox) # Sets the layout by default

        # Aligns everything on the UI at the center
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Gives an object ID to every self variable
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Does some CSS formatting
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri; 
            }
                           
            QLabel#city_label{
                font-size: 40px;
            }
                           
            QLineEdit#city_input{
                font-size: 40px;               
            }
                           
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;               
            }
                           
            QLabel#temperature_label{
                font-size: 75px;               
            }
                           
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;               
            }
                           
            QLabel#description_label{
                font-size: 50px;               
            }
    """)
        
        # Will connect to the requests when the button is clicked just like an Event Listener
        self.get_weather_button.clicked.connect(self.get_weather)
        
    # Gets the weather and other details from the API    
    def get_weather(self):
        city = self.city_input.text() # Stores the city input given by the user inside this variable
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('api_key')}"

        # Does some trial and error based on specific responses from the server or from the connection
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\n Please check your input")

                case 401:
                    self.display_error("Unauthorized\n Invalid API key")

                case 403:
                    self.display_error("Forbidden\n Access Denied")

                case 404:
                    self.display_error("Not found\n City not found")

                case 500:
                    self.display_error("Internal Server Error\n Please try again later")

                case 502:
                    self.display_error("Bad gateway\n Invalid response from the server")

                case 503:
                    self.display_error("Service Unavailable\n Server is down")

                case 504:
                    self.display_error("Gateway Timeout\n No response from the server")

                case _:
                    self.display_error(f"HTTP error occured\n {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\n Check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\n The request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\n Check the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n {req_error}")

    # Displays the generated error message from the above function to the user
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear() # Cleares the emoji after the second request is made without refreshing
        self.description_label.clear() # Cleares the description after the second request is made without refreshing

    # Displays the current weather on the UI
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"] # Temperature is in kelvin by default
        temperature_c = temperature_k - 273.15 # Takes it in Celcius
        temperature_f = (temperature_k * 9/5) - 459.67 # Takes it in Fahrenheit
        weather_id = data["weather"][0]["id"] # Gets the weather id which will show about the current description of the weather in the emoji
        weather_description = data["weather"][0]["description"] # Gets the weather description which will show about the current description of the weather

        # Displays the weather
        self.temperature_label.setText(f"{temperature_c:.0f}°C / {temperature_f:.0f}°F")

        # Displayes the emoji 
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

        # Displays the description
        self.description_label.setText(weather_description)

    # It is a static method independent of a class which takes the id in numbers and displays the most relevant emoji for that specific weather condition. Different numbers show different weather conditions
    @staticmethod
    def get_weather_emoji(weather_id):
        
        if 200 <= weather_id <= 232:
            return "⛈️"
        
        elif 300 <= weather_id <= 321:
            return "🌦️"
        
        elif 500 <= weather_id <= 504:
            return "🌧️"
        
        elif weather_id == 511:
            return "🌨️"
        
        elif 520 <= weather_id <= 531:
            return "🌧️"
        
        elif 600 <= weather_id <= 602:
            return "🌨️"
        
        elif 611 <= weather_id <= 613:
            return "🌧️❄️"
        
        elif 615 <= weather_id <= 616:
            return "🌧️❄️"
        
        elif 620 <= weather_id <= 622:
            return "❄️"
        
        elif weather_id == 701:
            return "🌫️"
        
        elif weather_id == 711:
            return "🌫️"
        
        elif weather_id == 721:
            return "🌫️"

        elif weather_id == 731 or weather_id == 761:
            return "🌫️"

        elif weather_id == 741:
            return "🌫️"

        elif weather_id == 751:
            return "🏜️"

        elif weather_id == 762:
            return "🌋"

        elif weather_id == 771:
            return "💨"

        elif weather_id == 781:
            return "🌪️"

        elif weather_id == 800:
            return "☀️"

        elif weather_id == 801:
            return "🌤️"

        elif weather_id == 802:
            return "⛅"

        elif weather_id == 803:
            return "🌥️"

        elif weather_id == 804:
            return "☁️"

        elif 900 <= weather_id <= 902:
            return "🌪️"

        elif weather_id == 903:
            return "🧊"

        elif weather_id == 904:
            return "🔥"

        elif weather_id == 905 or (951 <= weather_id <= 956):
            return "💨"

        elif 957 <= weather_id <= 962:
            return "🌬️"

        else:
            return "❓"

# Runs the class by rechecking the name
if __name__ == "__main__":
    configure()
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())



