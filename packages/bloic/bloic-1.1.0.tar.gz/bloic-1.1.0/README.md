# bloic (blog-post-image-converter)

## Description

**bloic** (for **blo**g-post **i**mage **c**onverter ) is a CLI tool developed to convert and resize image to good format & size for blog post.

## Dependencies

- [click](https://click.palletsprojects.com) to easily create a CLI

## Installation

### With `pip`

```console
pip install blog-post-image-converter
```

### With Docker

```console
docker pull bloic
```

## Usage

```console
Usage: bloic [OPTIONS] IMAGE_PATH

  Resizes an image based on a target width passed as a parameter, then
  converts it to the WebP format.

Options:
  --version                   Show the version and exit.
  -w, --width INTEGER RANGE   Target width of the image  [default: 1200; x>0]
  -o, --output-dir DIRECTORY  Output directory  [default: .]
  -d, --delete                Delete source image after conversion.
  --help                      Show this message and exit.
```

### Examples

Follwing command will create image named `image.webp` with a width of 1200px in current directory.

#### With installed package

```console
bloic image.jpeg
``` 

#### With Docker

```console
docker run --rm -v ${PWD}:/data -w /data bloic image.jpeg
```

## Support

Got questions?

You could [open an issue here](https://gitlab.com/romaiiiinnn/blog-post-image-converter/-/issues).

## Contributing

This is an active open-source project. I am always open to people who want to use the code or contribute to it.

Thank you for being involved! :heart_eyes:

## Authors & contributors

The original setup of this repository is by [Romain RICHARD](https://gitlab.com/romaiiiinnn).

## License

Every details about licence are in a [separate document](LICENSE).
