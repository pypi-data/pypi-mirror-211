import re
import m3u8
from .extractor import Extractor, crc32, os
from lewd_dl.downloader import HslDL

class XVideosIE(Extractor):
    _URL = "^https?://(?:(?:[^/]+)\.xvideos2?\.com/(?:video|embedframe\/))(?P<id>[0-9]+)"
    _NAME = "xvideos.com"
    
    def __init__(self, session, options):
        super(XVideosIE, self).__init__(session, options)
        self._prefix = "xvideos"
        
    def download(self):
        super(XVideosIE, self).download()
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        
        hsl = HslDL(self)
        hsl.download(self.cache_path)
    
    def extract(self):
        html = self._download_webpage(self._options.url)
        super(XVideosIE, self).extract()
        
        # https://www.xvideos.com/profiles/<NAME>
        
        data_list = {
            'title': "html5player\.setVideoTitle\('(.*)'\)",
            'thumbnail': "html5player\.setThumbUrl169\('(.*)'\)",
            'creator': "html5player\.setUploaderName\('(.*)'\)",
            '_hsl_index': "html5player\.setVideoHLS\('(.*)'\)"
        }
        
        for key in data_list:
            match = re.search(data_list[key], html)
            if match:
                self.video.set(key, match.group(1))
                
        self.video.creator_url = "https://www.xvideos.com/profiles/{}".format(self.video.creator)
        
        self._extract_resolutions()
        
        # Set task id
        self.task_id = "{:x}".format(crc32(str(self.video.title + str(self.video.id)).encode("utf-8")))
        
        # Set output filename if None
        if self._options.out == None:
            self._options.out = "{}.{}".format(self.video.title, self._options.format)
        
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