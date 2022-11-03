# image_formats.py
from wagtail.images.formats import Format, register_image_format

# register_image_format(Format('blogimage', 'blogimage', 'img-responsive', 'fill-750x350'))

register_image_format(Format('blogimagedefault', 'Image with default height and width', 'img-responsive', 'fill-750x350'))
register_image_format(Format('blogimagedefaultwidth', 'Image with default width', 'img-responsive', 'width-750'))

