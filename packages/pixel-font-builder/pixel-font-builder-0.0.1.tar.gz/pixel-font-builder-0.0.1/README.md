# Pixel Font Builder

[![Python](https://img.shields.io/badge/python-3.11-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/pixel-font-builder)](https://pypi.org/project/pixel-font-builder/)

A library that helps create pixel style fonts.

## Installation

```commandline
pip install pixel-font-builder
```

## Usage

```python
import logging
import os

from examples import build_dir, outputs_dir
from examples.utils import fs_util
from pixel_font_builder import FontBuilder, Glyph, StyleName, SerifMode, WidthMode, opentype

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(build_dir)
    fs_util.make_dirs_if_not_exists(outputs_dir)

    font_builder = FontBuilder(
        size=12,
        ascent=10,
        descent=-2,
        x_height=5,
        cap_height=7,
    )

    font_builder.character_mapping = {
        ord('A'): 'CAP_LETTER_A',
    }

    font_builder.add_glyph(Glyph(
        name='.notdef',
        advance_width=8,
        offset=(0, -2),
        data=[
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ))
    font_builder.add_glyph(Glyph(
        name='CAP_LETTER_A',
        advance_width=8,
        offset=(0, -2),
        data=[
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    ))

    font_builder.meta_infos.version = '1.0.0'
    font_builder.meta_infos.family_name = 'Demo Pixel'
    font_builder.meta_infos.style_name = StyleName.REGULAR
    font_builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    font_builder.meta_infos.width_mode = WidthMode.MONOSPACED
    font_builder.meta_infos.manufacturer = 'TakWolf Studio'
    font_builder.meta_infos.designer = 'TakWolf'
    font_builder.meta_infos.description = 'A demo pixel font.'
    font_builder.meta_infos.copyright_info = 'Copyright (c) TakWolf'
    font_builder.meta_infos.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    font_builder.meta_infos.vendor_url = 'https://github.com/TakWolf/pixel-font-builder'
    font_builder.meta_infos.designer_url = 'https://takwolf.com'
    font_builder.meta_infos.license_url = 'https://scripts.sil.org/OFL'

    font_builder.save_otf(os.path.join(outputs_dir, 'demo.otf'))
    font_builder.save_otf(os.path.join(outputs_dir, 'demo.woff2'), flavor=opentype.Flavor.WOFF2)
    font_builder.save_ttf(os.path.join(outputs_dir, 'demo.ttf'))
    font_builder.save_bdf(os.path.join(outputs_dir, 'demo.bdf'))


if __name__ == '__main__':
    main()
```

## Dependencies

- [FontTools](https://github.com/fonttools/fonttools)
- [Brotli](https://github.com/google/brotli)
- [BdfFont](https://github.com/TakWolf/bdffont)

## License

Under the [MIT license](LICENSE).
