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
        dirdepth = 0
        for dirpath, dnames, filenames in oswalk(self.dirtowalk):
            dirdepth += 1
            print(
                    "\n#current depth#\n{3}\n#current path#\n{0}\
                            \n#current directories#\n{1}\n#current files#\n{2}".format(
                        dirpath, dnames, filenames, dirdepth))
            for filename in filenames:
                if filename.endswith('m3u'):
                    print("found a playlist - contents:\n")
                    playlistpath = ospath.join(dirpath, filename)
                    playlistfile = open(playlistpath, "r")
                    for tracknumber, filename in enumerate(playlistfile):
                        (headpart, addnumberpart) = ospath.split(filename)
                        if addnumberpart[0:2].isdigit():
                            print("{0} already numbered".format(addnumberpart))
                        else:
                            addednumber = "{0:#02}-{1}".format(tracknumber, addnumberpart)
                            if dirdepth == 2:
                                exifile = ospath.join(dirpath, headpart, addnumberpart).strip("\n")
                                newfile = ospath.join(dirpath, headpart, addednumber).strip("\n")
                            else:
                                exifile = ospath.join(self.dirtowalk, headpart, addnumberpart).strip("\n")
                                newfile = ospath.join(self.dirtowalk, headpart, addednumber).strip("\n")

                        print("moving '{0}' '{1}'".format(exifile, newfile))
                        shmove(exifile, newfile)

# find m3u files
# find ogg files
# read m3u file line by line
#     compare with each ogg file
#     rename ogg file with number
