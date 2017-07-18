from PIL import Image, ImageFont, ImageDraw
import config
import logging
import os
import urllib.request

logger = logging.getLogger(__name__)


def markPictogram(path_to_picto):
    '''
    Function that receive a path to a picto and create a new pictogram
    marked with two cross lines in the form of X
    '''
    # open pictogram to mark
    img = Image.open(path_to_picto)
    # get size
    (width, height) = img.size
    # create Draw instance over img
    draw = ImageDraw.Draw(img)
    # Drawing a mark crossing lines in the form of a 'X'
    draw.line((30, 30, width-30, height-30), width=30, fill="black")
    draw.line((30, height-30, width-30, 30), width=30, fill="black")
    # return the image object
    return img



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


def joinPictos(list_of_pictos, id_translation, texto="", space=5, background_color='black'):
    '''
    Function that receive a list of pictos (filenames) in an order
    and save a image where all pitograms in the list given are together
    with a space between them.
    The image is saved on:
    /images/tranlations/<id_translation>/<id>_translated.png
    This function is used to return the result of a translation
    '''

    # open all images in a list of Image objects
    images = map(Image.open, list_of_pictos)
    # create to list with the widths and heights
    widths, heights = zip(*(i.size for i in images))
    # calc the total width and max height
    total_width = sum(widths)
    max_heigth = max(heights)

    # Create a new image with RGBA color scheme with black background
    # and with a width of total_width plus  the spaces between them
    # and with a height of max_height plus 2 spaces
    new_image = Image.new('RGBA', (total_width+(space*(len(list_of_pictos)+1)),
                          max_heigth+2*space), background_color)

    # Now we take the list of Image objects and we pasted it
    # over new_image secuencially
    x_offset = 0
    images = map(Image.open, list_of_pictos)
    list_images = list(images)
    for im in list_images:
        new_image.paste(im, (x_offset+space, space))
        x_offset += im.size[0]+space
    path = os.getcwd()+'/images/translations/'+str(id_translation)+'/'

    # create the correct directory
    os.makedirs(path, exist_ok=True)
    # create the filename path
    if texto == "":
        filename = path + str(id_translation) + '_translation.png'
    else:
        filename = path + str(id_translation) + '_agenda_' + texto + '.png'
    # remove it, if exist
    try:
        os.remove(filename)
    except OSError:
        pass
    # finally we save it:
    new_image.save(filename)

    return filename
