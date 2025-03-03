# wanda
Set random wallpapers with or without a keyword

[![PyPI](https://img.shields.io/pypi/v/wanda)](https://pypi.org/project/wanda/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/wanda)](https://pypistats.org/packages/wanda)
[![PyPI - License](https://img.shields.io/pypi/l/wanda)](https://tldrlegal.com/license/mit-license)

## Installation / Update
### On Windows/Linux:
```
pip install wanda -U
```
You may also use [pipx](https://pipx.pypa.io/latest/)

### On android:<br>
Install [termux](https://github.com/termux/termux-app) and [termux-api](https://github.com/termux/termux-api)
In termux:<br>
```
pkg up
pkg in clang pkg-config libxml2 libxslt libjpeg-turbo termux-api python
pip install cython lxml==5.2.2
pip install wanda -U
```

For issues installing pillow refer this [document](https://pillow.readthedocs.io/en/stable/installation.html)


## Usage
```
# Set randomly (uses picsum)
wanda

# Set from a keyword (uses picsum)
wanda -t mountain

# Set from a source
wanda -s wallhaven

# Set from a source with keyword
wanda -s wallhaven -t japan

# Use shortcode for source (w=wallhaven)
# For other shortcodes for other sources, check 'wanda -u'
wanda -s w -t japan

# Set album covers (m=musicbrainz)
# album cover would be square, so use -f to fit it to screen
# format for query with musicbrainz is 'artist-album'
wanda -s m -t "Meltt-Love Again" -f

# Set from folder (l=local)
wanda -s l -t "/path/to/wallpapers"

# download current wallpaper
wanda -d

# android specific - set wallpaper to lockscreen only
wanda -l

# android specific - set wallpaper to homescreen only
wanda -o

```
`wanda -h` for more details

## Notes

- By default, the source is [picsum](https://picsum.photos).
- Some sources may have inapt images. Use them at your own risk.

## Supported sources

- [4chan](https://boards.4chan.org) via [Rozen Arcana](https://archive-media.palanq.win)
- [artstation](https://artstation.com)
- [imgur](https://imgur.com) via [rimgo](https://rimgo.projectsegfau.lt)
- [earthview](https://chromewebstore.google.com/detail/earth-view-from-google-ea/bhloflhklmhfpedakmangadcdofhnnoh)
- generated
- local
- [musicbrainz](https://musicbrainz.org/) (Album covers)
- [picsum](https://picsum.photos)
- [reddit](https://reddit.com)
- [wallhaven](https://wallhaven.cc)
- [waifu](https://www.waifu.im/)

## Build
[python](https://www.python.org/downloads) and [poetry](https://python-poetry.org) are needed
```
git clone https://github.com/ksh-b/wanda.git
cd wanda
poetry install
poetry build
poetry run wanda
```

## Uninstall
```
pip uninstall wanda
```

## Why the name 'wanda'
This project was originally called [Wallpapers-ANDroid](https://github.com/ksyko/wallpaper-android)
<details>
  <summary></summary>
  Why the a at the end? 'wand' was already taken I think. a for awesome, i guess.
</details>


## License
MIT
