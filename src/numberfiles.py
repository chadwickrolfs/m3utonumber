import os
import os.path as ospath
from shutil import move as shmove
from pathlib import Path

class NumberFiles(object):
    '''
    Class to check for m3u playlists and subsequently add numbers to the front of tracks.
    dirtowalk 
    '''

    def __init__(self, dirtowalk):
        '''click '''
        self.dirtowalk = Path(dirtowalk)

    def numberfiles(self):
        m3uglob = '*.m3u'
        m3ufiles = sorted(self.dirtowalk.rglob(m3uglob))
        for m3ufile in m3ufiles:
            print(f'\nDEBUG:\nm3ufile: {m3ufile}\n')
            m3udir, m3ufilename = ospath.split(m3ufile)
            # print(f'\nDEBUG:\nm3udir: {m3udir}{os.sep}\ndirtowalk: {self.dirtowalk}\n')
            if f'{m3udir}{os.sep}' == self.dirtowalk:
                continue
            with open(m3ufile) as m3ufile_h:
                oggtracks = m3ufile_h.readlines()
            line0 = oggtracks[0]
            if (line0.startswith('#') or line0.startswith('<')):
                os.remove(m3ufile)
                continue

            oggs = []
            oggdir = set()
            # os.chdir(m3udir)
            # print(f'\nDEBUG:\nchdir: {os.getcwd()}')
            for tracknumber, oggfile in enumerate(oggtracks):
                oggfilename = ospath.basename(oggfile).strip()
                oggglob = f'*{oggfilename}'
                print(f'\nDEBUG:\noggfile: {oggfile}\nglob: {oggglob}')
                oggglobbed = sorted(self.dirtowalk.rglob(oggglob))

                # possible shortened actual oggname compared to m3u
                # examples:
                #   acdc: what_do_you_do_for_money_h
                #   beatles revolve: got_to_get_you_into_my_lif
                # rename accordingly, but then how to find
                # perhaps another glob oggfilename[0-5]*.ogg or something?

                # beastieboys check your head m3u does not reflect reality
                # perhaps best to log these for handmatig correctie
                # but how to get out of this double for loop ?
                # will have to make a new method

                oggfile = oggglobbed[0]

                oggdirname = ospath.dirname(oggfile)
                oggdir.add(oggdirname)

                if oggfilename[0:2].isdigit():
                    oggs.append(f'{oggfilename}\n')
                else:
                    numberedogg = f'{tracknumber:#02}-{oggfilename}'
                    oggs.append(f'{numberedogg}\n')
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
