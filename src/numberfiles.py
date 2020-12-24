import sys
import os
import os.path
import subprocess as sp

class NumberFiles(object):
  """
  Class to check for m3u playlists and subsequently add numbers to the
  front of tracks.
  """

  def __init__(self, dirtowalk):
    self.dirtowalk = dirtowalk

  def numberfiles(self):
    """
    work for NumberFiles
    """

    dirdepth = 0
    for dirpath, dnames, filenames in os.walk(self.dirtowalk):
      dirdepth += 1
      print "\n#current depth#\n{3}\n#current path#\n{0}\n#current directories#\n{1}\n#current files#\n{2}".format(dirpath, dirnames, filenames, dirdepth)
      for filename in filenames:
        if filename.endswith('m3u'):
          print "found a playlist - contents:\n"
          playlistpath = os.path.join(dirpath, filename)
          playlistfile = open(playlistpath, "r")
          for tracknumber, filename in enumerate(playlistfile):
            (headpart, addnumberpart) = os.path.split(filename)
            if addnumberpart[0:2].isdigit():
              print "{0} already numbered".format(addnumberpart)
            else:
              addednumber = "{0:#02}-{1}".format(tracknumber, addnumberpart)
              if dirdepth == 2:
                exifile = os.path.join(dirpath, headpart, addnumberpart).strip("\n")
                newfile = os.path.join(dirpath, headpart, addednumber).strip("\n")
	      else:
                exifile = os.path.join(self.dirtowalk, headpart, addnumberpart).strip("\n")
                newfile = os.path.join(self.dirtowalk, headpart, addednumber).strip("\n")
              print "'{0}' '{1}'".format(exifile, newfile)
              # os.rename(exifile, newfile)
              movecommand = "mv -nv '{0}' '{1}'".format(exifile, newfile)
              sp.call(movecommand, shell=True)
