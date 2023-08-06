import os
import re
from lewd_dl.log import Logger

class FFMPEG(Logger):
    def __init__(self, ie):
        super(FFMPEG, self).__init__()
        self._prefix = "ffmpeg"
        self.ie = ie
    
    def hsl_combine(self):
        self.report("Concatenating segments together")
        
        parts_file = os.path.join(self.ie.cache_path, "concat.part")
        seg_files = os.listdir(self.ie.cache_path)
        if "concat.part" in seg_files:
            seg_files.remove("concat.part")
        
        p = re.compile(r'\d+')
        seg_files = sorted(seg_files, key=lambda s: int(p.search(s).group()))
        
        with open(parts_file, "wb") as master_file:
            for seg_file in seg_files:
                if not seg_file.endswith(".ts"):
                    continue
                
                file = os.path.join(self.ie.cache_path, seg_file)
                
                with open(file, "rb") as seg:
                    print(file)
                    master_file.write(seg.read())
                    
        if os.path.exists(self.ie._options.out):
            return
        
        cmd = "ffmpeg -i {} -f {} -acodec copy -vcodec copy \"{}\"".format(
            parts_file,
            self.ie._options.format,
            self.ie._options.out
        )
        self.report("Exec: " + cmd)
        status = os.system(cmd)