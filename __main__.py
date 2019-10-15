from loader import *
from merger import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url')
parser.add_argument('--firstsegment',type=int,default=1)
parser.add_argument('--sourcefolder')
parser.add_argument('--output')
parser.add_argument('--nodownload',action='store_true')


args = parser.parse_args()

print(args)
if __name__ == '__main__':
    if not args.nodownload:
        download_segments_parallel_main(args.url,args.sourcefolder,args.firstsegment)
    else:
        pass
    seg_list = get_segments_list(args.sourcefolder)
    concatenate(seg_list,args.output)

