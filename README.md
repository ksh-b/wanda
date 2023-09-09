# wanda
Script to set wallpaper using keyword or randomly

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e5aacd529ce04f3fb8c0f9ce6a3bdd9e)](https://www.codacy.com/gh/ksyko/wanda/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ksyko/wanda&amp;utm_campaign=Badge_Grade)[![PyPI](https://img.shields.io/pypi/v/wanda)](https://pypi.org/project/wanda/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/wanda)](https://pypistats.org/packages/wanda)
[![PyPI - License](https://img.shields.io/pypi/l/wanda)](https://tldrlegal.com/license/mit-license)
[![codecov](https://codecov.io/gl/kshib/wanda/branch/main/graph/badge.svg?token=L88CXOYRTW)](https://codecov.io/gl/kshib/wanda)

## Installation / Update
```
pip install wanda -U
```

On android (with termux):
```
pkg in libxml2 libxslt libjpeg-turbo
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
```
`wanda -h` for more details

## Notes
- By default, the source is [unsplash](https://unsplash.com).
- Some sources may have inapt images. Use them at your own risk.

## Supported sources

- [4chan](https://boards.4chan.org) via [Rozen Arcana](https://archive-media.palanq.win)
- [artstation](https://artstation.com)
- [imgur](https://imgur.com) via [rimgo](https://rimgo.pussthecat.org)
- [earthview](https://earthview.withgoogle.com)
- local
- [picsum](https://picsum.photos)
- [unsplash](https://unsplash.com)
- [wallhaven](https://wallhaven.cc)

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
