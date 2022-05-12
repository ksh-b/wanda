import time
import re
from wanda import wanda

import unittest


class SimpleTest(unittest.TestCase):
    good_search = "nature"
    bad_search = "foobarxyzzy"
    bed_time = 3
    artstation_cdn = "https://cdn(.).artstation.com/"

    def test_conn_test(self):
        self.assertTrue(wanda.is_connected())

    def test_size(self):
        import re
        self.assertIsNotNone(re.search("^[0-9]+x[0-9]+", wanda.size()))

    def test_wallhaven(self):
        url = "https://w.wallhaven.cc/full/"
        self.assertTrue(wanda.wallhaven(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.wallhaven("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.wallhaven(self.good_search).startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.wallhaven, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.wallhaven(self.good_search), True, True)

    def test_unsplash(self):
        url = "https://images.unsplash.com/photo-"
        self.assertTrue(wanda.unsplash(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.unsplash("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.unsplash(self.good_search).startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.unsplash, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.unsplash(self.good_search), True, True)

    def test_reddit(self):
        url = "https://i.redd.it/"
        self.assertTrue(wanda.reddit(search=None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.reddit("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.reddit(self.good_search).startswith("https://"))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.reddit("wallpaper@halflife").startswith("https://"))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.reddit, search=self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.reddit(self.good_search), True, True)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.reddit("wallpaper@halflife"), True, True)

    def test_imgur(self):
        url = "https://rimgo.pussthecat.org/"
        self.assertTrue(wanda.imgur(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.imgur("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.imgur("jmVC8").startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.imgur, self.bad_search)
        time.sleep(self.bed_time)

        wanda.set_wp(wanda.imgur("jmVC8"), True, True)

    def test_fourchan(self):
        url = "https://s1.alice.al/"
        self.assertTrue(wanda.fourchan(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.fourchan("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.fourchan("phone").startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.fourchan, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.fourchan(self.good_search), True, True)

    def test_fivehundredpx(self):
        url = "https://drscdn.500px.org/photo/"
        self.assertTrue(wanda.fivehundredpx(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.fivehundredpx("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.fivehundredpx(self.good_search).startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.fivehundredpx, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.fivehundredpx(self.good_search), True, True)

    def test_artstation_any(self):
        url = self.artstation_cdn
        a = wanda.artstation_any(None)
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        a = wanda.artstation_any("")
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        a = wanda.artstation_any(self.good_search)
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        self.assertRaises(SystemExit, wanda.artstation_any, self.bad_search)
        time.sleep(self.bed_time)

        wanda.set_wp(wanda.artstation_any(self.good_search), True, True)

    def test_artstation_prints(self):
        url = self.artstation_cdn
        a = wanda.artstation_prints(None)
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        a = wanda.artstation_prints("")
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        a = wanda.artstation_prints(self.good_search)
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        self.assertRaises(SystemExit, wanda.artstation_prints, self.bad_search)
        time.sleep(self.bed_time)

        wanda.set_wp(wanda.artstation_prints(self.good_search), True, True)

    def test_artstation_artist(self):
        url = self.artstation_cdn
        a = wanda.artstation_artist(None)
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        a = wanda.artstation_artist("")
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        a = wanda.artstation_artist("tohad")
        self.assertIsNotNone(re.search(url, a), a)
        time.sleep(self.bed_time)

        self.assertRaises(SystemExit, wanda.artstation_artist, self.bad_search)
        time.sleep(self.bed_time)

        wanda.set_wp(wanda.artstation_artist("tohad"), True, True)

    def test_earthview(self):
        url = "https://www.gstatic.com/prettyearth/assets/full/"
        self.assertTrue(wanda.earthview(None).startswith(url))
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.earthview(""), True, True)

    def test_local(self):
        url = input("Enter valid image directory:")
        self.assertRaises(SystemExit, wanda.local, None)
        self.assertRaises(SystemExit, wanda.local, "")
        wanda.set_wp(wanda.local(url), True, True)

    def test_waifuim(self):
        url = "https://cdn.waifu.im/"
        self.assertTrue(wanda.waifuim(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.waifuim("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.waifuim("uniform").startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.waifuim, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.waifuim("uniform"), True, True)


if __name__ == '__main__':
    unittest.main()
