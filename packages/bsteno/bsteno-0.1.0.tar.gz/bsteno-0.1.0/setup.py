# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bsteno']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0']

entry_points = \
{'console_scripts': ['bsteno_extract = bsteno.bsteno_extract:main',
                     'bsteno_insert = bsteno.bsteno_insert:main']}

setup_kwargs = {
    'name': 'bsteno',
    'version': '0.1.0',
    'description': 'A python steganography package to insert/extract binary data into/from PNG files',
    'long_description': '# bSteno\n\nbSteno is a python module that allows users to insert and extract binary data (up to 16MB) to/from PNG files. The module doesn\'t modify the original PNG file and creates a new image instead.\n\nThe created PNG file is in RBGA format and the binary data is stored in the two LSBs of each channel. This means that 1 byte is stored in exacly one pixel of the image, with the following format:\n - The red channel contains bits 0-1\n - The green channel contains bits 2-3\n - The blue channel contains bits 4-5\n - The alpha channel contains bits 6-7\n\nThe presence of the alpha channel makes the image bigger than it could be, but I like the idea of having 1-pixel to 1-byte ratio as this simplifies the code quite a bit. This also makes it easier to extract the data if this scripts gets lost for some reason\n\nThe first three bytes/pixel of the image are used to store the size of the binary data. The size is stored in little endian\n\n## Installation\n\n```bash\n$ python3 -m pip install bsteno\n```\n\n## Use the CLI\n\nTo insert the content of `data.bin` into `source.png` and store the output in `output.png`, run:\n```bash\n$ bsteno_insert --png-in=source.png --data-in=data.bin --png-out=output.png\n```\n\nTo extract the binary data contained in `output.png` and store it in `data.bin`, run:\n```bash\n$ bsteno_extract --png-in=output.png --data-out=data.bin\n```\n\n## Use bSteno as a library\n\nbSteno can also be used as a library. It uses with the `Pillow` module to handle images. \n\nTo insert the content of `data.bin` into `source.png` and store the output in `output.png`, you can run the following code:\n```python\nimport PIL.Image\nfrom bsteno import bsteno\n\nimg_in = PIL.Image.open("source.png")\nwith open("data.bin", "rb") as f:\n\tdata = f.read()\nimg_out = bsteno.insert(img_in, data)\nimg_out.save("output.png", optimize=True)\n```\n\n`bsteno.insert` raises a `DataTooBig` exception if the data can\'t fit in the image.\n\nTo extract the binary data contained in `output.png` and store it in `data.bin`, you can run the following code:\n```python\nimport PIL.Image\nfrom bsteno import bsteno\n\nimg_in = PIL.Image.open("output.png")\ndata = bsteno.extract(img_in)\nwith open("data.out", "wb") as f:\n\tf.write(data)\n```\n\n## Development\n\nThis module uses `poetry`. After cloning the source code, run\n```bash\n$ poetry install\n```\nto prepare the virtual environment and install the cli tools. They can then be run with:\n\n```bash\n$ poetry run bsteno_insert ...\n$ poetry run bsteno_extract ...\n```\n\n### Running tests\n\n```bash\n$ poetry run python -m unittest\n```\n\n### Code formatter\n\nThis project uses `black` code formatter',
    'author': 'Blackthorn',
    'author_email': 'sosaria@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/lordblackthorn/bsteno/src',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
