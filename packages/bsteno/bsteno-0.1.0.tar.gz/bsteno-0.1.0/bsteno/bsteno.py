class DataTooBig(Exception):
    pass


# Use the two LSB bits
_MASK = 3
_MAX_SIZE_BYTES = 3


def _read_byte(pixel):
    r, g, b, a = pixel
    return (r & _MASK) | ((g & _MASK) << 2) | ((b & _MASK) << 4) | ((a & _MASK) << 6)


def insert(img_in, data):
    "Insert 'data' into the image. 'img_in' is not modified; a new image is returned instead"

    image = img_in.convert("RGBA")
    pixels = list(image.getdata())

    data_len = len(data)

    if data_len + _MAX_SIZE_BYTES > len(pixels):
        raise DataTooBig()

    data_len_bytes = bytes(
        [data_len & 255, (data_len >> 8) & 255, (data_len >> 16) & 255]
    )

    for i, byte in enumerate(data_len_bytes + data):
        r, g, b, a = pixels[i]
        r = (r & ~_MASK) | (byte & _MASK)
        g = (g & ~_MASK) | ((byte >> 2) & _MASK)
        b = (b & ~_MASK) | ((byte >> 4) & _MASK)
        a = (a & ~_MASK) | ((byte >> 6) & _MASK)
        pixels[i] = (r, g, b, a)

    image.putdata(pixels)

    return image


def extract(image):
    "Return the binary payload hidden in the image"

    pixels = list(image.getdata())

    data_len = (
        _read_byte(pixels[0])
        | (_read_byte(pixels[1]) << 8)
        | (_read_byte(pixels[2]) << 16)
    )

    data = bytearray(data_len)
    for i in range(data_len):
        data[i] = _read_byte(pixels[i + _MAX_SIZE_BYTES])

    return data
