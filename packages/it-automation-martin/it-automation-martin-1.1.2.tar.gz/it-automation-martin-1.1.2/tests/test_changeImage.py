from PIL import Image
import os
from it_automation.changeImage import resize_image, save_image_jpeg, convert_image


def test_resize_image():
    im = Image.new("L", (100, 100))
    im_resized = im.resize((200, 200))
    test_im_resized = resize_image(im, 200, 200)
    assert test_im_resized.size == im_resized.size


def test_save_image_jpeg(tmpdir):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # image_path = os.path.expanduser('~') + '/images/001.tiff'
    file_path = os.path.dirname(os.path.realpath(__file__))
    image_path = file_path + '/images/001.tiff'

    image_file_name = '001.tiff'
    with Image.open(image_path) as im:
        save_image_jpeg(im, image_file_name, tmpdir)
    test_file = os.path.join(tmpdir, '001.jpeg')
    assert os.path.isfile(test_file)


def test_convert_tiff(tmpdir):
    file_path = os.path.dirname(os.path.realpath(__file__))
    test_image_directory = file_path + '/images'
    resize_width = 600
    resize_height = 400
    convert_image(test_image_directory, resize_width, resize_height, tmpdir)

    test_jpeg_list = ['001.jpeg', '002.jpeg']
    for test_jpeg_file in test_jpeg_list:
        assert os.path.isfile(os.path.join(tmpdir, test_jpeg_file))
