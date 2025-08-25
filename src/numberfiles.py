import os
import pathlib
from dataclasses import dataclass
from shutil import move as shmove


@dataclass
class playfile:
    position: int
    original_path: str


@dataclass(repr=False)
class playlist:
    m3uname: str
    m3udir: str
    m3ulist: list[playfile]

    def __repr__(self):
        return self.m3uname


class NumberFiles(object):
    '''
    Class to check for m3u playlists and subsequently add numbers to the front
    of tracks.
    dirtowalk
    '''

    def __init__(self, dirtowalk):
        '''click '''
        self.dirtowalk = dirtowalk
        self.playlists: list = list()

    def list_playlists(self):
        self.get_m3ufiles()

        for self.m3ufile in self.m3ufiles:
            # print(f'\nDEBUG:\nm3ufile: {self.m3ufile}\n')
            self.make_playlist()
            self.playlists.append(self.playlist)

            # try to get a good list of playlists first
            continue

            line0 = self.playlist.m3ulist[0]
            if (line0.startswith('#') or line0.startswith('<')):
                print(f"extended m3u: {self.playlist.m3uname}")
                # os.remove(self.m3ufile)
                # TODO: parse it !
                continue

            try:
                self.ogg_tracks()
            except IndexError as e:
                print(f'\nHANDMATIG INTERVENTIE VERREIST\n{e}')
                continue

    def get_m3ufiles(self):
        m3uglob = '*.m3u'
        self.m3ufiles = sorted(self.dirtowalk.rglob(m3uglob))
        return self.m3ufiles

    def make_playlist(self):
        filelist = [
                playfile(pos, listfile)
                for pos, listfile
                in enumerate(self.m3ufile.read_text().split("\n"))
                if listfile
        ]
        self.playlist = playlist(
            self.m3ufile.name,
            self.m3ufile.parent,
            filelist,
        )

    def check_playlists(self):
        """check that files exist for all playlists
        hmm.. sometimes the file is named something else
        like the filename on disk is shortened
        maybe make a list of
        - bad playlists
        - which files have issues
        return the list then fix that list ?
        """
        for pl in self.playlists:
            m3udir_path = pathlib.Path(pl.m3udir)
            actual_oggs = [
                pfile.name
                for pfile
                in m3udir_path.glob("**/*.ogg")
            ]
            print(f"{pl.m3udir} actual: {actual_oggs}")
            for mfile in pl.m3ulist:
                file_path = pathlib.Path(mfile.original_path)
                if file_path.name not in actual_oggs:
                    print(f"{mfile.original_path} not found")

    def ogg_tracks(self):
        self.oggs = []
        self.oggdir = set()
        for self.tracknumber, self.oggfile in enumerate(
                self.playlist.m3ulist):
            oggglobbed = self.get_oggglob()

            self.oggfile = oggglobbed[0]

            self.oggdir.add(self.oggfile.parent)

            if self.oggfilename[0:2].isdigit():
                self.oggs.append(f'{self.oggfilename}\n')
            else:
                self.move_oggfile()

        self.write_m3ufile()
        self.move_m3ufile()

    def get_oggglob(self):
        oggglob = f'*{self.oggfile.name}'
        return sorted(self.dirtowalk.rglob(oggglob))

    def move_oggfile(self):
        numberedogg = f'{self.tracknumber:#02}-{self.oggfilename}'
        self.oggs.append(f'{numberedogg}\n')
        shmove(self.oggfile, self.oggfile.parent.joinpath(numberedogg))

    def write_m3ufile(self):
        with open(self.m3ufile, 'w') as m3ufile_h:
            m3ufile_h.writelines(self.oggs)

    def move_m3ufile(self):
        if self.oggdir:
            oggdir = self.oggdir.pop()
            if self.playlist.m3udir != oggdir:
                shmove(
                        self.m3ufile,
                        os.path.join(oggdir, self.playlist.m3ufilename))

    def get_playlists(self):
        return self.playlists
