import sys
from os import walk as oswalk
import os.path as ospath
from shutil import move as shmove

class NumberFiles(object):
    """
    Class to check for m3u playlists and subsequently add numbers to the front of tracks.
    dirtowalk 
    """

    def __init__(self, dirtowalk):
        '''click '''
        self.dirtowalk = dirtowalk

    def numberfiles(self):
        m3ufiles = glob.glob(f'{self.dirtowalk}/**/*.m3u', recursive=True)
        for m3ufile in m3ufiles:
            m3udir = os.dirname(m3ufile)
            with open(m3ufile, 'r+') as m3ufile_h:
                oggs = [os.path.basename(oggfile) for oggfile in m3ufile_h.readlines()]
                m3ufile_h.truncate()
                m3ufile.readlines(oggs)
            # determine where the ogg directory is relative to the m3u file
            # move m3u file into ogg directory
            for track, ogg in enumerate(oggs):
                shmove(ogg, f'{track:#02}-{ogg}')


# find m3u files
# g = glob.glob(f'{dirtowalk}/**/*.m3u', recursive=True)
# readlines from m3u file, only the filename
#     with open(g[0], 'r+') as gf
#       oggs = [os.path.basename(x) for x in gf.readlines()]
#     compare with each ogg file
#     rename ogg file with number
