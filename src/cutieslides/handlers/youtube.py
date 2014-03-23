
#from pytube import YouTube

cutieslides_handler = {'name': 'youtube',
                       'type': 'final',
                       'downloader': 'custom',
                       'domain': 'youtube.com',
                       'domain': 'Foo'}

class Handler:

    name = "youtube"
    type = 'final'
        
    domain = '^.*youtube.com$'
    path = '^\/watch$'
    
    downloader = 'default'
    priority = 0

    
    def get(r, properties):
        pass

    



