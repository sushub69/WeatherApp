import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,QLineEdit,
                             QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_name = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self) # alt + 0176 for degree symbol 
        self.image_label = QLabel(self)
        self.description_label = QLabel(self)
        self.resize(550,750)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App by Sushav")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_name)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_name.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_name.setObjectName("city_name")
        self.city_input.setObjectName("city_input")
        self.weather_button.setObjectName("weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.image_label.setObjectName("image_label")
        self.description_label.setObjectName("description_label")
        

        self.setStyleSheet("""
            QLabel, QPushButton, QLineEdit{
                font-family: Segoe UI;
            }
            QLabel#city_name{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
                padding: 8px;
                border: 2px solid #0b95fb;
                border-radius: 12px;
            }
            QPushButton#weather_button{
                font-size: 30px;
                font-weight: bold;
                padding: 8px;
                border-radius: 12px;
                background-color: #0b95fb;
                color: white;
            }
            QPushButton#weather_button:hover {
                background-color: #1976d2;
            }
            QLabel#temperature_label{
                font-size: 72px;
                font-weight: bold;
                padding: 8px;
            }
            QLabel#image_label{          
            }
            QLabel#description_label{
                font-size: 55px;
            }
        """)

        self.weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api_key = "1e46a7ffc31318b88253e57acb76569a"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status() # Need to typed manually to catch erros
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request: \nPlease check your input")
                case 401:
                    self.display_error("Unauthorized: \nInvalid API key")
                case 403:
                    self.display_error("Forbidden: \nAcces is not allowed")
                case 404:
                    self.display_error("Not found: \nCity was not found")
                case 500:
                    self.display_error("Internal Server Error: \nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway: \nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable: \nServer is currently down")
                case 504:
                    self.display_error("Gateway Timeout: \nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request took too long")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.image_label.clear()
        self.description_label.clear()


    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size:60px;")
        self.description_label.setStyleSheet("font-size: 55px;")
        
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        # print(f"{temp_c:.2f}°C")
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        # print(weather_description)
        
        self.temperature_label.setText(f"{temp_c:.0f}°C")
        self.weather_image(weather_id)
        self.description_label.setText((weather_description).capitalize())

    def weather_image(self, weather_id):

        if 200 <= weather_id <= 232:
            image_path = "Weather_Images/thunderstorm.jpg"

        elif 300 <= weather_id <= 321:
            image_path = "Weather_Images/drizzle.jpg"

        elif 500 <= weather_id <= 531:
            image_path = "Weather_Images/heavyrain.jpg"

        elif 600 <= weather_id <= 622:
            image_path = "Weather_Images/snowing.jpg"

        elif 701 <= weather_id <= 741:
            image_path = "Weather_Images/mist.jpg"

        elif 751 <= weather_id <= 761:
            image_path = "Weather_Images/dusty.jpg"

        elif weather_id == 762:
            image_path = "Weather_Images/volcanicash.jpg"

        elif weather_id == 771:
            image_path = "Weather_Images/squall.jpg"

        elif weather_id == 781:
            image_path = "Weather_Images/tornado.jpg"

        elif weather_id == 800:
            image_path = "Weather_Images/clear.jpg"

        elif 801 <= weather_id <= 804:
            image_path = "Weather_Images/cloudy.jpg"

        else:
            image_path = ""

        pixmap = QPixmap(image_path)

        pixmap = pixmap.scaled(500,500, # Resize image while keeping its aspect ratio
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation)

        self.image_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())