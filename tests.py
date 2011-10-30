import tagit
import unittest
import shutil
from mutagen.easyid3 import EasyID3
import os

class TagitTests(unittest.TestCase):

    def setUp(self):
        shutil.copytree("sampledata/Ayatollah (2008) Louder - no tags", "sampledata/no tags")
        
    def tearDown(self):
        shutil.rmtree("sampledata/no tags")

    def test_get_mp3_file_list(self):
        
        t = tagit.Tagit("sampledata/Ayatollah (2008) Louder")
        
        expected_files = [ "01-ayatollah-intro.mp3"
            , "02-ayatollah-circulate.mp3"
            , "03-ayatollah-louder.mp3"
            , "04-ayatollah-other_worlds.mp3"
            , "05-ayatollah-into_space.mp3"
            , "06-ayatollah-naturally_born.mp3"
            , "07-ayatollah-chariots_of_the_gods.mp3"
            , "08-ayatollah-music_to_my_ears.mp3"
            , "09-ayatollah-eye_pod.mp3"
        ]
    
        actual_files = t.get_mp3_file_list()
        self.assertEquals(expected_files, actual_files)
    
    def test_format_filename(self):
        t = tagit.Tagit("sampledata/Ayatollah (2008) Louder")
        self.assertEquals(t.format_filename("01-ayatollah-intro.mp3"), "01-ayatollah-intro.mp3               \t")
    
    def test_tag_track_numbers(self):        
        t = tagit.Tagit("sampledata/no tags")
        t.tag_track_numbers()
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "01-ayatollah-intro.mp3"))
        self.assertEquals(mp3_file["tracknumber"][0], u'1')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "02-ayatollah-circulate.mp3"))
        self.assertEquals(mp3_file["tracknumber"][0], u'2')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "06-ayatollah-naturally_born.mp3"))
        self.assertEquals(mp3_file["tracknumber"][0], u'6')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "09-ayatollah-eye_pod.mp3"))
        self.assertEquals(mp3_file["tracknumber"][0], u'9')

    def test_tag_titles_from_text_file(self):
        t = tagit.Tagit("sampledata/no tags")
        t.tag_titles_from_text_file("sampledata/title_list")
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "01-ayatollah-intro.mp3"))
        self.assertEquals(mp3_file["title"][0], u'Intro')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "02-ayatollah-circulate.mp3"))
        self.assertEquals(mp3_file["title"][0], u'Circulat\xe9')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "06-ayatollah-naturally_born.mp3"))
        self.assertEquals(mp3_file["title"][0], u'Naturally Born')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "09-ayatollah-eye_pod.mp3"))
        self.assertEquals(mp3_file["title"][0], u'Eye Pod')
        
        
    def test_tag_artist(self):
        t = tagit.Tagit("sampledata/no tags")
        t.tag_single_tag("artist", "Ayatollah")
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "01-ayatollah-intro.mp3"))
        self.assertEquals(mp3_file["artist"][0], u'Ayatollah')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "02-ayatollah-circulate.mp3"))
        self.assertEquals(mp3_file["artist"][0], u'Ayatollah')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "06-ayatollah-naturally_born.mp3"))
        self.assertEquals(mp3_file["artist"][0], u'Ayatollah')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "09-ayatollah-eye_pod.mp3"))
        self.assertEquals(mp3_file["artist"][0], u'Ayatollah')
        
    def test_tag_album(self):
        t = tagit.Tagit("sampledata/no tags")
        t.tag_single_tag("album", "Louder")
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "01-ayatollah-intro.mp3"))
        self.assertEquals(mp3_file["album"][0], u'Louder')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "02-ayatollah-circulate.mp3"))
        self.assertEquals(mp3_file["album"][0], u'Louder')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "06-ayatollah-naturally_born.mp3"))
        self.assertEquals(mp3_file["album"][0], u'Louder')
        mp3_file = EasyID3(os.path.join("sampledata/no tags", "09-ayatollah-eye_pod.mp3"))
        self.assertEquals(mp3_file["album"][0], u'Louder')
        
    def test_tag_art(self):
        t = tagit.Tagit("sampledata/no tags")
        t.tag_art("sampledata/albumart.png")
        
    def test_tag_year(self):
        t = tagit.Tagit("sampledata/no tags")
        t.tag_year("2010")
        #shutil.copytree("no tags", "saved - year")