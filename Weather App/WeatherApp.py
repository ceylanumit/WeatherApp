from tkinter import *
from PIL import ImageTk, Image
import requests

weather_api_url = "http://api.openweathermap.org/data/2.5/weather"
api_key = "0d8ff83f33fe4eb2009f55a93b956c31"
icon_base_url = "https://openweathermap.org/img/wn/{}@2x.png"

def get_weather(city):
    params = {"q": city, "appid": api_key}
    data = requests.get(weather_api_url, params=params).json()
    if data:
        city_name = data.get("name", "").capitalize()
        country_code = data.get("sys", {}).get("country", "")
        temperature = int(data.get("main", {}).get("temp", 0) - 273.15)
        weather_icon = data.get("weather", [{}])[0].get("icon", "")
        weather_description = data.get("weather", [{}])[0].get("description", "")
        return (city_name, country_code, temperature, weather_icon, weather_description)

def update_weather_info():
    city = city_entry.get()
    weather_info = get_weather(city)
    if weather_info:
        location_label["text"] = "{},{}".format(weather_info[0], weather_info[1])
        temperature_label["text"] = "{}°C".format(weather_info[2])
        weather_condition_label["text"] = weather_info[4]
        weather_icon = ImageTk.PhotoImage(Image.open(requests.get(icon_base_url.format(weather_info[3]), stream=True).raw))
        weather_icon_label.configure(image=weather_icon)
        weather_icon_label.image = weather_icon

app = Tk()
app.geometry("350x450")
app.title("Weather App")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_coordinate = int((screen_width/2) - (350/2))
y_coordinate = int((screen_height/2) - (500/2))

app.geometry(f"350x450+{x_coordinate}+{y_coordinate}")

city_entry = Entry(app, justify="center")
city_entry.pack(fill=BOTH, ipady=10, padx=18, pady=5)
city_entry.focus()

search_button = Button(app, text="Search", font=("Arial", 10), command=update_weather_info)
search_button.pack(fill=BOTH, ipady=5, padx=18, pady=(0, 10))

weather_icon_label = Label(app)
weather_icon_label.pack()

location_label = Label(app, font=("Arial", 30))
location_label.pack()

temperature_label = Label(app, font=("Arial", 40, "bold"))
temperature_label.pack()

weather_condition_label = Label(app, font=("Arial", 15))
weather_condition_label.pack()

app.mainloop()
