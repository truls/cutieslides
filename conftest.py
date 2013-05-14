from config import Config
import time

conf = Config("/home/truls/uni/kantine/slideshow/slides.yml")

try:
    for el in conf.slidesgen():
        print(el)
        time.sleep(.1)
except KeyboardInterrupt:
    conf.end()
