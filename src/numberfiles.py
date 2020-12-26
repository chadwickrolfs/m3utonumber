import os
import os.path as ospath
from shutil import move as shmove
from glob import glob

class NumberFiles(object):
    '''
    Class to check for m3u playlists and subsequently add numbers to the front of tracks.
    dirtowalk 
    '''

    def __init__(self, dirtowalk):
        '''click '''
        self.dirtowalk = dirtowalk

    def numberfiles(self):
        m3uglob = f'{self.dirtowalk}**/*.m3u'
        # TODO: consider Path.rglob
        m3ufiles = glob(m3uglob, recursive=True)
        for m3ufile in m3ufiles:
            print(f'\nDEBUG:\nm3ufile: {m3ufile}\n')
            m3udir, m3ufilename = ospath.split(m3ufile)
            # print(f'\nDEBUG:\nm3udir: {m3udir}{os.sep}\ndirtowalk: {self.dirtowalk}\n')
            if f'{m3udir}{os.sep}' == self.dirtowalk:
                continue
            oggs = []
            oggdir = set()
            with open(m3ufile) as m3ufile_h:
                oggtracks = m3ufile_h.readlines()

            # os.chdir(m3udir)
            # print(f'\nDEBUG:\nchdir: {os.getcwd()}')
            for tracknumber, oggfile in enumerate(oggtracks):
                oggfilename = ospath.basename(oggfile).strip()
                oggglob = f'{self.dirtowalk}**/*{oggfilename}'
                # print(f'\nDEBUG:\noggfile: {oggfile}\nglob: {oggglob}')
                oggglobbed = glob(oggglob, recursive=True)

                oggfile = oggglobbed[0]

                oggdirname = ospath.dirname(oggfile)
                oggdir.add(oggdirname)

                if oggfilename[0:2].isdigit():
                    oggs.append(f'{oggfilename}\n')
                else:
                    numberedogg = f'{tracknumber:#02}-{oggfilename}'
                    oggs.append(f'numberedogg\n')
                    shmove(
                            oggfile,
                            ospath.join(oggdirname, numberedogg))

            with open(m3ufile, 'w') as m3ufile_h:
                m3ufile_h.writelines(oggs)

            if oggdir:
                # print(f'\nDEBUG\noggdir set: {oggdir}\n')
                oggdir = oggdir.pop()
                if m3udir != oggdir:
                    shmove(m3ufile, os.path.join(oggdir, m3ufilename))
