import re
import requests
from lewd_dl.options import Options
from .extractor import *
from lewd_dl.proccessors import *

class LewdDL():
    def __init__(self, options: Options):
        self.options = options
        self.video = None
        self.session = requests.Session()
        
        self.session.headers.update({"user-agent": self.options.ua})

    @staticmethod
    def main(options):
        ldl = LewdDL(options)
        ie = None
        
        if options.print_platforms:
            print("[info] Supported platforms:")
            for key in globals():
                if key.endswith("IE"):
                    print("  - " + globals()[key]._NAME)
                    
            exit(0)
        
        # Select Info Extractor
        for key in globals():
            if key.endswith("IE"):
                ie_class = globals()[key]
                m = re.match(ie_class._URL, options.url)
                if m:
                    ie = ie_class(ldl.session, options)
                    ie.video.id = m.group("id")
                    
        if ie == None:
            print("Error: no Info Extractor found for suplied video")
            exit(1)

        ie.extract()
        
        if options.list_resolutions:
            ie.list_resolutions()
            exit(0)
            
        ie.download()
        
        ffmpeg = FFMPEG(ie)
        ffmpeg.hsl_combine()
        