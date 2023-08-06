import m3u8
import time
import os
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn, SpinnerColumn
from lewd_dl.log import Logger

class HslDL(Logger):
    def __init__(self, ie):
        super(HslDL, self).__init__()
        self._prefix = "download"
        
        self.ie = ie
        
    def download(self, download_path):     
        seg_count = 0
           
        progress_bar = Progress(
            SpinnerColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("-"),
            TimeElapsedColumn()
        )
        
        is_skiped = True

        playlist = m3u8.loads(self.ie._http_get(self.ie.video._hsl_src))
        with progress_bar as p:
            for i in p.track(range(playlist.files.__len__())):
                seg = playlist.files[i]
                seg_dl_path = os.path.join(download_path, "{}.ts".format(seg_count))
                
                if not os.path.exists(seg_dl_path):
                    print(seg_dl_path)
                    with open(seg_dl_path, "wb") as seg_file:
                        seg_file.write(self.ie._http_get(os.path.join(self.ie.video._hsl_base, seg), True))
                        is_skiped = False
                        seg_count += 1
                    time.sleep(self.ie._options.rate_limit)
                    
        if is_skiped:
            self.report("Download skiped")
        else:
            self.report("Download complete")
                    