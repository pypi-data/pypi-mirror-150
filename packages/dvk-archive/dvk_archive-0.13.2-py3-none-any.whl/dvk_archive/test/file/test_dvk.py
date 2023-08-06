#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.test.temp_dir import get_test_dir
from dvk_archive.main.web.bs_connect import download
from os import remove, mkdir, pardir, stat
from os.path import abspath, basename, exists, join

def test_can_write():
    """
    Tests the can_write method.
    """
    # TEST VALID DVK THAT CAN BE WRITTEN
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(abspath(join(test_dir, "write.dvk")))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    assert dvk.can_write()
    # TEST WITH NO DVK FILE
    dvk.set_dvk_file(None)
    assert not dvk.can_write()
    # TEST DVK FILE WITHOUT EXISTING PARENT DIRECTORY
    dvk.set_dvk_file("/non-existant/file.dvk")
    assert not dvk.can_write()
    # TEST WITH NO DVK ID
    dvk.set_dvk_file(abspath(join(test_dir, "write.dvk")))
    dvk.set_dvk_id(None)
    assert not dvk.can_write()
    # TEST WITH NO TITLE
    dvk.set_dvk_id("id123")
    dvk.set_title(None)
    assert not dvk.can_write()
    # TEST WITH NO ARTIST
    dvk.set_title("Title")
    dvk.set_artist(None)
    assert not dvk.can_write()
    # TEST WITH NO PAGE URL
    dvk.set_artist("artist")
    dvk.set_page_url(None)
    assert not dvk.can_write()
    # TEST WITH NO MEDIA FILE
    dvk.set_page_url("/url/")
    dvk.set_media_file("")
    assert not dvk.can_write()
    # TEST VALID WRITABLE DVK
    dvk.set_media_file("file.txt")
    assert dvk.can_write()

def test_get_set_dvk_file():
    """
    Tests the get_dvk_file and set_dvk_file methods.
    """
    # TEST EMPTY DVK FILE WITH CONSTRUCTOR
    dvk = Dvk();
    assert dvk.get_dvk_file() is None
    # TEST GETTING AND SETTING DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "blah.dvk"))
    assert basename(dvk.get_dvk_file()) == "blah.dvk"
    assert abspath(join(dvk.get_dvk_file(), pardir)) == test_dir
    # TEST SETTING DVK FILE TO NULL
    dvk.set_dvk_file(None)
    assert dvk.get_dvk_file() is None
    # WRITE DVK FILE
    dvk.set_dvk_file(join(test_dir, "new.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert basename(read_dvk.get_dvk_file()) == "new.dvk"
    assert abspath(join(read_dvk.get_dvk_file(), pardir)) == test_dir

def test_get_set_dvk_id():
    """
    Tests the get_dvk_id and set_dvk_id methods.
    """
    # Test setting empty ID with constructor
    dvk = Dvk()
    assert dvk.get_dvk_file() is None
    # Test getting and setting Dvk ID
    dvk.set_dvk_id("id1234")
    assert dvk.get_dvk_id() == "ID1234"
    dvk.set_dvk_id("TST128-J")
    assert dvk.get_dvk_id() == "TST128-J"
    # Test setting ID with whitespace
    dvk.set_dvk_id(" thg124  ")
    assert dvk.get_dvk_id() == "THG124"
    dvk.set_dvk_id("   ")
    assert dvk.get_dvk_id() is None
    # Test invalid IDs
    dvk.set_dvk_id(None)
    assert dvk.get_dvk_id() is None
    dvk.set_dvk_id("")
    assert dvk.get_dvk_id() is None
    # Write Dvk file
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "id_dvk.dvk"))
    dvk.set_dvk_id("WRITE456")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading Dvk ID
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_dvk_id() == "WRITE456"

def test_get_set_title():
    """
    Tests the get_title and set_title methods.
    """
    # Test empty title from constructor
    dvk = Dvk()
    assert dvk.get_title() is None
    # Test getting and setting title
    dvk.set_title("Test Title")
    assert dvk.get_title() == "Test Title"
    dvk.set_title(None)
    assert dvk.get_title() is None
    dvk.set_title("")
    assert dvk.get_title() == ""
    # Test title with whitespace
    dvk.set_title("  To much space ")
    assert dvk.get_title() == "To much space"
    dvk.set_title("    ")
    assert dvk.get_title() == ""
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "ttl_dvk.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title #2")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading title from Dvk file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_title() == "Title #2"

def test_get_set_artists():
    """
    Tests the get_artists, set_artist and set_artists methods.
    """
    # Test empty artists from constructor
    dvk = Dvk()
    assert len(dvk.get_artists()) == 0
    # Test getting and setting a single artist
    dvk.set_artist("Artist Person")
    assert len(dvk.get_artists()) == 1
    assert dvk.get_artists()[0] == "Artist Person"
    dvk.set_artist("")
    assert len(dvk.get_artists()) == 0
    # Test getting and setting multiple artists
    artists = ["artist10", "artist10", "", None, "artist1",
                "test1.0.20-stuff", "test10.0.0-stuff"]
    dvk.set_artists(artists)
    assert len(dvk.get_artists()) == 4
    assert dvk.get_artists()[0] == "artist1"
    assert dvk.get_artists()[1] == "artist10"
    assert dvk.get_artists()[2] == "test1.0.20-stuff"
    assert dvk.get_artists()[3] == "test10.0.0-stuff"
    # Test getting and setting artists with whitespace
    artists = ["   ABC   ", "    ", "thing  ", "  other"]
    dvk.set_artists(artists)
    assert len(dvk.get_artists()) == 3
    assert dvk.get_artists()[0] == "ABC"
    assert dvk.get_artists()[1] == "other"
    assert dvk.get_artists()[2] == "thing"
    # Test setting invalid artist values
    dvk.set_artist(None)
    assert len(dvk.get_artists()) == 0
    dvk.set_artists(None)
    assert len(dvk.get_artists()) == 0
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "artist.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    artists = ["Person"]
    artists.append("artist")
    dvk.set_artists(artists)
    dvk.set_page_url("/url")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading artists from a Dvk file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert len(read_dvk.get_artists()) == 2
    assert read_dvk.get_artists()[0] == "artist"
    assert read_dvk.get_artists()[1] == "Person"

