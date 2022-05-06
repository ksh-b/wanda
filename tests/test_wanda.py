import time
from wanda import wanda

import unittest


class SimpleTest(unittest.TestCase):
    good_search = "nature"
    bad_search = "foobarxyzzy"

    def test_wallhaven(self):
        url = "https://w.wallhaven.cc/full/"
        assert wanda.wallhaven(None).startswith(url)
        time.sleep(1)
        assert wanda.wallhaven("").startswith(url)
        time.sleep(1)
        assert wanda.wallhaven(self.good_search).startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.wallhaven, self.bad_search)

    def test_unsplash(self):
        url = "https://images.unsplash.com/photo-"
        assert wanda.unsplash(None).startswith(url)
        time.sleep(1)
        assert wanda.unsplash("").startswith(url)
        time.sleep(1)
        assert wanda.unsplash(self.good_search).startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.unsplash, self.bad_search)

    def test_reddit(self):
        url = "https://i.redd.it/"
        assert wanda.reddit(search=None).startswith(url)
        time.sleep(1)
        assert wanda.reddit(search="").startswith(url)
        time.sleep(1)
        assert wanda.reddit(search=self.good_search).startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.unsplash, search=self.bad_search)

    def test_imsea(self):
        url = ".mm.bing.net/th?id="
        assert url in wanda.imsea(None)
        time.sleep(1)
        assert url in wanda.imsea("")
        time.sleep(1)
        assert url in wanda.imsea(self.good_search)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.imsea, self.bad_search)

    def test_imgur(self):
        url = "https://rimgo.pussthecat.org/"
        assert wanda.imgur(None).startswith(url)
        time.sleep(1)
        assert wanda.imgur("").startswith(url)
        time.sleep(1)
        assert wanda.imgur("jmVC8").startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.imgur, self.bad_search)

    def test_fourchan(self):
        url = "https://i.4cdn.org/"
        assert wanda.fourchan(None).startswith(url)
        time.sleep(1)
        assert wanda.fourchan("").startswith(url)
        time.sleep(1)
        assert wanda.fourchan("welcome").startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.fourchan, self.bad_search)

    def test_fivehundredpx(self):
        url = "https://drscdn.500px.org/photo/"
        assert wanda.fivehundredpx(None).startswith(url)
        time.sleep(1)
        assert wanda.fivehundredpx("").startswith(url)
        time.sleep(1)
        assert wanda.fivehundredpx(self.good_search).startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.fivehundredpx, self.bad_search)

    def test_artstation_any(self):
        url = "https://cdna.artstation.com/"
        assert wanda.artstation_any(None).startswith(url)
        time.sleep(3)
        assert wanda.artstation_any("").startswith(url)
        time.sleep(3)
        assert wanda.artstation_any(self.good_search).startswith(url)
        time.sleep(3)
        self.assertRaises(SystemExit, wanda.artstation_any, self.bad_search)

    def test_artstation_prints(self):
        url = "https://cdna.artstation.com/"
        assert wanda.artstation_prints(None).startswith(url)
        time.sleep(1)
        assert wanda.artstation_prints("").startswith(url)
        time.sleep(1)
        assert wanda.artstation_prints("tohad").startswith(url)
        time.sleep(1)
        self.assertRaises(SystemExit, wanda.artstation_prints, self.bad_search)


if __name__ == '__main__':
    unittest.main()
