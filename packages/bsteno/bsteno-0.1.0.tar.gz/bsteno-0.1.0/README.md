# bSteno

bSteno is a python module that allows users to insert and extract binary data (up to 16MB) to/from PNG files. The module doesn't modify the original PNG file and creates a new image instead.

The created PNG file is in RBGA format and the binary data is stored in the two LSBs of each channel. This means that 1 byte is stored in exacly one pixel of the image, with the following format:
 - The red channel contains bits 0-1
 - The green channel contains bits 2-3
 - The blue channel contains bits 4-5
 - The alpha channel contains bits 6-7

The presence of the alpha channel makes the image bigger than it could be, but I like the idea of having 1-pixel to 1-byte ratio as this simplifies the code quite a bit. This also makes it easier to extract the data if this scripts gets lost for some reason

The first three bytes/pixel of the image are used to store the size of the binary data. The size is stored in little endian

## Installation

```bash
$ python3 -m pip install bsteno
```

## Use the CLI

To insert the content of `data.bin` into `source.png` and store the output in `output.png`, run:
```bash
$ bsteno_insert --png-in=source.png --data-in=data.bin --png-out=output.png
```

To extract the binary data contained in `output.png` and store it in `data.bin`, run:
```bash
$ bsteno_extract --png-in=output.png --data-out=data.bin
```

## Use bSteno as a library

bSteno can also be used as a library. It uses with the `Pillow` module to handle images. 

To insert the content of `data.bin` into `source.png` and store the output in `output.png`, you can run the following code:
```python
import PIL.Image
from bsteno import bsteno

img_in = PIL.Image.open("source.png")
with open("data.bin", "rb") as f:
	data = f.read()
img_out = bsteno.insert(img_in, data)
img_out.save("output.png", optimize=True)
```

`bsteno.insert` raises a `DataTooBig` exception if the data can't fit in the image.

To extract the binary data contained in `output.png` and store it in `data.bin`, you can run the following code:
```python
import PIL.Image
from bsteno import bsteno

img_in = PIL.Image.open("output.png")
data = bsteno.extract(img_in)
with open("data.out", "wb") as f:
	f.write(data)
```

## Development

This module uses `poetry`. After cloning the source code, run
```bash
$ poetry install
```
to prepare the virtual environment and install the cli tools. They can then be run with:

```bash
$ poetry run bsteno_insert ...
$ poetry run bsteno_extract ...
```

### Running tests

```bash
$ poetry run python -m unittest
```

### Code formatter

This project uses `black` code formatter