def test_set_time_int():
    """
    Tests the set_time_int method.
    """
    # TEST EMPTY TIME FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST VALID TIME
    dvk.set_time_int(2017, 10, 6, 19, 15)
    assert dvk.get_time() == "2017/10/06|19:15"
    # TEST INVALID YEAR
    dvk.set_time_int(0, 10, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID MONTH
    dvk.set_time_int(2017, 0, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 13, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID DAY
    dvk.set_time_int(2017, 10, 0, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 32, 7, 15);
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID HOUR
    dvk.set_time_int(2017, 10, 10, -1, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 10, 24, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID MINUTE
    dvk.set_time_int(2017, 10, 10, 7, -1)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 10, 7, 60)
    assert dvk.get_time() == "0000/00/00|00:00"
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "time_dvk.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_time_int(2020, 10, 26, 21, 15)
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING TIME FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_time() == "2020/10/26|21:15"

def test_get_set_time():
    """
    Tests the get_time and set_time methods.
    """
    # TEST DEFAULT TIME FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST GETTING AND SETTING TIME
    dvk.set_time("2017!10!06!05!00")
    assert dvk.get_time() == "2017/10/06|05:00"
    # TEST SETTING INVALID TIMES
    dvk.set_time(None)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("2017/10/06")
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("yyyy/mm/dd/hh/tt")
    assert dvk.get_time() == "0000/00/00|00:00"
    # WRITE DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "time.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_time("2020/10/27|17:55")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING TIME FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_time() == "2020/10/27|17:55"

def test_get_set_web_tags():
    """
    Tests the get_web_tags and set_web_tags methods.
    """
    # Test empty web tags from constructor
    dvk = Dvk()
    assert dvk.get_web_tags() == []
    # Test getting and setting web tags
    tags = ["tag2", "Tag1", "tag2", None]
    dvk.set_web_tags(tags)
    assert len(dvk.get_web_tags()) == 2
    assert dvk.get_web_tags()[0] == "tag2"
    assert dvk.get_web_tags()[1] == "Tag1"
    # Test Setting web tags with whitespace
    tags = ["other tag   ", "  thing", "  "]
    dvk.set_web_tags(tags)
    assert len(dvk.get_web_tags()) == 2
    assert dvk.get_web_tags()[0] == "other tag"
    assert dvk.get_web_tags()[1] == "thing"
    # Test invalid tags
    dvk.set_web_tags(None)
    assert dvk.get_web_tags() == []
    dvk.set_web_tags([])
    assert dvk.get_web_tags() == []
    tags = [None]
    dvk.set_web_tags(tags)
    assert dvk.get_web_tags() == []
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "tags.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    tags = ["String"]
    tags.append("tags")
    dvk.set_web_tags(tags)
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading web tags from Dvk file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert len(read_dvk.get_web_tags()) == 2
    assert read_dvk.get_web_tags()[0] == "String"
    assert read_dvk.get_web_tags()[1] == "tags"

def test_get_set_description():
    """
    Tests the get_description and set_descritpion methods.
    """
    # Test default description from constructor
    dvk = Dvk()
    assert dvk.get_description() is None
    # Test getting and setting description
    dvk.set_description("   <i>\"Ba&#241;o\"</i>  ")
    assert dvk.get_description() == "<i>&#34;Baño&#34;</i>"
    dvk.set_description("<i>Ba&#241;o</i>")
    assert dvk.get_description() == "<i>Baño</i>"
    # Test setting empty description
    dvk.set_description(None)
    assert dvk.get_description() is None
    dvk.set_description("")
    assert dvk.get_description() is None
    dvk.set_description("   ")
    assert dvk.get_description() is None
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "desc.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_description("Other Description")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading description from Dvk file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_description() == "Other Description"

def test_get_set_page_url():
    """
    Tests the get_page_url and set_page_url methods.
    """
    # Test empty page URL from constructor
    dvk = Dvk()
    assert dvk.get_page_url() is None
    # Test getting and setting page URL
    dvk.set_page_url("/Page/URL")
    assert dvk.get_page_url() == "/Page/URL"
    # Test setting invalid URL
    dvk.set_page_url(None)
    assert dvk.get_page_url() is None
    dvk.set_page_url("")
    assert dvk.get_page_url() is None
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "page.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("test.net/url/Page")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading page URL from Dvk file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_page_url() == "test.net/url/Page"

def test_get_set_direct_url():
    """
    Tests the get_direct_url and set_direct_url methods.
    """
    # Test empty direct URL from constructor
    dvk = Dvk()
    assert dvk.get_direct_url() is None
    # Test getting and setting direct URL
    dvk.set_direct_url("/direct/URL")
    assert dvk.get_direct_url() == "/direct/URL"
    # Test setting invalid direct URL
    dvk.set_direct_url(None)
    assert dvk.get_direct_url() is None
    dvk.set_direct_url("")
    assert dvk.get_direct_url() is None
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "direct.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_direct_url("test.net/url/Direct")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading direct URL
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_direct_url() == "test.net/url/Direct"

def test_get_set_secondary_url():
    """
    Tests the get_secondary_url and set_secondary_url methods.
    """
    # Test empty secondary URL from constructor
    dvk = Dvk()
    assert dvk.get_secondary_url() is None
    # Test getting and setting secondary URL
    dvk.set_secondary_url("/Page/URL")
    assert dvk.get_secondary_url() == "/Page/URL"
    # Test setting invalid secondary URL
    dvk.set_secondary_url(None)
    assert dvk.get_secondary_url() is None
    dvk.set_secondary_url("")
    assert dvk.get_secondary_url() is None
    # Write Dvk
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "sec.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_secondary_url("test.net/url/second")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading secondary URL from Dvk file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_secondary_url() == "test.net/url/second"

def test_get_set_media_file():
    """
    Tests the get_media_file and set_media_file methods.
    """
    # TEST EMPTY MEDIA FILE FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_media_file() is None
    # TEST SETTING MEDIA FILE WITH NO DVK FILE SET
    dvk.set_media_file("file.txt")
    assert dvk.get_media_file() is None
    # TEST SETTING MEDIA FILE FROM DVK FILE WITH INVALID PARENT
    dvk.set_dvk_file("/non-existant/file.dvk")
    dvk.set_media_file("file.txt")
    assert dvk.get_media_file() is None
    # TEST SETTING MEDIA WITH VALID DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "file.dvk"))
    dvk.set_media_file("file.txt")
    assert abspath(join(dvk.get_media_file(), pardir)) == test_dir
    assert basename(dvk.get_media_file()) == "file.txt"
    # TEST SETTING INVALID MEDIA FILE WITH INVALID DVK FILE
    dvk.set_media_file(None)
    assert dvk.get_media_file() is None
    dvk.set_media_file("")
    assert dvk.get_media_file() is None
    # WRITE DVK
    dvk.set_dvk_file(join(test_dir, "media.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING MEDIA FILE VALUE FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert abspath(join(read_dvk.get_media_file(), pardir)) == test_dir
    assert basename(read_dvk.get_media_file()) == "media.png"

def test_get_set_secondary_file():
    """
    Tests the get_secondary_file and set_secondar_file methods.
    """
    # TEST EMPTY SECONDARY MEDIA FILE FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_secondary_file() is None
    # TEST SETTING SECONDARY MEDIA FILE WITH NO DVK FILE SET
    dvk.set_secondary_file("file.txt")
    assert dvk.get_secondary_file() is None
    # TEST SETTING SECONDARY MEDIA FILE FROM DVK FILE WITH INVALID PARENT
    dvk.set_dvk_file("/non-existant/file.dvk")
    dvk.set_secondary_file("file.txt")
    assert dvk.get_secondary_file() is None
    # TEST SETTING SECONDARY MEDIA WITH VALID DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "file.dvk"))
    dvk.set_secondary_file("file.txt")
    assert abspath(join(dvk.get_secondary_file(), pardir)) == test_dir
    assert basename(dvk.get_secondary_file()) == "file.txt"
    # TEST SETTING INVALID SECONDARY MEDIA FILE WITH INVALID DVK FILE
    dvk.set_secondary_file(None)
    assert dvk.get_secondary_file() is None
    dvk.set_secondary_file("")
    assert dvk.get_secondary_file() is None
    # WRITE DVK
    dvk.set_dvk_file(join(test_dir, "media.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_secondary_file("media.png");
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING SECONDARY MEDIA FILE VALUE FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert abspath(join(read_dvk.get_secondary_file(), pardir)) == test_dir
    assert basename(read_dvk.get_secondary_file()) == "media.png"

def test_get_set_favorites():
    """
    Tests the get_favorites and set_favorites methods.
    """
    # TEST GETTING EMPTY FAVORITES LIST FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_favorites() == []
    # TEST GETTING AND SETTING FAVORITES
    favorites = ["Test", "artist", None, "artist"]
    dvk.set_favorites(favorites)
    assert len(dvk.get_favorites()) == 2
    assert dvk.get_favorites()[0] == "artist"
    assert dvk.get_favorites()[1] == "Test"
    # TEST GETTING FAVORITES FROM WEB TAGS IN OLD FORMAT
    tags = ["favorite:Other", "tag1", "tag2", "Favorite:thing", "Favorite:Test"]
    dvk.set_web_tags(tags)
    dvk.set_favorites(favorites)
    assert len(dvk.get_web_tags()) == 2
    assert dvk.get_web_tags()[0] == "tag1"
    assert dvk.get_web_tags()[1] == "tag2"
    assert len(dvk.get_favorites()) == 4
    assert dvk.get_favorites()[0] == "artist"
    assert dvk.get_favorites()[1] == "Other"
    assert dvk.get_favorites()[2] == "Test"
    assert dvk.get_favorites()[3] == "thing"
    tags = ["favorite:Other", "tag1", "tag2", "Favorite:thing", "Favorite:Test"]
    dvk.set_web_tags(tags)
    dvk.set_favorites(None)
    assert len(dvk.get_web_tags()) == 2
    assert dvk.get_web_tags()[0] == "tag1"
    assert dvk.get_web_tags()[1] == "tag2"
    assert len(dvk.get_favorites()) == 3
    assert dvk.get_favorites()[0] == "Other"
    assert dvk.get_favorites()[1] == "Test"
    assert dvk.get_favorites()[2] == "thing"
    # TEST SETTING INVALID FAVORITES
    dvk = Dvk()
    dvk.set_favorites(None)
    assert dvk.get_favorites() == []
    # WRITE DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "fav.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.set_web_tags(["Thing", "Favorite:Person"])
    dvk.set_favorites(["person2", "Other Artist"])
    dvk.write_dvk()
    # TEST READING FAVORITES FROM A DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_web_tags() == ["Thing"]
    assert len(read_dvk.get_favorites()) == 3
    assert read_dvk.get_favorites()[0] == "Other Artist"
    assert read_dvk.get_favorites()[1] == "Person"
    assert read_dvk.get_favorites()[2] == "person2"

def test_get_set_single():
    """
    Tests the is_single and set_single methods.
    """
    # TEST GETTING DEFAULT SINGLE VALUE FROM CONSTRUCTOR
    dvk = Dvk()
    assert not dvk.is_single()
    # TEST GETTING AND SETTING IS SINGLE
    dvk.set_single(True)
    assert dvk.is_single()
    dvk.set_single(False)
    assert not dvk.is_single()
    # TEST GETTING SINGLE FROM LEGACY
    dvk.set_web_tags(["DVK:Single", "tag", "tag2", "dvk:single"])
    dvk.set_single(False)
    assert dvk.is_single()
    assert dvk.get_web_tags() == ["tag", "tag2"]
    # TEST GIVING EMPTY VALUE WHEN SETTING SINGLE
    dvk = Dvk()
    dvk.set_single(True)
    dvk.set_single()
    assert not dvk.is_single()
    # WRITE DVKS
    test_dir = get_test_dir()
    dvk_single = Dvk()
    dvk_single.set_dvk_file(join(test_dir, "single.dvk"))
    dvk_single.set_dvk_id("id123")
    dvk_single.set_title("Title")
    dvk_single.set_artist("Artist")
    dvk_single.set_page_url("/url/")
    dvk_single.set_media_file("media.png")
    dvk_single.set_single(True)
    dvk_single.write_dvk()
    dvk_tag = Dvk()
    dvk_tag.set_dvk_file(join(test_dir, "tag.dvk"))
    dvk_tag.set_dvk_id("id123")
    dvk_tag.set_title("Title")
    dvk_tag.set_artist("Artist")
    dvk_tag.set_page_url("/url/")
    dvk_tag.set_media_file("media.png")
    dvk_tag.set_web_tags(["tag1", "Dvk:Single"])
    dvk_tag.write_dvk()
    dvk_none = Dvk()
    dvk_none.set_dvk_file(join(test_dir, "none.dvk"))
    dvk_none.set_dvk_id("id123")
    dvk_none.set_title("Title")
    dvk_none.set_artist("Artist")
    dvk_none.set_page_url("/url/")
    dvk_none.set_media_file("media.png")
    dvk_none.set_web_tags(["none"])
    dvk_none.write_dvk()
    # TEST READING SINGLE VALUE FROM DVK FILES
    read_dvk = Dvk(dvk_single.get_dvk_file())
    dvk_single = None
    assert read_dvk.is_single()
    read_dvk = Dvk(dvk_tag.get_dvk_file())
    dvk_tag = None
    assert read_dvk.get_web_tags() == ["tag1"]
    assert read_dvk.is_single()
    read_dvk = Dvk(dvk_none.get_dvk_file())
    dvk_none = None
    assert read_dvk.get_web_tags() == ["none"]
    assert not read_dvk.is_single()

def test_get_set_next_id():
    """
    Tests the get_next_id and set_next_id methods.
    """
    # Test getting default next ID from Dvk constructor
    dvk = Dvk()
    assert dvk.get_next_id() is None
    # Test getting and setting next ID
    dvk.set_next_id("TST123")
    assert dvk.get_next_id() == "TST123"
    dvk.set_next_id("non")
    assert dvk.get_next_id() == "non"
    dvk.set_next_id(None)
    assert dvk.get_next_id() is None
    dvk.set_next_id()
    assert dvk.get_next_id() is None
    # Write DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "next.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.set_next_id("NEW9876")
    dvk.write_dvk()
    # Test reading next ID from DVK file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert exists(read_dvk.get_dvk_file())
    assert read_dvk.get_next_id() == "NEW9876"

def test_get_set_prev_id():
    """
    Tests the get_prev_id and set_prev_id methods.
    """
    # Test getting default prev ID from Dvk constructor
    dvk = Dvk()
    assert dvk.get_prev_id() is None
    # Test getting and setting prev ID
    dvk.set_prev_id("TST123")
    assert dvk.get_prev_id() == "TST123"
    dvk.set_prev_id("non")
    assert dvk.get_prev_id() == "non"
    dvk.set_prev_id(None)
    assert dvk.get_prev_id() is None
    dvk.set_prev_id()
    assert dvk.get_prev_id() is None
    # Write DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "next.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.set_prev_id("NEW9876")
    dvk.write_dvk()
    # Test reading prev ID from DVK file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert exists(read_dvk.get_dvk_file())
    assert read_dvk.get_prev_id() == "NEW9876"

def test_set_first():
    """
    Tests the set_first method.
    """
    # Test setting Dvk to the first in a sequence
    dvk = Dvk()
    assert dvk.get_prev_id() is None
    dvk.set_first()
    assert dvk.get_prev_id() == "non"
    dvk.set_prev_id("ID123")
    assert dvk.get_prev_id() == "ID123"
    dvk.set_first()
    assert dvk.is_first()

def test_is_first():
    """
    Tests the is_first method.
    """
    # Test seeing if Dvk is the first in a sequence
    dvk = Dvk()
    assert not dvk.is_first()
    dvk.set_prev_id("NEW123")
    assert not dvk.is_first()
    dvk.set_first()
    assert dvk.is_first()
    dvk.set_prev_id("non")
    assert dvk.is_first()

def test_set_last():
    """
    Tests the set_last method.
    """
    # Test setting Dvk to the last in a sequence
    dvk = Dvk()
    assert dvk.get_next_id() is None
    dvk.set_last()
    assert dvk.get_next_id() == "non"
    dvk.set_next_id("ID123")
    assert dvk.get_next_id() == "ID123"
    dvk.set_last()
    assert dvk.is_last()

def test_is_last():
    """
    Tests the is_last method.
    """
    # Test seeing if Dvk is the last in a sequence
    dvk = Dvk()
    assert not dvk.is_last()
    dvk.set_next_id("NEW123")
    assert not dvk.is_last()
    dvk.set_last()
    assert dvk.is_last()
    dvk.set_next_id("non")
    assert dvk.is_last()

def test_get_set_sequence_title():
    """
    Tests the get_sequence_title and set_sequence_title methods.
    """
    # Test getting default sequence title from constructor.
    dvk = Dvk()
    assert dvk.get_sequence_title() == None
    # Test getting and setting the sequence title
    dvk.set_sequence_title("Title!")
    assert dvk.get_sequence_title() == "Title!"
    dvk.set_sequence_title(" other   ")
    assert dvk.get_sequence_title() == "other"
    dvk.set_sequence_title("    ")
    assert dvk.get_sequence_title() == None
    dvk.set_sequence_title("")
    assert dvk.get_sequence_title() == None
    # Write DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "seq_title.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.set_sequence_title("New Title")
    dvk.write_dvk()
    # Test reading sequence_title from DVK file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert exists(read_dvk.get_dvk_file())
    assert read_dvk.get_sequence_title() == "New Title"

def test_get_set_section_title():
    """
    Tests the get_section_title and set_section_title methods.
    """
    # Test getting default section title from constructor.
    dvk = Dvk()
    assert dvk.get_sequence_title() == None
    # Test getting and setting the section title
    dvk.set_section_title("Title!")
    assert dvk.get_section_title() == "Title!"
    dvk.set_section_title(" other   ")
    assert dvk.get_section_title() == "other"
    dvk.set_section_title("     ")
    assert dvk.get_section_title() == None
    dvk.set_section_title("")
    assert dvk.get_section_title() == None
    # Write DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "seq_title.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.set_section_title("New Title")
    dvk.write_dvk()
    # Test reading section title from DVK file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert exists(read_dvk.get_dvk_file())
    assert read_dvk.get_section_title() == "New Title"

def test_get_set_sequence_total():
    """
    Tests the get_sequence_total and set_sequence_total methods.
    """
    # Tests getting the default sequence total from the constructor
    dvk = Dvk()
    assert dvk.get_sequence_total() == 1
    # Tests getting and setting the sequence total
    dvk.set_sequence_total(45)
    assert dvk.get_sequence_total() == 45
    dvk.set_sequence_total(3)
    assert dvk.get_sequence_total() == 3
    dvk.set_sequence_total(1)
    assert dvk.get_sequence_total() == 1
    dvk.set_sequence_total(-2)
    assert dvk.get_sequence_total() == 1
    # Write DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "seq_total.dvk"))
    dvk.set_dvk_id("ID123")
    dvk.set_title("Sequence Total")
    dvk.set_artist("artist")
    dvk.set_page_url("URL")
    dvk.set_media_file("media.txt")
    dvk.set_sequence_total(71)
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # Test reading sequence total from DVK file
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert exists(read_dvk.get_dvk_file())
    assert read_dvk.get_sequence_total() == 71

def test_get_set_sequence_number():
    """
    Tests the get_sequence_number and set_sequence_number functions.
    """
    # Test getting default sequence number from constructor
    dvk = Dvk()
    assert dvk.get_sequence_number() == 0
    # Test getting and setting the sequence number
    dvk.set_sequence_total(20)
    dvk.set_sequence_number(12)
    assert dvk.get_sequence_number() == 12
    dvk.set_sequence_number(20)
    assert dvk.get_sequence_number() == 20
    dvk.set_sequence_number(-1)
    assert dvk.get_sequence_number() == 0
    dvk.set_sequence_number(21)
    assert dvk.get_sequence_number() == 0
    # Write DVK
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "seq_num.dvk"))
    dvk.set_dvk_id("ID123")
    dvk.set_title("Seq Num")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.txt")
    dvk.set_sequence_total(24)
    dvk.set_sequence_number(13)
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    assert dvk.get_sequence_number() == 13
    # Test reading sequence number from Dvk
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert exists(read_dvk.get_dvk_file())
    assert read_dvk.get_sequence_total() == 24
    assert read_dvk.get_sequence_number() == 13

def test_get_filename():
    """
    Tests the get_filename method.
    """
    # Test getting filename if duplicate filename doesn't exist
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_id("DVK1234")
    dvk.set_title("It's a Title!")
    dvk.set_artist("artist")
    assert dvk.get_filename(test_dir) == "It-s a Title"
    assert dvk.get_filename(test_dir, True) == "It-s a Title_S"
    # Test getting filename if duplicate filename exists
    file = abspath(join(test_dir, "Other Name.dvk"))
    with open(file, "w") as out_file:
        out_file.write("TEST")
    dvk.set_title("Other name")
    assert dvk.get_filename(test_dir) == "Other name - artist"
    assert dvk.get_filename(test_dir, True) == "Other name - artist_S"
    # Test getting filename if duplicate filename of same artist exists
    file = abspath(join(test_dir, "BLAH.dvk"))
    with open(file, "w") as out_file:
        out_file.write("TEST")
    file = abspath(join(test_dir, "Blah - artist.png"))
    with open(file, "w") as out_file:
        out_file.write("TEST")
    file = abspath(join(test_dir, "Blah - artist.txt"))
    with open(file, "w") as out_file:
        out_file.write("TEST")
    dvk.set_title("blah")
    dvk.set_direct_url("page/url.txt")
    dvk.set_secondary_url("page/url.png")
    assert dvk.get_filename(test_dir) == "blah_V236"
    assert dvk.get_filename(test_dir, True) == "blah_V236_S"
    # Test getting filename if part of a sequence
    dvk.set_title("Doesn't Matter")
    dvk.set_sequence_title("Seq!")
    dvk.set_sequence_total(250)
    dvk.set_sequence_number(13)
    assert dvk.get_filename(test_dir) == "013 Seq"
    dvk.set_sequence_total(9)
    dvk.set_sequence_number(1)
    dvk.set_section_title("Chapter 1")
    assert dvk.get_filename(test_dir, True) == "01 Seq - Chapter 1_S"
    # Test filename doesn't change due to conflict with itself
    dvk = Dvk()
    dvk.set_dvk_id("ID123")
    dvk.set_title("Self Overwrite")
    dvk.set_artist("Person")
    dvk.set_page_url("/url/")
    dvk.set_media_file("overwrite.txt")
    dvk.set_dvk_file(join(test_dir, dvk.get_filename(test_dir, False)) + ".dvk")
    assert basename(dvk.get_dvk_file()) == "Self Overwrite.dvk"
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    assert dvk.get_filename(test_dir, False) == "Self Overwrite"
    # Test getting filename with invalid parameters
    assert dvk.get_filename("/non/existant/") == ""
    assert dvk.get_filename(None) == ""
    dvk.set_dvk_id(None)
    assert dvk.get_filename(test_dir) == ""
    dvk.set_dvk_id("id123")
    dvk.set_title(None)
    assert dvk.get_filename(test_dir) == ""
    dvk.set_title("Title")
    dvk.set_artists()
    assert dvk.get_filename(test_dir) == ""

def test_rename_files():
    """
    Tests the rename_files method.
    """
    # CREATE TEST DVK WITHOUT EXISTING MEDIA FILES
    no_media_dvk = Dvk()
    test_dir = get_test_dir()
    no_media_dvk.set_dvk_file(join(test_dir, "rnm.dvk"))
    no_media_dvk.set_dvk_id("id123")
    no_media_dvk.set_title("Title")
    no_media_dvk.set_artist("Artist")
    no_media_dvk.set_page_url("/url/")
    no_media_dvk.set_media_file("file.txt")
    no_media_dvk.set_secondary_file("sec.png")
    no_media_dvk.write_dvk()
    assert exists(no_media_dvk.get_dvk_file())
    assert not exists(no_media_dvk.get_media_file())
    assert not exists(no_media_dvk.get_secondary_file())
    # TEST RENAMING DVK FILE
    no_media_dvk.rename_files("New", "New2")
    read_dvk = Dvk(no_media_dvk.get_dvk_file())
    no_media_dvk = None
    assert basename(read_dvk.get_dvk_file()) == "New.dvk"
    assert basename(read_dvk.get_media_file()) == "New.txt"
    assert basename(read_dvk.get_secondary_file()) == "New2.png"
    assert exists(read_dvk.get_dvk_file())
    assert not exists(read_dvk.get_media_file())
    assert not exists(read_dvk.get_secondary_file())
    # CREATE TEST DVK WITH EXISTING MEDIA FILE
    media_dvk = Dvk()
    media_dvk.set_dvk_file(join(test_dir, "rnm.dvk"))
    media_dvk.set_dvk_id("id123")
    media_dvk.set_title("Title")
    media_dvk.set_artist("Artist")
    media_dvk.set_page_url("/url/")
    media_dvk.set_media_file("media.png")
    with open(media_dvk.get_media_file(), "w") as out_file:
        out_file.write("TEST")
    media_dvk.write_dvk()
    assert exists(media_dvk.get_dvk_file())
    assert exists(media_dvk.get_media_file())
    assert media_dvk.get_secondary_file() is None
    # TEST RENAMING DVK FILE WITH MEDIA FILE
    media_dvk.rename_files("other", "other")
    read_dvk = Dvk(media_dvk.get_dvk_file())
    media_dvk = None
    assert basename(read_dvk.get_dvk_file()) == "other.dvk"
    assert basename(read_dvk.get_media_file()) == "other.png"
    assert read_dvk.get_secondary_file() is None
    assert exists(read_dvk.get_dvk_file())
    assert exists(read_dvk.get_media_file())
    # CREATE TEST DVK WITH EXISTING MEDIA AND SECONDARY FILES
    secondary_dvk = Dvk()
    secondary_dvk.set_dvk_file(join(test_dir, "rnm.dvk"))
    secondary_dvk.set_dvk_id("id123")
    secondary_dvk.set_title("Title")
    secondary_dvk.set_artist("Artist")
    secondary_dvk.set_page_url("/url/")
    secondary_dvk.set_media_file("media.pdf")
    with open(secondary_dvk.get_media_file(), "w") as out_file:
        out_file.write("TEST")
    secondary_dvk.set_secondary_file("secondary.jpg")
    with open(secondary_dvk.get_secondary_file(), "w") as out_file:
        out_file.write("SECONDARY")
    secondary_dvk.write_dvk()
    assert exists(secondary_dvk.get_dvk_file())
    assert exists(secondary_dvk.get_media_file())
    assert exists(secondary_dvk.get_secondary_file())
    # TEST RENAMING DVK FILE WITH MEDIA AND SECONDARY FILES
    secondary_dvk.rename_files("First", "Second")
    read_dvk = Dvk(secondary_dvk.get_dvk_file())
    secondary_dvk = None
    assert basename(read_dvk.get_dvk_file()) == "First.dvk"
    assert basename(read_dvk.get_media_file()) == "First.pdf"
    assert basename(read_dvk.get_secondary_file()) == "Second.jpg"
    assert exists(read_dvk.get_dvk_file())
    assert exists(read_dvk.get_media_file())
    assert exists(read_dvk.get_secondary_file())

def test_write_media():
    """
    Tests the write_media method
    """
    # CREATE DVK THAT CANNOT BE WRITTEN
    test_dir = get_test_dir()
    media_dvk = Dvk()
    media_dvk.set_dvk_file(join(test_dir, "inv.dvk"))
    media_dvk.set_dvk_id("id123")
    media_dvk.set_artist("artist")
    media_dvk.set_page_url("/url/")
    media_dvk.set_media_file("media.txt")
    media_dvk.set_direct_url("http://www.pythonscraping.com/img/gifts/img6.jpg")
    # TEST WRITE MEDIA WHEN URL IS VALID, BUT DVK CANNOT BE WRITTEN
    media_dvk.write_media()
    assert not exists(media_dvk.get_dvk_file())
    assert not exists(media_dvk.get_media_file())
    # TEST WRITE MEDIA WHEN DVK CAN BE WRITTEN, BUT URL IS INVALID
    media_dvk.set_title("Title")
    media_dvk.set_direct_url("!@#$%^")
    media_dvk.write_media(True)
    assert not exists(media_dvk.get_dvk_file())
    assert not exists(media_dvk.get_media_file())
    assert media_dvk.get_time() == "0000/00/00|00:00"
    # TEST VALID DIRECT MEDIA URL
    media_dvk.set_direct_url("http://www.pythonscraping.com/img/gifts/img6.jpg")
    media_dvk.write_media();
    assert exists(media_dvk.get_dvk_file())
    assert exists(media_dvk.get_media_file())
    assert basename(media_dvk.get_media_file()) == "media.jpg"
    assert stat(media_dvk.get_media_file()).st_size == 39785
    assert media_dvk.get_time() == "0000/00/00|00:00"
    # CREATE DVK WITH INVALID SECONDARY URL
    secondary_dvk = Dvk()
    secondary_dvk.set_dvk_file(join(test_dir, "inv2.dvk"))
    secondary_dvk.set_dvk_id("id123")
    secondary_dvk.set_title("Title")
    secondary_dvk.set_artist("artist")
    secondary_dvk.set_page_url("/url/")
    secondary_dvk.set_media_file("primary.jpg")
    secondary_dvk.set_direct_url("http://www.pythonscraping.com/img/gifts/img6.jpg")
    secondary_dvk.set_secondary_file("secondary.png")
    secondary_dvk.set_secondary_url("!@#$%^")
    # TEST WRITING MEDIA WITH VALID PRIMARY, BUT INVALID SECONDARY MEDIA URLS
    media_dvk.write_media();
    assert not exists(secondary_dvk.get_dvk_file())
    assert not exists(secondary_dvk.get_media_file())
    assert not exists(secondary_dvk.get_secondary_file())
    # TEST WRITING MEDIA WITH VALID PRIMARY AND SECONDARY MEDIA URLS
    secondary_dvk.set_secondary_url("http://www.pythonscraping.com/img/gifts/img4.jpg")
    secondary_dvk.write_media(True)
    assert exists(secondary_dvk.get_dvk_file())
    assert exists(secondary_dvk.get_media_file())
    assert exists(secondary_dvk.get_secondary_file())
    assert stat(secondary_dvk.get_media_file()).st_size == 39785
    assert stat(secondary_dvk.get_secondary_file()).st_size == 85007
    assert basename(secondary_dvk.get_secondary_file()) == "secondary.jpg"
    assert secondary_dvk.get_time() == "2014/08/04|00:49"
    assert secondary_dvk.get_direct_url() == "http://www.pythonscraping.com/img/gifts/img6.jpg"
    assert secondary_dvk.get_secondary_url() == "http://www.pythonscraping.com/img/gifts/img4.jpg"
    # TEST WRITING MEDIA WITH A DATA URI
    data_dvk = Dvk()
    data_dvk.set_dvk_file(join(test_dir, "data.dvk"))
    data_dvk.set_dvk_id("DAT125")
    data_dvk.set_title("Data")
    data_dvk.set_artist("Artist")
    data_dvk.set_page_url("/url/")
    data_dvk.set_media_file("primary_dot")
    data_dvk.set_secondary_file("secondary_dot")
    url = "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACN"\
                +"byblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4"\
                +"OHwAAAABJRU5ErkJggg=="
    data_dvk.set_direct_url(url)
    data_dvk.set_secondary_url(url)
    data_dvk.write_media()
    assert exists(data_dvk.get_dvk_file())
    assert exists(data_dvk.get_media_file())
    assert exists(data_dvk.get_secondary_file())
    assert stat(data_dvk.get_media_file()).st_size == 85
    assert stat(data_dvk.get_secondary_file()).st_size == 85
    assert basename(data_dvk.get_media_file()) == "primary_dot.png"
    assert basename(data_dvk.get_secondary_file()) == "secondary_dot.png"
    assert data_dvk.get_direct_url() is None
    assert data_dvk.get_secondary_url() is None

def test_delete_dvk():
    """
    Tests the delete_dvk method.
    """
    # Test deleting DVK file with no media
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "dvk.dvk"))
    dvk.set_dvk_id("ID123")
    dvk.set_title("Title")
    dvk.set_artist("Artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("Non-Existant.png")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    dvk.delete_dvk()
    assert not exists(dvk.get_dvk_file())
    assert not exists(dvk.get_media_file())
    assert dvk.get_secondary_file() is None
    # Test deleting DVK file with media
    dvk.set_media_file("media.txt")
    with open(dvk.get_media_file(), "w") as out_file:
        out_file.write("Main File")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    assert exists(dvk.get_media_file())
    dvk.delete_dvk()
    assert not exists(dvk.get_dvk_file())
    assert not exists(dvk.get_media_file())
    assert dvk.get_secondary_file() is None
    # Test deleting DVK file with secondary file
    dvk.set_secondary_file("secondary.png")
    with open(dvk.get_media_file(), "w") as out_file:
        out_file.write("Main File")
    with open(dvk.get_secondary_file(), "w") as out_file:
        out_file.write("Secondary")
        dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    assert exists(dvk.get_media_file())
    assert exists(dvk.get_secondary_file())
    dvk.delete_dvk()
    assert not exists(dvk.get_dvk_file())
    assert not exists(dvk.get_media_file())
    assert not exists(dvk.get_secondary_file())
    # Test deleting DVK doesn't fail when file is invalid
    dvk.set_dvk_file("/non-existant/asdf")
    dvk.set_media_file("asdf")
    dvk.set_secondary_file("asdf")
    dvk.delete_dvk()
    assert not exists(dvk.get_dvk_file())
    assert dvk.get_media_file() is None
    assert dvk.get_secondary_file() is None

def test_move_dvk():
    """
    Tests the move_dvk method.
    """
    # CREATE TEST FILES
    test_dir = get_test_dir()
    sub = abspath(join(test_dir, "sub"))
    mkdir(sub)
    no_media = Dvk()
    no_media.set_dvk_file(join(test_dir, "no_media.dvk"))
    no_media.set_dvk_id("NM123")
    no_media.set_title("No Media")
    no_media.set_artist("artist")
    no_media.set_page_url("/url/")
    no_media.set_media_file("no_media.png")
    no_media.write_dvk()
    main_dvk = Dvk()
    main_dvk.set_dvk_file(join(test_dir, "main.dvk"))
    main_dvk.set_dvk_id("ID234")
    main_dvk.set_title("Main")
    main_dvk.set_artist("artist")
    main_dvk.set_page_url("/url/")
    main_dvk.set_media_file("main.txt")
    with open(main_dvk.get_media_file(), "w") as out_file:
        out_file.write("Main test")
    main_dvk.write_dvk()
    second = Dvk()
    second.set_dvk_file(join(test_dir, "second.dvk"))
    second.set_dvk_id("SEC246")
    second.set_title("Second")
    second.set_artist("artist")
    second.set_page_url("/url/")
    second.set_media_file("second.txt")
    second.set_secondary_file("second2.txt")
    with open(second.get_media_file(), "w") as out_file:
        out_file.write("File")
    with open(second.get_secondary_file(), "w") as out_file:
        out_file.write("Secondary Test")
    second.write_dvk()
    # TEST MOVING DVK FILE WITH NO MEDIA
    file = no_media.get_dvk_file()
    assert exists(file)
    no_media.move_dvk(sub)
    assert not exists(file)
    assert abspath(join(sub, "no_media.dvk")) == no_media.get_dvk_file()
    assert exists(no_media.get_dvk_file())
    assert no_media.get_title() == "No Media"
    # TEST MOVING DVK WITH MEDIA
    assert exists(main_dvk.get_dvk_file())
    file = main_dvk.get_media_file()
    assert exists(file)
    main_dvk.move_dvk(sub)
    assert not exists(file)
    assert abspath(join(sub, "main.dvk")) == main_dvk.get_dvk_file()
    assert exists(main_dvk.get_dvk_file())
    assert abspath(join(sub, "main.txt")) == main_dvk.get_media_file()
    assert exists(main_dvk.get_media_file())
    with open(main_dvk.get_media_file()) as f:
        contents = f.read()
    assert contents == "Main test"
    assert main_dvk.get_title() == "Main"
    # TEST MOVING DVK WITH SECONDARY MEDIA
    assert exists(second.get_dvk_file())
    assert exists(second.get_media_file())
    file = second.get_secondary_file()
    assert exists(file)
    second.move_dvk(sub)
    assert not exists(file)
    assert abspath(join(sub, "second.dvk")) == second.get_dvk_file()
    assert exists(second.get_dvk_file())
    assert abspath(join(sub, "second.txt")) == second.get_media_file()
    assert exists(second.get_media_file())
    assert abspath(join(sub, "second2.txt")) == second.get_secondary_file()
    assert exists(second.get_secondary_file())
    with open(second.get_media_file()) as f:
            contents = f.read()
    assert contents == "File"
    with open(second.get_secondary_file()) as f:
            contents = f.read()
    assert contents == "Secondary Test"
    assert second.get_title() == "Second"
    # TEST MOVING TO INVALID DIRECTORIES
    main_dvk.move_dvk(None)
    assert abspath(join(sub, "main.dvk")) == main_dvk.get_dvk_file()
    main_dvk.move_dvk("/non-existant/dir/")
    assert abspath(join(sub, "main.dvk")) == main_dvk.get_dvk_file()

def test_update_extensions():
    """
    Tests the update_extensions method.
    """
    # CREATE TEST MEDIA FILES
    test_dir = get_test_dir()
    image_file = abspath(join(test_dir, "image.pdf"))
    download("http://www.pythonscraping.com/img/gifts/img6.jpg", image_file)
    text_file = abspath(join(test_dir, "text.txt"))
    with open(text_file, "w") as out_file:
        out_file.write("TEST File")
    assert exists(image_file)
    assert exists(text_file)
    # CREATE DVK WITH IMPROPER EXTENSIONS FOR LINKED MEDIA FILES
    dvk = Dvk()
    dvk.set_dvk_file(join(test_dir, "ext.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("image.pdf")
    dvk.set_secondary_file("text.txt")
    dvk.write_dvk()
    # TEST THAT FILES EXIST IN ORIGINAL FORMAT
    assert exists(dvk.get_dvk_file())
    assert exists(dvk.get_media_file())
    assert exists(dvk.get_secondary_file())
    assert basename(dvk.get_media_file()) == "image.pdf"
    assert basename(dvk.get_secondary_file()) == "text.txt"
    # TEST UPDATING EXTENSIONS OF LINKED MEDIA
    dvk.update_extensions()
    assert exists(dvk.get_dvk_file())
    assert exists(dvk.get_media_file())
    assert exists(dvk.get_secondary_file())
    assert basename(dvk.get_media_file()) == "image.jpg"
    assert basename(dvk.get_secondary_file()) == "text.txt"

def all_tests():
    """
    Runs all tests for the Dvk class.
    """
    test_can_write()
    test_get_set_dvk_file()
    test_get_set_dvk_id()
    test_get_set_title()
    test_get_set_artists()
    test_set_time_int()
    test_get_set_time()
    test_get_set_web_tags()
    test_get_set_description()
    test_get_set_page_url()
    test_get_set_direct_url()
    test_get_set_secondary_url()
    test_get_set_media_file()
    test_get_set_secondary_file()
    test_get_set_favorites()
    test_get_set_single()
    test_get_set_next_id()
    test_get_set_prev_id()
    test_is_first()
    test_is_last()
    test_set_first()
    test_set_last()
    test_get_set_sequence_title()
    test_get_set_section_title()
    test_get_set_sequence_total()
    test_get_set_sequence_number()
    test_get_filename()
    test_rename_files()
    test_delete_dvk()
    test_move_dvk()
    test_write_media()
    test_update_extensions()
