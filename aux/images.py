from PIL import Image, ImageFont, ImageDraw

import os


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
    img = Image.new('RGB', size_picto, background_color)
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
    # making the filename
    filename = "pictoText_"+text+".png"
    # saving the image
    img.save(filename)


def joinPictos(list_of_pictos, texto, space=5, background_color='black'):
    '''
    Function that receive a list of pictos (filenames) in an order
    and return a image where all pitograms in the list given are together
    with a space between them.
    The image is saved on:
    /images/tranlations/<text_to_translate>/<text_to_translate>_translated.png
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
    path = os.getcwd()+'/images/translations/'+texto+'/'
    os.makedirs(path)
    filename = path + texto + '_translated.png'
    new_image.save(filename)
