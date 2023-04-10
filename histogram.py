# recursively scan a dir for files of the specified extension, execute ffprobe on them, and build a histogram of their bitrates
# Usage: histogram.py <extension> (e.g., histogram.py opus)
import sys
import json
import glob
import numpy as np
from multiprocessing import Pool, cpu_count
from subprocess import Popen,PIPE,STDOUT,DEVNULL

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <extension to scan>")
    sys.exit(1)
SCAN_EXT = sys.argv[1]
GLOB_PATH = './**/*.' + SCAN_EXT
BIN_SIZE = 2.5

def run_ffmpeg(filename):
    with Popen(['ffprobe', filename, '-show_format', '-of', 'json'], stdout=PIPE, stderr=DEVNULL) as process:
        return process.communicate()[0].decode('utf-8')

def get_bitrate(filename):
    try:
        ffoutput = json.loads(run_ffmpeg(filename))
        bitratestr = ffoutput["format"]["bit_rate"]
        bitrate = float(bitratestr) / 1000 # to kbits
    except Exception as e:
        print("Failed to process file: " + filename)
        return None
    #print(bitrate)
    return bitrate

# https://gist.github.com/joezuntz/2f3bdc2ab0ea59229907
def ascii_hist(hist, bin_edges):
    total = 1.0*len(bin_edges)
    width = 50
    nmax = hist.max()
    for (xi, n) in zip(bin_edges, hist):
        bar = '#'*int(n*1.0*width/nmax)
        xi = '{0: <8.4g}'.format(xi).ljust(10)
        print('{0}| {1}'.format(xi,bar))

with Pool(cpu_count()) as pool:
    bitrate_list = pool.map_async(get_bitrate, glob.iglob(GLOB_PATH, recursive=True)).get()

bitrate_list = list(filter(lambda item: item is not None, bitrate_list)) # Remove None values from list (items which failed to be analyzed)
try:
    bins = np.arange(min(bitrate_list), max(bitrate_list) + BIN_SIZE, BIN_SIZE) # bin width of BIN_SIZE
    hist, bin_edges = np.histogram(list(bitrate_list), bins)
    ascii_hist(hist, bin_edges)
except Exception as e:
    print("Failed to parse bitrates list. Two or more files not found maybe?")
    sys.exit(1)
