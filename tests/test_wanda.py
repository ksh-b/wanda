import os.path
import re
import unittest
from pathlib import Path

import pytest

import wanda.sources as source
import wanda.utils.common_utils as common
import wanda.utils.image_utils as image


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
        self.assertRaises(SystemExit, source.local, None)
        self.assertRaises(SystemExit, source.local, "")

    def test_wallhaven(self):
        url = "https://w.wallhaven.cc/full/"

        response = source.wallhaven(None)
        self.assert_starts_with(response, url)

        response = source.wallhaven("")
        self.assert_starts_with(response, url)

        response = source.wallhaven(self.good_search)
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, source.wallhaven, self.bad_search)

    def test_reddit(self):
        url = "https://i.redd.it/"

        self.assertIn("wallpaper", source.suggested_subreddits())

        response = source.reddit(search=None)
        self.assert_starts_with(response, url)

        response = source.reddit("")
        self.assert_starts_with(response, url)

        response = source.reddit(self.good_search)
        self.assertNotNone(response, "^https?://")

        response = source.reddit("wallpaper@halflife")
        self.assertNotNone(response, "^https?://")

        self.assertRaises(SystemExit, source.reddit, search=self.bad_search)

    def test_imgur(self):
        url = "https://rimgo.projectsegfau.lt/"

        self.assertRaises(SystemExit, source.imgur, None)

        self.assertRaises(SystemExit, source.imgur, "")

        response = source.imgur(search="jmVC8")
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, source.imgur, self.bad_search)

    def test_fourchan(self):
        url = "^(https?://archive-media.palanq.win/|https?://i.4cdn.org)"

        response = source.fourchan(None)
        self.assertNotNone(response, url)

        response = source.fourchan("")
        self.assertNotNone(response, url)

        response = source.fourchan("phone")
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, source.fourchan, self.bad_search)

    def test_artstation_any(self):
        url = self.artstation_cdn
        response = source.artstation_any(None)
        self.assertNotNone(response, url)

        response = source.artstation_any("")
        self.assertNotNone(response, url)

        response = source.artstation_any(self.good_search)
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, source.artstation_any, self.bad_search)

    def test_artstation_prints(self):
        url = self.artstation_cdn
        response = source.artstation_prints(None)
        self.assertNotNone(response, url)

        response = source.artstation_prints("")
        self.assertNotNone(response, url)

        response = source.artstation_prints(self.good_search)
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, source.artstation_prints, self.bad_search)

    def test_artstation_artist(self):
        url = self.artstation_cdn

        self.assertRaises(SystemExit, source.artstation_artist, None)
        self.assertRaises(SystemExit, source.artstation_artist, "")
        self.assertRaises(SystemExit, source.artstation_artist, self.bad_search)

        response = source.artstation_artist("tohad")
        self.assertNotNone(response, url)

    def test_earthview(self):
        url = "https://www.gstatic.com/prettyearth/assets/full/"
        response = source.earthview(None)
        self.assert_starts_with(response, url)

    def test_musicbrainz(self):
        self.assertNotIsInstance(source.musicbrainz, str, "NoArtistFoo-NoAlbumBar")

        source.musicbrainz("Coldplay-Parachutes")

    def test_waifuim(self):
        url = "https://cdn.waifu.im/"

        response = source.waifuim(None)
        self.assert_starts_with(response, url)

        response = source.waifuim("")
        self.assert_starts_with(response, url)

        response = source.waifuim("uniform")
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, source.waifuim, self.bad_search)


# These tests would need actual device
@pytest.mark.skip
class AdvancedTest(unittest.TestCase):
    good_search = "nature"

    def test_size(self):
        self.assertEqual(type(source.size()), tuple)

    def test_set_local(self):
        folder = f"{str(Path.home())}/wanda"
        path = source.get_dl_path()
        path = source.download(path, "https://i.imgur.com/bBNy18H.jpeg")
        self.assertTrue(os.path.exists(path))
        image.set_wp(source.local(folder), True, True)

    def test_set_wallhaven(self):
        image.set_wp(source.wallhaven(self.good_search), True, True)

    def test_set_artstation(self):
        image.set_wp(source.artstation_artist("tohad"), True, True)

        image.set_wp(source.artstation_prints(self.good_search), True, True)

        image.set_wp(source.artstation_any(self.good_search), True, True)

    def test_set_reddit(self):
        image.set_wp(source.reddit(self.good_search), True, True)

        image.set_wp(source.reddit("wallpaper@halflife"), True, True)

    @staticmethod
    def test_set_imgur():
        image.set_wp(source.imgur("jmVC8"), True, True)

    @staticmethod
    def test_set_earthview():
        image.set_wp(source.earthview(""), True, True)

    @staticmethod
    def test_set_waifuim():
        image.set_wp(source.waifuim("uniform"), True, True)

    @staticmethod
    def test_set_fourchan():
        image.set_wp(source.fourchan("mobile"), True, True)

    def test_set_fivehundredpx(self):
        image.set_wp(source.fivehundredpx(self.good_search), True, True)


if __name__ == "__main__":
    unittest.main()
