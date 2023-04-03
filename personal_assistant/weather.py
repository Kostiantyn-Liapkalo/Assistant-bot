import requests
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.validation import Validator
from prompt_toolkit.styles import Style
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER 
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


cities_completer = WordCompleter(["Kabul", "Tirana", "Algiers", "Andorra la Vella", "Luanda", "Saint John's", "Buenos Aires", 
                                  "Yerevan", "Canberra", "Vienna", "Baku", "Nassau", "Manama", "Dhaka", "Bridgetown", "Minsk", "Brussels", 
                                  "Belmopan", "Porto Novo", "Thimphu", "La Paz ", "Sarajevo", "Gaborone", "Brasilia", "Bandar Seri Begawan", 
                                  "Sofia", "Ouagadougou", "Gitega", "Phnom Penh", "Yaounde", "Ottawa", "Praia", "Bangui", "N'Djamena", "Santiago", 
                                  "Beijing", "Bogota", "Moroni", "Kinshasa", "Brazzaville", "San Jose", "Yamoussoukro", "Zagreb", "Havana", "Nicosia", 
                                  "Prague", "Copenhagen", "Djibouti", "Roseau", "Santo Domingo", "Dili", "Quito", "Cairo", "San Salvador", "London", "Malabo", 
                                  "Asmara", "Tallinn", "Mbabana", "Addis Ababa", "Palikir", "Suva", "Helsinki", "Paris", "Libreville", "Banjul", "Tbilisi", 
                                  "Berlin", "Accra", "Athens", "Saint George's", "Guatemala City", "Conakry", "Bissau", "Georgetown", "Port au Prince", 
                                  "Tegucigalpa", "Budapest", "Reykjavik", "New Delhi", "Jakarta", "Tehran", "Baghdad", "Dublin", "Rome", "Kingston", 
                                  "Tokyo", "Amman", "Astana", "Nairobi", "Tarawa Atoll", "Pristina", "Kuwait City", "Bishkek", "Vientiane", "Riga", 
                                  "Beirut", "Maseru", "Monrovia", "Tripoli", "Vaduz", "Vilnius", "Luxembourg", "Antananarivo", "Lilongwe", "Kuala Lumpur", 
                                  "Male", "Bamako", "Valletta", "Majuro", "Nouakchott", "Port Louis", "Mexico City", "Chisinau", "Monaco", "Ulaanbaatar", 
                                  "Podgorica", "Rabat", "Maputo", "Nay Pyi Taw", "Windhoek", "Kathmandu", "Amsterdam", "Wellington", "Managua", 
                                  "Niamey", "Abuja", "Pyongyang", "Skopje", "Belfast", "Oslo", "Muscat", "Islamabad", "Melekeok", "Jerusalem", "Panama City", 
                                  "Port Moresby", "Asuncion", "Lima", "Manila", "Warsaw", "Lisbon", "Doha", "Bucharest", "Moscow", "Kigali", "Basseterre", 
                                  "Castries", "Kingstown", "Apia", "San Marino", "Sao Tome", "Riyadh", "Edinburgh", "Dakar", "Belgrade", "Victoria", "Freetown", 
                                  "Singapore", "Bratislava", "Ljubljana", "Honiara", "Mogadishu", "Pretoria", "Seoul", "Juba", "Madrid", 
                                  "Sri Jayawardenapura Kotte", "Khartoum", "Paramaribo", "Stockholm", "Bern", "Damascus", "Taipei", 
                                  "Dushanbe", "Dodoma[23]", "Bangkok", "Lome", "Nuku'alofa", "Port of Spain", "Tunis", "Ankara", "Ashgabat", 
                                  "Funafuti", "Kampala", "Kyiv", "Abu Dhabi", "London", "Washington D.C.", "Montevideo", "Tashkent", "Port Vila", 
                                  "Vatican City", "Caracas", "Hanoi", "Cardiff", "Sana'a", "Lusaka", "Harare", "Dubai", "menu"], ignore_case=True)

# style = Style.from_dict({
#     'completion-menu.completion': 'bg:#0d2fc9 #ffffff',
#     'completion-menu.completion.current': 'bg:#f6fa0c #000000',
#     'scrollbar.background': 'bg:#88aaaa',
#     'scrollbar.button': 'bg:#222222',
# })

def weather(city = 'Kyiv'):
    city = city + "+weather"
    res = requests.get(
        f'https://www.google.com/search?q={city}&hl=en&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    if len(soup.select('#wob_dts')) == 0:
        return print("Wrong input. No such city found. Try again!")
    else:
        time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    temp = soup.select('#wob_tm')[0].getText().strip()
    humidity = soup.select('#wob_hm')[0].getText().strip()
    wind = soup.select('#wob_ws')[0].getText().strip()

    city = "Weather in " + city.replace("+weather", "").capitalize()
    temp = "Temperature: " + temp+" °C"
    info = "Info: " + info
    humidity = "Humidity: " + humidity
    wind = "Wind: " + wind
    data = [city, time, temp, info, humidity, wind]

    next_days =[]
  
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.findAll("div")[0].attrs['aria-label']
        # get weather status for that day
        weather = "Info: " + day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature 
        max_temp = "Max. temperature: " + temp[0].text + " °C"
        # minimum temparature
        min_temp = "Min. temperature: " + temp[2].text + " °C"
        next_days.append([day_name, weather, max_temp, min_temp])
    
    next_days_split = [next_days[1:4], next_days[4:len(next_days)-1]]

    format_weather(data, next_days_split)

def create_table(data):
    my_table =PrettyTable()
    for i in data:
        my_table.add_column(i[0], i[1:])
    my_table.set_style(SINGLE_BORDER)
    my_table.align = 'c'
    return my_table


def format_weather(data: list, next_days_split = None ):
    print(data[0])
    my_weather_table = PrettyTable()
    my_weather_table.add_column(data[1], data[2:])
    my_weather_table.set_style(SINGLE_BORDER)
    # my_weather_table.max_width = 200
    my_weather_table.align = 'c'
    print(my_weather_table)

    first_table = create_table(next_days_split[0])
    second_table = create_table(next_days_split[1])

    print(f"{first_table}\n{second_table}")
    print("\nReturn to main menu type 'menu'\n")


def is_text(text) -> str:
    return text.isalpha()

validator = Validator.from_callable(is_text,
    error_message='This input contains wrong characters!',
    move_cursor_to_end=True)


def main():
    session = PromptSession(completer=cities_completer)
    # with styling dropdown list
    # session = PromptSession(completer=cities_completer, style=style) 

    weather() # default Kyiv
    while True:
        try:
            city = session.prompt('(WEATHER) Enter city >>> ', validator=validator)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except IndexError:
            print("Wrong input. Try again starting from letter.")
        else:
            if city == "menu":
                break
            else:
                weather(city)
    # print('GoodBye!')

if __name__ == '__main__':
    main()