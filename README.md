# wanda
Script to set wallpaper using keyword or randomly

[![PyPI](https://img.shields.io/pypi/v/wanda)](https://pypi.org/project/wanda/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/wanda)](https://pypistats.org/packages/wanda)
[![PyPI - License](https://img.shields.io/pypi/l/wanda)](https://tldrlegal.com/license/mit-license)

## Installation / Update
```
pip install wanda -U
```

On android (with termux):
Install [termux-api](https://github.com/termux/termux-api)
```
pkg up
pkg in clang pkg-config libxml2 libxslt libjpeg-turbo termux-api python
pip install cython lxml==5.0.0
pip install wanda -U
```

For issues installing pillow refer this [document](https://pillow.readthedocs.io/en/stable/installation.html)


## Usage
```
# Set randomly
wanda

# Set from a keyword 
wanda -t mountain

# Set from a source
wanda -s wallhaven

# Set from a source 
wanda -s wallhaven -t japan

# Set album covers
wanda -sm -t "Meltt-Love Again" -f

```
`wanda -h` for more details

## Notes

- By default, the source is [picsum](https://picsum.photos).
- Some sources may have inapt images. Use them at your own risk.

## Supported sources

- [4chan](https://boards.4chan.org) via [Rozen Arcana](https://archive-media.palanq.win)
- [500px](https://500px.com)
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

## License
MIT
