class Options():
    def __init__(self,
            url: str = "",
            ua: str = "",
            resolution: str = "",
            cach_dir: str = "/tmp/lewd-dl",
            format: str = "mp4"):
        
        self.url = url
        self.ua = ua
        self.format = format
        self.resolution = resolution
        self.cach_dir = cach_dir
        self.list_resolutions = False
        self.rate_limit = 0.5
        self.out = None
        self.print_platforms = False
        self.ignore_errors = False