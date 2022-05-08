import time
from wanda import wanda

import unittest


class SimpleTest(unittest.TestCase):
    good_search = "nature"
    bad_search = "foobarxyzzy"
    bed_time = 3

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
        self.assertTrue(wanda.reddit(search="").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.reddit(search=self.good_search).startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.reddit, search=self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.reddit(self.good_search), True, True)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.reddit("wallpaper@halflife"), True, True)

    def test_imsea(self):
        url = ".mm.bing.net/th?id="
        self.assertTrue(url in wanda.imsea(None))
        time.sleep(self.bed_time)
        self.assertTrue(url in wanda.imsea(""))
        time.sleep(self.bed_time)
        self.assertTrue(url in wanda.imsea(self.good_search))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.imsea, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.imsea(self.good_search), True, True)

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
        wanda.set_wp(wanda.imgur(self.good_search), True, True)

    def test_fourchan(self):
        url = "https://i.4cdn.org/"
        self.assertTrue(wanda.fourchan(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.fourchan("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.fourchan("welcome").startswith(url))
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
        url = "https://cdna.artstation.com/"
        self.assertTrue(wanda.artstation_any(None).startswith(url))
        time.sleep(3)
        self.assertTrue(wanda.artstation_any("").startswith(url))
        time.sleep(3)
        self.assertTrue(wanda.artstation_any(self.good_search).startswith(url))
        time.sleep(3)
        self.assertRaises(SystemExit, wanda.artstation_any, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.artstation_any(self.good_search), True, True)

    def test_artstation_prints(self):
        url = "https://cdna.artstation.com/"
        self.assertTrue(wanda.artstation_prints(None).startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.artstation_prints("").startswith(url))
        time.sleep(self.bed_time)
        self.assertTrue(wanda.artstation_prints("tohad").startswith(url))
        time.sleep(self.bed_time)
        self.assertRaises(SystemExit, wanda.artstation_prints, self.bad_search)
        time.sleep(self.bed_time)
        wanda.set_wp(wanda.artstation_prints(self.good_search), True, True)


if __name__ == '__main__':
    unittest.main()
