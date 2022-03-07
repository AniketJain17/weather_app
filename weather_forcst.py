# Import modules
import tkinter,pytz,requests
from tkinter import *
from tkinter import messagebox,BOTH
from io import BytesIO
from PIL import ImageTk, Image


software_version = 'alpha version'
IST = pytz.timezone('Asia/Kolkata')

#Define fonts and colors
large_font = ('Engravers MT', 17)
lrge_font = ('Avenir Next LT Pro', 14)
small_font = ('Bahnschrift Condensed', 15)
top_left_frame_bg  = "#ff4f00"
top_right_frame_bg = "#ff4f00"
quote = ('Harlow Solid Italic',18)

# Dfine Window
app= tkinter.Tk()
app.geometry("700x560+400+200")
app.iconbitmap("image_main\weather.ico")
app.title(f"{software_version}")
app.resizable(True, True)
app.config(background = 'yellow')


#Define functions
def search():
    """Use open ewather api to look up current weather conditions given a city/ city, country"""
    global response

    #Get API response
    #URL and my api key....USE YOUR OWN API KEY!
    url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = 'c39c3d4158714d582f23b5e802f964bc' #USE YOUR OWN API KEY

    #Search by the appropriate query, either city name or zip
    if search_method.get() == 1:
        querystring = {"q":city_entry.get(), 'appid':api_key, 'units':'imperial'}
    elif search_method.get() == 2:
        querystring = {"zip":city_entry.get(), 'appid':api_key, 'units':'imperial'}

    #Call API
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    #Example response return
    #print(response)
    '''
    {
    'coord': {'lon': 80.2785, 'lat': 13.0878}, 
    'weather': [{'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '150n'}], 
    'base': 'stations', 
    'main': {'temp': 77, 'feels_like': 82.78, 'temp_min': 77, 'temp_max': 77, 'pressure': 1013, 'humidity': 83},
    'visibility': 5000, 
    'wind': {'speed': 4.61, 'deg': 70},
    'clouds': {'all': 40}, 'dt': 1613942687,
    'sys': {'type': 1, 'id': 9218, 'country': 'IN', 'sunrise': 1613955522, 'sunset': 1613997987}, 
    'timezone': 19800, 
    'id': 1264527, 
    'name': 'Chennai', 
    'cod': 200
    }
    '''
    get_weather()
    get_icon()


def get_weather():
    """Grab information from API response and update our weather labels."""
    #Gather the data to be used from the API response
    if response['cod'] == 200:
        city_name = response['name']
        country_code = str(response['sys']['country'])
        city_lat = str(response['coord']['lat'])
        city_lon = str(response['coord']['lon'])

        main_weather = response['weather'][0]['main']
        description = response['weather'][0]['description']

        temp = str(response['main']['temp'])
        feels_like = str(response['main']['feels_like'])
        temp_min = str(response['main']['temp_min'])
        temp_max = str(response['main']['temp_max'])
        humidity = str(response['main']['humidity'])
    else:
        if search_method.get() == 1:
            city_name = 'Try Zipcode'
        else:
            city_name = 'Try City,CountryCode'
        country_code,city_lat, city_lon, main_weather, description, temp, feels_like, temp_min, temp_max, humidity = '','','','','','','','','',''

    #Update output lables
    city_info_label.config(text=city_name + "," + country_code + " (" + city_lat + ", " + city_lon + ")")
    weather_label.config(text="Weather: " + main_weather + ", " + description)
    temp_label.config(text='Temperature: ' + temp + " F")
    feels_label.config(text="Feels Like: " + feels_like + " F")
    temp_min_label.config(text="Min Temperature: " + temp_min + " F")
    temp_max_label.config(text="Max Temperature: " + temp_max + " F")
    humidity_label.config(text="Humidity: " + humidity)
        

def get_icon():
    """Get the appropriate weather icon from API response"""
    global img

    #Get the icon id from API response.
    icon_id = response['weather'][0]['icon']

    #Get the icon from the correct webiste
    url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)

    #Make a request at the url to download the icon; stream=True automatically dl
    icon_response = requests.get(url, stream=True)

    #Turn into a form tkinter/python can use
    img_data = icon_response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    #Update label
    photo_label.config(image=img)

#---------------------------
# Frame details
#---------------------------

frame1 = Frame(app, height = 100, width=180, bg= top_left_frame_bg, bd=1, relief = FLAT)
frame1.place(x=0,y=0)
frame2 = Frame(app, height = 170, width=800, bg= top_left_frame_bg, bd=1, relief = FLAT)
frame2.place(x=0,y=0)
frame3 = Frame(app, height = 200, width=500, bg= 'yellow', bd=0, relief = FLAT)
frame3.place(x=180,y=240)


#---------------------------
#Output frame layout
#---------------------------
city_info_label = Label(frame3, font=large_font,bg="yellow")
city_info_label.place(x=60)
weather_label =Label(frame3, font=small_font,bg="yellow")
temp_label =Label(frame3, font=small_font,bg="yellow")
feels_label =Label(frame3, font=small_font,bg="yellow")
temp_min_label =Label(frame3, font=small_font,bg="yellow")
temp_max_label =Label(frame3, font=small_font,bg="yellow")
humidity_label =Label(frame3, font=small_font,bg="yellow")
photo_label =Label(frame3,bg="yellow")

city_info_label.pack()
weather_label.pack()
temp_label.pack()
feels_label.pack()
temp_min_label.pack()
temp_max_label.pack()
humidity_label.pack()
photo_label.pack()

#LOGO
logo_image = PhotoImage(file= "image_main\logo.png")
logo_btn = Button(app, image=logo_image, bg= top_right_frame_bg, relief = FLAT)
logo_btn.place(x = 25,y = 29)


#---------------------------
#labels
#---------------------------

label_location = Label(text="Climate is what we expect, weather is what we get. ", bg = top_left_frame_bg, font = quote)
label_location.place(x=190, y=29)
label_location = Label(text="Enter Your Location", bg = top_right_frame_bg, font = 'Verdana 11')
label_location.place(x=276, y=84)
label_location = Label(text="FORECASTED WEATHER :", bg="yellow",font = 'Algerian 15')
label_location.place(x=225, y=180)

city_entry =Entry(frame2, width=20,bd=2, font=lrge_font ,bg = top_left_frame_bg)
city_entry.place(x=250, y=110)

submit_button = Button(frame2,text="Search", command=search,bd=3 ,bg = top_left_frame_bg)
submit_button.place(x=440,y=110)

search_method = IntVar()
search_method.set(1)


app.mainloop()