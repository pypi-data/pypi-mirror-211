import re
import json
import m3u8
from bs4 import BeautifulSoup
from .extractor import Extractor, crc32, os
from lewd_dl.downloader import HslDL

class XnxxIE(Extractor):
    _URL = "^https?://(?:(?:[^/]+)\.xnxx\.com\/(?:video-|embedframe\/))(?P<id>[a-zA-Z_\-0-9]+)"
    _NAME = "xnxx.com"
    
    def __init__(self, session, options):
        super(XnxxIE, self).__init__(session, options)
        
    def download(self):
        super(XnxxIE, self).download()
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        
        hsl = HslDL(self)
        hsl.download(self.cache_path)
    
    def extract(self):
        html = self._download_webpage(self._options.url)
        super(XnxxIE, self).extract()
        
        # Extract id
        v_id = re.search(r"var html5player = new HTML5Player\('html5video', '([0-9]+)'\);", html)
        if not v_id:
            self.report_error("Could not extract video id")

        self.video.id = v_id.group(1)
        
        
        # Extract title
        v_title = re.search(r"html5player\.setVideoTitle\('(.*)'\)", html)
        if not v_title:
            self.report_error("Could not extract video title")

        self.video.title = v_title.group(1)
        
        
        # Extract description
        self.report("Skiped description")
        
        
        # Extract HSL/m3u8 playlist
        v_hls = re.search(r"html5player\.setVideoHLS\('(.*)'\)", html)
        if not v_hls:
            self.report_error("Could not extract video hls playlist")

        self.video._hsl_index = v_hls.group(1)
        
        
        # Extract thumbnail
        v_thumbnail = re.search(r"html5player\.setThumbUrl\('(.*)'\)", html)
        if not v_thumbnail:
            self.report_warning("Could not extract video thumbnail")

        self.video.thumbnail = v_thumbnail.group(1)
        
        
        # Extract creator (uploader name)
        v_creator = re.search(r"html5player\.setUploaderName\('(.*)'\)", html)
        if not v_creator:
            self.report_warning("Could not extract video creator")

        self.video.creator = v_creator.group(1)
        self.video.creator_url = "https://www.xvideos.com/profiles/{}".format(self.video.creator)

              
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