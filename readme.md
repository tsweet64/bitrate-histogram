# bitrate-histogram

A simple python script to calculate a historam of the bitrates of media files in a directory recursively via `ffprobe`

To use, simply run `python histogram.py ext` (where ext is the file extension of media files you wish to scan for).

Example output:

```
117       | ################
119.5     | ######################
122       | ##################################################
124.5     | ##################################################
127       | ######################
129.5     | ######################
132       | ################
134.5     | 
137       | #####
```
