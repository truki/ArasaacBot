from PIL import Image, ImageFont, ImageDraw
import config
import logging
import os
import urllib.request

logger = logging.getLogger(__name__)


def getAndSavePicFromUrl(url, path_to_save, image_name):
    '''
    Function that get an image from a URL and save it into a specific
    path passed like parameter
    '''
    print("Downloading and saving image: {}".format(image_name))
    try:
        urllib.request.urlretrieve(url, path_to_save+image_name)
        logger.info("Saving image to this path: {}".format(path_to_save))
    except Exception as e:
        logger.error("while downloading and saving the pic image: {0} ".format(image_name, e.args[0]))


def makePictoText(text, width=500, height=500, background_color="white",
                  font_type="Arial", font_size=96, font_color="black"):
    '''
    Function that make a pictogram with a background color, and with
    a text inside
    size = (width, high)
        '''
    # tuple with size of pictogram
    size_picto = (width, height)
    # make a picto with white background color with Image constructor
    img = Image.new('RGBA', size_picto, background_color)
    # create a draw object to paint on the imagee
    draw = ImageDraw.Draw(img)
    # create a text object that will be inserted in the picto
    font = ImageFont.truetype(font_type, font_size)
    # extract width and height of the text resultant
    width_text, height_text = draw.textsize(text, font)
    # if the width of the text is greater that width of the picto
    # then try with a less size of font, from 72, 71, 70, ... 24 (min)
    if width_text >= width:
        for s in list(reversed(range(24, font_size))):
            font = ImageFont.truetype(font_type, s)
            width_text, height_text = draw.textsize(text, font)
            if width_text < width:
                break
    # paint the text on the image (centered)
    draw.text(((size_picto[0]-width_text)/2, (size_picto[1]-height_text)/2),
              text, (0, 2, 2), font=font)
    return img


def joinPictos(list_of_pictos, id_translation, texto, space=5, background_color='black'):
    '''
    Function that receive a list of pictos (filenames) in an order
    and save a image where all pitograms in the list given are together
    with a space between them.
    The image is saved on:
    /images/tranlations/<id_translation>/<id>_translated.png
    This function is used to return the result of a translation
    '''

    images = map(Image.open, list_of_pictos)
    widths, heights = zip(*(i.size for i in images))
    print("widths: {0} and heights: {1}".format(widths, heights))
    total_width = sum(widths)
    max_heigth = max(heights)

    new_image = Image.new('RGBA', (total_width+(space*(len(list_of_pictos)+1)),
                          max_heigth+2*space), background_color)
    x_offset = 0
    images = map(Image.open, list_of_pictos)
    list_images = list(images)
    for im in list_images:
        new_image.paste(im, (x_offset+space, space))
        x_offset += im.size[0]+space
    path = os.getcwd()+'/images/translations/'+str(id_translation)+'/'
    os.makedirs(path, exist_ok=True)
    filename = path + str(id_translation) + '_translation.png'
    try:
        os.remove(filename)
    except OSError:
        pass
    new_image.save(filename)
