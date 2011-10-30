#!/usr/bin/python

import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

class Tagit:
    
    def __init__(self, dir_name, dry_run=False):
        self.dir_name = dir_name
        self.dry_run = dry_run
        self.longest_filename = max([len(filename) for filename in self.get_mp3_file_list()])
        
    def format_filename(self, filename):
        return filename + (" " * (self.longest_filename - len(filename))) + "\t"

    def get_mp3_file_list(self):
        return [filename for filename in os.listdir(self.dir_name) if filename.endswith(".mp3")]
        
    def tag_track_numbers(self):
        print "-- track numbers --"
        start_track = 1
        for filename in self.get_mp3_file_list():
            print "" + self.format_filename(filename) + "tracknumber => " + str(start_track)
            if not self.dry_run:
                mp3_file = EasyID3(os.path.join(self.dir_name, filename))
                mp3_file["tracknumber"] = unicode(str(start_track))
                mp3_file.save()
            start_track += 1
        print "\n"
    
    def tag_titles_from_text_file(self, filename):
        print "-- titles --"
        f = open(filename, 'r')
        titles = f.readlines()
        mp3_files = self.get_mp3_file_list()
        if len(mp3_files) != len(titles):
            raise Exception("The count of titles in " + filename + " and the count of mp3 files are different")
        for filename, title in zip(mp3_files, titles):
            print "" + self.format_filename(filename) + "title => " + title.strip()
            if not self.dry_run:
                mp3_file = EasyID3(os.path.join(self.dir_name, filename))
                mp3_file["title"] = unicode(title.strip().decode('UTF-8'))
                mp3_file.save()
        print "\n"
        
    def tag_single_tag(self, tag_name, tag_value):
        print "-- " + tag_name + " --"
        for filename in self.get_mp3_file_list():
            print "" + self.format_filename(filename) + tag_name + " => " + tag_value
            if not self.dry_run:
                mp3_file = EasyID3(os.path.join(self.dir_name, filename))
                mp3_file[tag_name] = unicode(tag_value.decode('UTF-8'))
                mp3_file.save()
        print "\n"
        
    def tag_year(self, year):
        print "-- year --"
        from mutagen.id3 import TDRC, ID3TimeStamp
        ts = ID3TimeStamp(year + "-01-01 22:22:22")
        tdrc = TDRC(3, [ts]) 
        for filename in self.get_mp3_file_list():
            print "" + self.format_filename(filename) + "tdrc => " + str(tdrc)
            if not self.dry_run:
                mp3_file = EasyID3(os.path.join(self.dir_name, filename))
                mp3_file["date"] = unicode(year + "-01-01 22:22:22")
                mp3_file.save()
        print "\n"
    
    def tag_art(self, art_file):
        print "-- cover --"
        mime_type = None
        if art_file.endswith((".png", ".PNG")):
            mime_type = 'image/png'
        elif art_file.endswith((".jpg", ".JPG", ".jpeg", "JPEG")):
            mime_type = 'image/jpeg'
        if mime_type is None:
            raise Exception("invalid image file extension")            
        for filename in self.get_mp3_file_list():
            print "" + self.format_filename(filename) + "cover => " + art_file + " (" + mime_type  + ")"
            if not self.dry_run:
                audio = MP3(os.path.join(self.dir_name, filename), ID3=ID3)
                try:
                    audio.add_tags()
                except error:
                    pass
                audio.tags.add(
                    APIC(
                        encoding=3,
                        mime=mime_type,
                        type=3,
                        desc=u'Cover',
                        data=open(art_file).read()
                    )
                )
                audio.save()
        print "\n"

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", "--path", type="string", default=".",
                    help="the path to the directory containing the mp3 files", metavar="PATH")
    parser.add_option("-t", "--titles", type="string",
                    help="add title tag to mp3 files based on the lines found in input file", metavar="FILE")
    parser.add_option("-b", "--artist", type="string",
                    help="add artist tag to mp3 files", metavar="ARTIST")
    parser.add_option("-a", "--album", type="string",
                    help="add album tag to mp3 files", metavar="ALBUM")
    parser.add_option("-n", "--track-numbers",  action="store_true", dest="track_numbers", default=False, 
                    help="add track tag to mp3 files based on the order of files in the directory")
    parser.add_option("-i", "--image", type="string",
                    help="populate cover tag of mp3 files with the content found in input file", metavar="FILE")
    parser.add_option("-d", "--dry-run",  action="store_true", dest="dry_run", default=False, 
                    help="prints the action, but does not modify any file")
    parser.add_option("-y", "--year", type="string",
                    help="add year tag to mp3 files", metavar="YEAR")
                    
    (options, args) = parser.parse_args()
    t = Tagit(options.path, options.dry_run)
    if options.track_numbers:
        t.tag_track_numbers()
    if options.titles is not None:
        t.tag_titles_from_text_file(options.titles)
    if options.artist is not None:
        t.tag_single_tag("artist", options.artist)
    if options.album is not None:
        t.tag_single_tag("album", options.album)
    if options.image is not None:
        t.tag_art(options.image)
    if options.year is not None:
        t.tag_year(options.year)
    
if __name__ == "__main__":
    main()