import sys
import os
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
        scriptdir = os.getcwd()
        m3ufiles = glob.glob(
                f'{self.dirtowalk}/**/*.m3u',
                recursive=True)
        for m3ufile in m3ufiles:
            oggs = []
            oggdir = set()

            m3udir. m3ufilename = ospath.split(m3ufile)
            os.chdir(m3udir)

            with open(m3ufile, 'r+') as m3ufile_h:
                for tracknumber, oggfile in enumerate(m3ufile_h):
                    oggfilename = ospath.basename(oggfile)
                    oggdirname = ospath.dirname(oggfile)
                    oggdir.add(oggdirname)

                    if oggfilename[0:2].isdigit():
                        oggs.append(oggfilename)
                    else:
                        numberedogg = f'{tracknumber:#02}_{oggfilename}'
                        oggs.append(numberedogg)
                        shmove(
                                oggfile,
                                ospath.join(oggdirname, numberedogg))

                m3ufile_h.truncate()
                m3ufile_h.writelines(oggs)

            oggdir = oggdir[0]
            if m3udir != oggdir:
                shmove(m3ufile, os.path.join(oggdir, m3ufilename))
