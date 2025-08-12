import os
import os.path as ospath
from shutil import move as shmove
from pathlib import Path


class NumberFiles(object):
    '''
    Class to check for m3u playlists and subsequently add numbers to the front
    of tracks.
    dirtowalk
    '''

    def __init__(self, dirtowalk):
        '''click '''
        self.dirtowalk = Path(dirtowalk)

    def numberfiles(self):
        m3ufiles = self.get_m3ufiles()

        for self.m3ufile in m3ufiles:
            print(f'\nDEBUG:\nm3ufile: {self.m3ufile}\n')
            self.m3udir, self.m3ufilename = ospath.split(self.m3ufile)
            if f'{self.m3udir}{os.sep}' == self.dirtowalk:
                continue

            self.oggtracks = self.get_oggtracks()
            if not self.oggtracks:
                continue

            line0 = self.oggtracks[0]
            if (line0.startswith('#') or line0.startswith('<')):
                os.remove(self.m3ufile)
                continue

            try:
                self.ogg_tracks()
            except IndexError as e:
                print(f'\nHANDMATIG INTERVENTIE VERREIST\n{e}')
                continue

    def get_oggtracks(self):
        with open(self.m3ufile) as m3ufile_h:
            return m3ufile_h.readlines()

    def get_m3ufiles(self):
        m3uglob = '*.m3u'
        return sorted(self.dirtowalk.rglob(m3uglob))

    def ogg_tracks(self):
        self.oggs = []
        self.oggdir = set()
        for self.tracknumber, self.oggfile in enumerate(
                self.oggtracks):
            oggglobbed = self.get_oggglob()

            self.oggfile = oggglobbed[0]

            self.oggdirname = ospath.dirname(self.oggfile)
            self.oggdir.add(self.oggdirname)

            if self.oggfilename[0:2].isdigit():
                self.oggs.append(f'{self.oggfilename}\n')
            else:
                self.move_oggfile()

        self.write_m3ufile()
        self.move_m3ufile()

    def get_oggglob(self):
        self.oggfilename = ospath.basename(self.oggfile).strip()
        oggglob = f'*{self.oggfilename}'
        return sorted(self.dirtowalk.rglob(oggglob))

    def move_oggfile(self):
        numberedogg = f'{self.tracknumber:#02}-{self.oggfilename}'
        self.oggs.append(f'{numberedogg}\n')
        shmove(self.oggfile, ospath.join(self.oggdirname, numberedogg))

    def write_m3ufile(self):
        with open(self.m3ufile, 'w') as m3ufile_h:
            m3ufile_h.writelines(self.oggs)

    def move_m3ufile(self):
        if self.oggdir:
            oggdir = self.oggdir.pop()
            if self.m3udir != oggdir:
                shmove(
                        self.m3ufile,
                        os.path.join(oggdir, self.m3ufilename))
