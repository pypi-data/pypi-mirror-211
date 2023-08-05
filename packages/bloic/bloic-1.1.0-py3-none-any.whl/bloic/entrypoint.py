import os

import click
from PIL import Image

from bloic import __version__


@click.command()
@click.version_option(__version__)
@click.argument('image_path', type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('--width', '-w', type=click.IntRange(min=0, min_open=True), default=1200, show_default=True, help='Target width of the image')
@click.option('--output-dir', '-o', type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True), default='.', show_default=True, help='Output directory')
@click.option('--delete', '-d', is_flag=True, help='Delete source image after conversion.')
def resize_image(image_path, width, output_dir, delete):
    """
    Resizes an image based on a target width passed as a parameter, then converts it to the WebP format.
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise click.BadParameter('The specified file path is invalid.')

    # Open the image
    image = Image.open(image_path)

    # Get the original width and height of the image
    original_width = image.width
    original_height = image.height

    # Calculate the new height while maintaining the aspect ratio of the image
    new_height = int(original_height * width / original_width)

    # Resize the image
    resized_image = image.resize((width, new_height))

    # Get the filename without the extension
    filename = os.path.splitext(os.path.basename(image_path))[0]

    # Save the resized image as a WebP file in the output directory
    output_path = os.path.join(output_dir, filename + '.webp')
    resized_image.convert('RGB').save(output_path, 'webp')

    click.echo('The image was successfully resized and converted to the WebP format!')
    if delete and os.path.exists(image_path):
        os.remove(image_path)
        click.echo('Source image was successfully deleted.')


if __name__ == '__main__':
    resize_image()
