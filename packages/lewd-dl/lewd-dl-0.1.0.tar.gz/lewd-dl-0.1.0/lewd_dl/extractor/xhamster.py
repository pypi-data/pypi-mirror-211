import re
import json
import m3u8
from bs4 import BeautifulSoup
from .extractor import Extractor, crc32, os
from lewd_dl.downloader import HslDL

class XHamsterIE(Extractor):
    _URL = "^https?://(?:(?:[^/]+\.)?xhamster\.(?:com|desi)\/(?:videos\/))(?P<id>[a-zA-Z_\-0-9]+)"
    _NAME = "xhamster"
    
    def __init__(self, session, options):
        super(XHamsterComIE, self).__init__(session, options)
        self._prefix = "xhamster"
        
    def download(self):
        super(XHamsterComIE, self).download()
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        
        hsl = HslDL(self)
        hsl.download(self.cache_path)
        
    def extract(self):
        self.video.url = "https://xhamster.com/videos/{}".format(self.video.id)
        
        html = self._download_webpage(self.video.url)
        super(XHamsterComIE, self).extract()
        
        DOMdoc = BeautifulSoup(self._download_webpage(self._options.url), "lxml")
        
        
        # Extract id, title, description from JSON
        data = DOMdoc.find("script",  id="initials-script").text
        data = data.replace("window.initials=", "")
        data = data.replace(";", "")
        data = json.loads(data)
        
        self.video.id = data["videoModel"]["id"]
        self.video.title = data["videoModel"]["title"]
        self.video.description = data["videoModel"]["description"]
        
        # Extract HSL/m3u8 playlist
        self.video._hsl_index = data["xplayerSettings"]["sources"]["hls"]["url"]
        
        # Extract thumbnail
        self.video.thumbnail = data["videoModel"]["thumbURL"]
        
        # Extract creator informations
        self.video.creator = data["videoModel"]["author"]["name"]
        self.video.creator_url = data["videoModel"]["author"]["pageURL"]
        
        # Set task id
        self.task_id = "{:x}".format(crc32(str(self.video.title + str(self.video.id)).encode("utf-8")))
        
        # Set output filename if None
        if self._options.out == None:
            self._options.out = "{}.{}".format(self.video.title, self._options.format)
            
        self._extract_resolutions()
        
        # Check and select resolution to download
        if not self._options.resolution in self.video.resolutions:
            self.video.selected_res = self.video.resolution_best
        
        self.video._hsl_src = self.video._hsl_src_res_list[self.video.selected_res]
        
        self.cache_path = os.path.join(self._options.cach_dir, self.task_id)
        
    def _extract_resolutions(self):
        hsl = m3u8.loads(self._http_get(self.video._hsl_index))
        
        # Setting base url for hsl stuff (later used for downloading)
        self.video._hsl_base = self.video._hsl_index[:self.video._hsl_index.rfind('/')] + "/"
        
        for playlist in hsl.playlists:
            if playlist.stream_info.resolution[1] > self.video.resolution_best:
                self.video.resolution_best = playlist.stream_info.resolution[1]
            
            res_name = playlist.stream_info.resolution[1]
            self.video.resolutions.append(playlist.stream_info.resolution[1])
            self.video.resolutions_tuples.append(playlist.stream_info.resolution)
            self.video._hsl_src_res_list[res_name] = self.video._hsl_base + playlist.uri