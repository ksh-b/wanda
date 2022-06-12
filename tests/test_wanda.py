import os.path
import re
import unittest
from pathlib import Path

import pytest

from wanda import wanda


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
        self.assertTrue(wanda.is_connected())

    def test_local(self):
        self.assertRaises(SystemExit, wanda.local, None)
        self.assertRaises(SystemExit, wanda.local, "")

    def test_wallhaven(self):
        url = "https://w.wallhaven.cc/full/"

        response = wanda.wallhaven(None)
        self.assert_starts_with(response, url)

        response = wanda.wallhaven("")
        self.assert_starts_with(response, url)

        response = wanda.wallhaven(self.good_search)
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, wanda.wallhaven, self.bad_search)

    def test_unsplash(self):
        url = "https://images.unsplash.com/photo-"

        response = wanda.unsplash(None)
        self.assert_starts_with(response, url)

        response = wanda.unsplash("")
        self.assert_starts_with(response, url)

        response = wanda.unsplash(self.good_search)
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, wanda.unsplash, self.bad_search)

    def test_reddit(self):
        url = "https://i.redd.it/"

        self.assertIn("wallpaper", wanda.suggested_subreddits())

        response = wanda.reddit(search=None)
        self.assert_starts_with(response, url)

        response = wanda.reddit("")
        self.assert_starts_with(response, url)

        response = wanda.reddit(self.good_search)
        self.assertNotNone(response, "^https?://")

        response = wanda.reddit("wallpaper@halflife")
        self.assertNotNone(response, "^https?://")

        self.assertRaises(SystemExit, wanda.reddit, search=self.bad_search)

    def test_imgur(self):
        url = "https://rimgo.pussthecat.org/"

        response = wanda.imgur(None)
        self.assert_starts_with(response, url)

        response = wanda.imgur("")
        self.assert_starts_with(response, url)

        response = wanda.imgur("jmVC8")
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, wanda.imgur, self.bad_search)

    def test_fourchan(self):
        url = "^(https?://s1.alice.al|https?://i.4cdn.org)"

        response = wanda.fourchan(None)
        self.assertNotNone(response, url)

        response = wanda.fourchan("")
        self.assertNotNone(response, url)

        response = wanda.fourchan("phone")
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, wanda.fourchan, self.bad_search)

    def test_fivehundredpx(self):
        url = "https://drscdn.500px.org/photo/"

        response = wanda.fivehundredpx(None)
        self.assertTrue(response.startswith(url))

        response = wanda.fivehundredpx("")
        self.assert_starts_with(response, url)

        response = wanda.fivehundredpx(self.good_search)
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, wanda.fivehundredpx, self.bad_search)

    def test_artstation_any(self):
        url = self.artstation_cdn
        response = wanda.artstation_any(None)
        self.assertNotNone(response, url)

        response = wanda.artstation_any("")
        self.assertNotNone(response, url)

        response = wanda.artstation_any(self.good_search)
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, wanda.artstation_any, self.bad_search)

    def test_artstation_prints(self):
        url = self.artstation_cdn
        response = wanda.artstation_prints(None)
        self.assertNotNone(response, url)

        response = wanda.artstation_prints("")
        self.assertNotNone(response, url)

        response = wanda.artstation_prints(self.good_search)
        self.assertNotNone(response, url)

        self.assertRaises(SystemExit, wanda.artstation_prints, self.bad_search)

    def test_artstation_artist(self):
        url = self.artstation_cdn

        self.assertRaises(SystemExit, wanda.artstation_artist, None)
        self.assertRaises(SystemExit, wanda.artstation_artist, "")
        self.assertRaises(SystemExit, wanda.artstation_artist, self.bad_search)

        response = wanda.artstation_artist("tohad")
        self.assertNotNone(response, url)

    def test_earthview(self):
        url = "https://www.gstatic.com/prettyearth/assets/full/"
        response = wanda.earthview(None)
        self.assert_starts_with(response, url)

    def test_waifuim(self):
        url = "https://cdn.waifu.im/"

        response = wanda.waifuim(None)
        self.assert_starts_with(response, url)

        response = wanda.waifuim("")
        self.assert_starts_with(response, url)

        response = wanda.waifuim("uniform")
        self.assert_starts_with(response, url)

        self.assertRaises(SystemExit, wanda.waifuim, self.bad_search)


# These tests would need actual device
@pytest.mark.skip
class AdvancedTest(unittest.TestCase):
    good_search = "nature"

    def test_size(self):
        self.assertEqual(type(wanda.size()), tuple)

    def test_set_local(self):
        folder = f"{str(Path.home())}/wanda"
        path = wanda.get_dl_path()
        path = wanda.download(path, "https://i.imgur.com/bBNy18H.jpeg")
        self.assertTrue(os.path.exists(path))
        wanda.set_wp(wanda.local(folder), True, True)

    def test_set_wallhaven(self):
        wanda.set_wp(wanda.wallhaven(self.good_search), True, True)

    def test_set_artstation(self):
        wanda.set_wp(wanda.artstation_artist("tohad"), True, True)

        wanda.set_wp(wanda.artstation_prints(self.good_search), True, True)

        wanda.set_wp(wanda.artstation_any(self.good_search), True, True)

    def test_set_reddit(self):
        wanda.set_wp(wanda.reddit(self.good_search), True, True)

        wanda.set_wp(wanda.reddit("wallpaper@halflife"), True, True)

    def test_set_unsplash(self):
        wanda.set_wp(wanda.unsplash(self.good_search), True, True)

    @staticmethod
    def test_set_imgur():
        wanda.set_wp(wanda.imgur("jmVC8"), True, True)

    @staticmethod
    def test_set_earthview():
        wanda.set_wp(wanda.earthview(""), True, True)

    @staticmethod
    def test_set_waifuim():
        wanda.set_wp(wanda.waifuim("uniform"), True, True)

    @staticmethod
    def test_set_fourchan():
        wanda.set_wp(wanda.fourchan("mobile"), True, True)

    def test_set_fivehundredpx(self):
        wanda.set_wp(wanda.fivehundredpx(self.good_search), True, True)


if __name__ == "__main__":
    unittest.main()
