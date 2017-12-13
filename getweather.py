import json
import httplib2


weather_api_key = 'ce652ce44d3df1fd5yv66610bd929815bdb95'


def get_weather(city, country):
    url = ('http://api.openweathermap.org/data/2.5/forecast?q={},{}&APPID={}&units=metric'.format(city, country, weather_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    if result['city']['id']:
        city_name = result['city']['name']
        country_name = result['city']['country']
        temperature = result['list'][0]['main']['temp']
        date = result['list'][0]['dt_txt']
        description = result['list'][0]['weather'][0]['description']
        city_info = {'city': city_name, 'country': country_name, 'date': date, 'temperature': temperature, 'description': description}
        return city_info
    else:
        return "No City Found!"


if __name__ == '__main__':
    get_weather("Bangalore", "IN")
    get_weather("Delhi", "IN")
    get_weather("Mumbai", "IN")
    get_weather("Bhopal", "IN")
    get_weather("Kolkata", "IN")
