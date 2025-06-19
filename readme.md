# 🌦️ Weather App

A **simple desktop weather application** built with **Python** and **PyQt5**, using the **OpenWeatherMap API** to fetch live weather updates for any city in the world.

---

## 🚀 Features

- Enter any city and instantly get:
  - Current temperature (°C / °F)
  - Weather condition (with emoji 🌤️❄️🌪️ etc.)
  - Description of the weather (e.g., "light rain", "clear sky")
- Beautiful and clean interface
- Error handling for invalid inputs, wrong API keys, or server issues

---


## 🛠️ Setup Instructions

1. Clone the Repository


2. Install the required packages from requirements.txt using:

    pip install -r requirements.txt


3. Get your OpenWeatherMap API key as:

    Go to https://home.openweathermap.org/users/sign_up

    Sign up (or log in if you already have an account)

    Navigate to API keys 

    You will already have a key generated and if you dont see, generate one and make sure that it is active through the active button given there


4. Setup your environment variables as:

    Create a .env file in the project root directory (this file is already ignored by .gitignore)

    Add your API key like this:

    api_key = YOUR_API_KEY_HERE


5. Run the app using "python main.py"



