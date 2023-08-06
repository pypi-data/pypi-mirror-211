import re
import json
import m3u8
from bs4 import BeautifulSoup
from .extractor import Extractor, crc32, os
from lewd_dl.__vars__ import __std__user_agent_tv__
from lewd_dl.downloader import HslDL

class PornHubIE(Extractor):
    _URL = "^https?://(?:(?:[^/]+)\.pornhub\.com\/(?:view_video\.php\?viewkey=))(?P<id>[a-zA-Z_\-0-9]+)"
    _NAME = "pornhub.com"
    
    def __init__(self, session, options):
        super(PornHubIE, self).__init__(session, options)
        
    def download(self):
        super(PornHubIE, self).download()
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        
        hsl = HslDL(self)
        hsl.download(self.cache_path)
    
    def extract(self):
        self.session.headers.update({"user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; AFTT Build/LVY48F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.10"})
        self.session.cookies.set("accessAgeDisclaimerPH", "1")
        
        #html = self._download_webpage(self._options.url)
        html = self._download_webpage("https://www.pornhub.com/view_video.php?viewkey={}".format(self.video.id))
        super(PornHubIE, self).extract()
        
        DOMdoc = BeautifulSoup(html, "lxml")
        v_id = DOMdoc.select("div#videoShow")[0]["data-video-id"]
        self.video._intern_id = v_id
        
        reJData = re.search("var flashvars_{}{}".format("[0-9]+", " = (?P<json>\{.*\});"), html)

        if reJData:
            jData = json.loads(reJData.group("json"))
            
            # Extract title
            self.video.title = jData["video_title"]
            
            for item in jData["mediaDefinitions"]:
                if item["format"] == "hls" and type(item["quality"]) == list:
                    # Extract HSL/m3u8 playlist
                    self.video._hsl_index = item["videoUrl"]
        

        data = json.loads(DOMdoc.select("script[type=\"application/ld+json\"]")[0].text)

        # Extract description
        self.video.description = data["description"]
        
        # Extract thumbnail
        self.video.thumbnail = data["thumbnailUrl"]
        
        # Extract creator
        self.video.creator = data["author"]
        self.video.creator_url = "https://www.pornhub.com/model/{}".format(self.video.creator)

              
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