from PIL import Image, ImageFont, ImageDraw

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



def joinPictos(list_of_pictos, texto):
    '''
    Function that receive a list of pictos (filenames) in an order
    and return a image where all pitograms in the list given are paste together
    This function is used to return the result of a translation
    '''

    images = map(Image.open, list_of_pictos)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_heigth = max(heights)

    new_image = Image.new('RGBA', (total_width, max_heigth))

    x_offset = 0
    for im in images:
        new_image.paste(im, (x_offset,0))
        x_offset += im.size[0]
    filename = texto + '.jpg'
    new_image.save(filename)
