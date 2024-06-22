import os.path
import unittest
from pathlib import Path

import pytest

import wanda.utils.common_utils as common
import wanda.utils.image_utils as image
from sources.extractor import *


# These tests should be compatible with ci runners
class SimpleTest(unittest.TestCase):
    good_search = "nature"
    bad_search = "foobarxyzzy"
    artstation_cdn = "https://cdn(.).artstation.com/"

    def assert_starts_with(self, response, url):
        self.assertTrue(response.startswith(url), response)

    def assertNotNone(self, response, url):
        self.assertIsNotNone(re.search(url, response), response)

    def test_conn_test(self):
        self.assertTrue(common.is_connected())

    def test_local(self):
        self.assertRaises(SystemExit, local, None)
        self.assertRaises(SystemExit, local, "")

    def test_wallhaven(self):
        url = "https://w.wallhaven.cc/full/"

        response = wallhaven(None)
        self.assert_starts_with(response, url)

        response = wallhaven("")
        self.assert_starts_with(response, url)

        response = wallhaven(self.good_search)
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, wallhaven, self.bad_search)

    def test_reddit(self):
        url = "https://i.redd.it/"

        self.assertIn("wallpaper", suggested_subreddits())

        response = reddit(search=None)
        self.assert_starts_with(response, url)

        response = reddit("")
        self.assert_starts_with(response, url)

        response = reddit(self.good_search)
        self.assertNotNone(response, "^https?://")

        response = reddit("wallpaper@halflife")
        self.assertNotNone(response, "^https?://")

        self.assertRaises(SystemExit, reddit, search=self.bad_search)

    def test_imgur(self):
        url = "https://rimgo.eu.projectsegfau.lt"

        self.assertRaises(SystemExit, imgur, None)

        self.assertRaises(SystemExit, imgur, "")

        response = imgur(search="jmVC8")
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, imgur, self.bad_search)

    def test_fourchan(self):
        url = "^(https?://archive-media.palanq.win/|https?://i.4cdn.org)"

        response = fourchan(None)
        self.assertNotNone(response, url)

        response = fourchan("")
        self.assertNotNone(response, url)

        response = fourchan("phone")
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, fourchan, self.bad_search)

    def test_artstation_any(self):
        url = self.artstation_cdn
        response = artstation_any(None)
        self.assertNotNone(response, url)

        response = artstation_any("")
        self.assertNotNone(response, url)

        response = artstation_any(self.good_search)
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, artstation_any, self.bad_search)

    def test_artstation_prints(self):
        url = self.artstation_cdn
        response = artstation_prints(None)
        self.assertNotNone(response, url)

        response = artstation_prints("")
        self.assertNotNone(response, url)

        response = artstation_prints(self.good_search)
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, artstation_prints, self.bad_search)

    def test_artstation_artist(self):
        url = self.artstation_cdn

        self.assertRaises(SystemExit, artstation_artist, None)
        self.assertRaises(SystemExit, artstation_artist, "")
        self.assertRaises(SystemExit, artstation_artist, self.bad_search)

        response = artstation_artist("tohad")
        self.assertNotNone(response, url)

    def test_earthview(self):
        response = earthview(None)
        self.assertIsNotNone(response)

    def test_musicbrainz(self):
        self.assertNotIsInstance(musicbrainz, str, "NoArtistFoo-NoAlbumBar")

        musicbrainz("Coldplay-Parachutes")

    def test_waifuim(self):
        url = "https://cdn.waifu.im/"

        response = waifuim(None)
        self.assert_starts_with(response, url)

        response = waifuim("")
        self.assert_starts_with(response, url)

        response = waifuim("uniform")
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, waifuim, self.bad_search)


# These tests would need actual device
@pytest.mark.skip
class AdvancedTest(unittest.TestCase):
    good_search = "nature"

    def test_size(self):
        self.assertEqual(type(size()), tuple)

    def test_set_local(self):
        folder = f"{str(Path.home())}/wanda"
        path = get_dl_path()
        path = common.download(path, "https://i.imgur.com/bBNy18H.jpeg")
        self.assertTrue(os.path.exists(path))
        image.set_wp(local(folder), True, True)

    def test_set_wallhaven(self):
        image.set_wp(wallhaven(self.good_search), True, True)

    def test_set_artstation(self):
        image.set_wp(artstation_artist("tohad"), True, True)

        image.set_wp(artstation_prints(self.good_search), True, True)

        image.set_wp(artstation_any(self.good_search), True, True)

    def test_set_reddit(self):
        image.set_wp(reddit(self.good_search), True, True)

        image.set_wp(reddit("wallpaper@halflife"), True, True)

    @staticmethod
    def test_set_earthview():
        image.set_wp(earthview(""), True, True)

    @staticmethod
    def test_set_waifuim():
        image.set_wp(waifuim("uniform"), True, True)

    @staticmethod
    def test_set_fourchan():
        image.set_wp(fourchan("mobile"), True, True)


if __name__ == "__main__":
    unittest.main()
