from pyowm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'

place = "Липецк"
owm = OWM('69177191d47d70a85bfce033c260b888', config_dict)
mgr = owm.weather_manager()
observation = mgr.weather_at_place(place)
w = observation.weather

t = w.temperature("celsius")
t1 = t['temp']
dt = w.detailed_status

print(t1)
print(dt)
