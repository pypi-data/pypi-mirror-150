#!/usr/bin/env python3

from dvk_archive.main.processing.string_processing import pad_num
from dvk_archive.main.processing.string_processing import get_filename
from dvk_archive.main.processing.string_processing import truncate_string
from dvk_archive.main.processing.string_processing import get_url_directory
from dvk_archive.main.processing.string_processing import truncate_path

def test_pad_num():
    """
    Tests the pad_num function.
    """
    # Test padding out number strings with zeros
    assert pad_num("2F", 2) == "2F"
    assert pad_num("2E", 5) == "0002E"
    assert pad_num("10F", 2) == "10F"
    # Test using invalid values
    assert pad_num("A3", 0) == ""
    assert pad_num("F3", -1) == ""
    assert pad_num(None, 2) == ""

def test_get_filename():
    """
    Tests the get_filename function
    """
    # Test getting file friendly names
    assert get_filename("This & That 2") == "This - That 2"
    assert get_filename("! !end filler!??  ") == "end filler"
    assert get_filename("thing--stuff  @*-   bleh") == "thing-stuff - bleh"
    assert get_filename("a% - !b @  ??c") == "a - b - c"
    assert get_filename("Test String", 5) == "Test"
    assert get_filename("Test String", -1) == "Test String"
    # Test converting from non-standard latin characters
    assert get_filename("ÀÁÂÃÄÅ") == "AAAAAA"
    assert get_filename("ÈÉÊË") == "EEEE"
    assert get_filename("ÌÍÎÏ") == "IIII"
    assert get_filename("ÑÒÓÔÕÖ") == "NOOOOO"
    assert get_filename("ÙÚÛÜÝ") == "UUUUY"
    assert get_filename("àáâãäå") == "aaaaaa"
    assert get_filename("èéêë") == "eeee"
    assert get_filename("ìíîï") == "iiii"
    assert get_filename("ñòóôõö") == "nooooo"
    assert get_filename("ùúûüýÿ") == "uuuuyy"
    # Test getting filenames with no length
    assert get_filename("") == "0"
    assert get_filename("$") == "0"
    # Test getting filename when given string is invalid
    assert get_filename(None) == "0"

def test_truncate_string():
    """
    Tests the truncate_string function.
    """
    # TEST TRUNCATING STRINGS
    assert truncate_string("blah", 0) == ""
    assert truncate_string("bleh", -1) == ""
    assert truncate_string("bleh", 4) == "bleh"
    assert truncate_string("words", 3) == "wor"
    assert truncate_string("word-stuff", 5) == "word"
    assert truncate_string("words n stuff", 4) == "stu"
    assert truncate_string("word stuff", 5) == "word"
    assert truncate_string("words-n-stuff", 4) == "stu"
    in_str = "This string is way too long to work as a title p25"
    out_str = "This string is way too long to work p25";
    assert truncate_string(in_str, 40) == out_str
    in_str = "HereIsA LongThingWithoutManySpacesWhichCanBeShort"
    out_str = "HereIsA WithoutManySpacesWhichCanBeShort"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisMessageIsAbsolutelyWayToLongToWorkFor-"
    in_str = in_str + "AnyThingAtAllSoLetsSeeHowThisWillFareISuppose"
    out_str = "ThisMessageIsAbsolutelyWayToLongToWorkFo"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisMessageIsAbsolutelyWayToLongToWorkForAnyThing-"
    in_str = in_str + "AtAllSoLetsSeeHowThisWillFareISuppose"
    out_str = "Th-AtAllSoLetsSeeHowThisWillFareISuppose"
    assert truncate_string(in_str, 40) == out_str
    in_str = "ThisLongTitleHasNoSpacesAtAllSoItHasAMiddleBreak"
    out_str = "ThisLongTitleHasAtAllSoItHasAMiddleBreak"
    assert truncate_string(in_str, 40) == out_str
    # TEST WHEN GIVEN STRING IS INVALID
    assert truncate_string(None, 2) == ""

def test_get_url_directory():
    """
    Tests the get_url_directory function.
    """
    # Test getting last directory
    assert get_url_directory("a/b/c/url.txt") == "url.txt"
    assert get_url_directory("/url//test") == "test"
    # Test getting directory with ending slash
    assert get_url_directory("test/") == "test"
    assert get_url_directory("/other/thing//") == "thing"
    assert get_url_directory("///") == ""
    # Test getting directory from invalid URL
    assert get_url_directory("") == ""
    assert get_url_directory(None) == ""

def test_truncate_path():
    """
    Tests the truncate_path function.
    """
    # Test truncating paths
    assert truncate_path("/path/", "/path/file.txt") == ".../file.txt"
    assert truncate_path("main", "main/path.png") == ".../path.png"
    assert truncate_path("/a/b/c/", "/a/b/c/thing.jpg") == ".../thing.jpg"
    # Test truncating path if file is not in the given directory
    assert truncate_path("/a/b/c/", "/unrelated/f.txt") == "/unrelated/f.txt"
    assert truncate_path("/a/", "/A/file.png") == "/A/file.png"
    # Test if file and parent path are exactly the same
    assert truncate_path("/a/b/c", "/a/b/c") == "/a/b/c"
    # Test when the parent path is invalid
    assert truncate_path(None, "/other/file.txt") == "/other/file.txt"
    # Test when the file is invalid
    assert truncate_path("/path/", None) == ""
    assert truncate_path(None, None) == ""

def all_tests():
    """
    Runs all test for the string_processing module.
    """
    test_pad_num()
    test_get_filename()
    test_truncate_string()
    test_get_url_directory()
    test_truncate_path()
