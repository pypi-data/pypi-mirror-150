import argparse
import PIL.Image
from . import bsteno


def main():
    parser = argparse.ArgumentParser(description="Extract binary data from a PNG file")

    parser.add_argument(
        "--png-in",
        action="store",
        required=True,
        metavar="filename",
        help="Input PNG file",
    )

    parser.add_argument(
        "--data-out",
        action="store",
        required=True,
        metavar="filename",
        help="Output binary file",
    )

    args = parser.parse_args()

    img_in = PIL.Image.open(args.png_in)
    data = bsteno.extract(img_in)
    with open(args.data_out, "wb") as f:
        f.write(data)
