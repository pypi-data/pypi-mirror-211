import json

class Video(object):
    def __init__(self):
        self.url = ""
        self.title = ""
        self.thumbnail = ""
        self.description = ""
        self.id = ""
        self.resolutions = []
        self.resolutions_tuples = []
        self.selected_res = None
        self.creator = ""
        self.creator_url = ""
        self.isHsl = False
        self.isFile = False
        
        self._hsl_index = ""
        self._hsl_selected = ""
        self._hsl_src = ""
        self._hsl_src_res_list = {}
        self._hsl_base = ""
        self.resolution_best = 0
        
    def set(self, key, value):
        setattr(self, key, value)
        
    def to_json(self):
        return json.dumps({
            title: self.title,
            creator: self.creator_url,
            url: self.url,
            thumbnail: self.thumbnail,
            description: self.description
        })