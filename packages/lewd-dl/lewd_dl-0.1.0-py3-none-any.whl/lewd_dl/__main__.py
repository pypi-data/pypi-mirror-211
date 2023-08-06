import os
from argparse import ArgumentParser
from .LewdDL import LewdDL, Options
from lewd_dl.__vars__ import __std__user_agent__, __std__request_rate_sec__, __std__format__, __std__cache_dir__


def main():    
    parser = ArgumentParser()
    parser.add_argument("url", type=str, nargs="?", help="Video urls to download")
    parser.add_argument("--user-agent", dest="ua", type=str, default=__std__user_agent__, help="Set user agent")
    parser.add_argument("-r", dest="res", type=str, default="best", help="Select resolution to download (By deafult \"best\" is chossen)")
    parser.add_argument("--rate-limit", metavar="SEC", type=int, default=__std__request_rate_sec__, help="Time to wait between download requests (default 0.5s)")
    parser.add_argument("-f", metavar="FORMAT" ,dest="format", default=__std__format__, help="Select format to download (default mp4)")
    parser.add_argument("-o", metavar="OUTPUT", dest="out", default=None, help="Output filename")
    parser.add_argument("--cache-dir", metavar="DIR", default=__std__cache_dir__, help="Set custom cache folder")
    
    parser.add_argument("-R", dest="res_list", action="store_true", help="Prints available resolutions and exits")
    parser.add_argument("--dump-user-agent", action="store_true", help="Prints current user-agent then exits")
    parser.add_argument("--platforms", action="store_true", help="Print list of supported platforms and exits")
    
    args = parser.parse_args()
    
    if args.dump_user_agent:
        print(args.ua)
        exit(0)
    
    options = Options()
    options.url = args.url
    options.ua = args.ua
    options.list_resolutions = args.res_list
    options.resolution = args.res
    options.rate_limit = args.rate_limit
    options.format = args.format
    options.out = args.out
    options.cach_dir = args.cache_dir
    options.print_platforms = args.platforms
    
    if not os.path.exists(options.cach_dir):
        os.mkdir(options.cach_dir)
    
    LewdDL.main(options)