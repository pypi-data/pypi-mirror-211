class Logger():
    def __init__(self):
        self._prefix = "lewd-dl"
        self.verbose = False
        
    def report_warning(self, text):
        if not self.verbose: return
    
    def report_info(self, text):
        print("[info] {}".format(text))
        
    def report_error(self, text, prefix = None):
        if prefix == None:
            print("[{}] Error {}".format(self._prefix, text))
        else:
            print("[{}] Error {}".format(prefix, text))
            
        if not self._options.ignore_errors:
            exit(1)
        
    def report(self, text, prefix = None):
        if prefix == None:
            print("[{}] {}".format(self._prefix, text))
        else:
            print("[{}] {}".format(prefix, text))
        
    def log_id(self, text):
        print("[{}] {}: {}".format(self._prefix, self.video.id, text))