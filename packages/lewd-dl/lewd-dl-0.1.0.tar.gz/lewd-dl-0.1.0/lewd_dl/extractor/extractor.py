import os
from zlib import crc32
from abc import ABCMeta, abstractmethod
from requests import Session, exceptions

from lewd_dl.video import Video
from lewd_dl.options import Options
from lewd_dl.log import Logger
from lewd_dl.utils.resolutions import *

class Extractor(Logger):
    _URL = ""
    _NAME = ""
    
    def __init__(self, session: Session, options: Options):   
        super(Extractor, self).__init__()     
        self.session = session
        self.video = Video()
        self._options = options
        
        self.video.url = self._options.url
        self.video.resolutions = []
        self.task_id = ""
        self.cache_path = ""
        
    def _download_webpage(self, url):
        self.log_id("Downloading webpage")
        
        return self._http_get(url)
        
    def _http_get(self, url, raw=False):
        
        try:
            req = self.session.get(url)
        except exceptions.RequestException as e:
            print(f"Error :: RequestException()\n  " + url)
            if not self._options.ignore_errors: exit(1)
        else:
            if req.status_code != 200:
                self.info(f"Error :: HTTPError({req.status_code})\n  Url: {req.url}")
                if not self._options.ignore_errors: exit(1)
                
            content = req.content
            if not raw:
                content = content.decode("utf-8")
            req.close()
            
            return content
        
        return None
    
    @abstractmethod
    def download(self):
        self.report("Destination: {}".format(self._options.out), "download")
    
    @abstractmethod
    def extract(self):
        self.log_id("Extracting video information")
    
    def list_resolutions(self):
        self.report_info("Available resolutions for {}:".format(self.video.id))
        print("format code  resolution  aspect")
        for res in self.video.resolutions_tuples:
            print("{}  {}  {}".format("{}p".format(res[1]).ljust(11, " "),
                    "{}x{}".format(res[0], res[1]).ljust(10, " "),
                    calc_aspect(res[0], res[1])
                ))