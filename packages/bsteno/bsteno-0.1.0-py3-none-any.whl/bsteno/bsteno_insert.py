import argparse
import PIL.Image
from . import bsteno


def main():
    parser = argparse.ArgumentParser(description="Insert binary data into a PNG file")

    parser.add_argument(
        "--png-in",
        action="store",
        required=True,
        metavar="filename",
        help="Input PNG file",
    )

    parser.add_argument(
        "--data-in",
        action="store",
        required=True,
        metavar="filename",
        help="Input binary file",
    )

    parser.add_argument(
        "--png-out",
        action="store",
        required=True,
        metavar="filename",
        help="Output PNG file",
    )

    args = parser.parse_args()

    img_in = PIL.Image.open(args.png_in)
    with open(args.data_in, "rb") as f:
        data = f.read()
    img_out = bsteno.insert(img_in, data)
    img_out.save(args.png_out, optimize=True)
