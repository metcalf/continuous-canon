import Image, ImageDraw

PRINT_WIDTH = 4.25
MARGIN = 0.25

PADDING_WIDTH = 0.25
PADDING_HEIGHT = 0.7
PADDING_GAP = 1.5
PADDING_COLOR = (200, 200, 200)

def draw_stripes(image, offset, dpi):
    draw = ImageDraw.Draw(image)
    height = PADDING_HEIGHT * dpi[1]
    width = PADDING_WIDTH * dpi[0]
    rows = int(height / 8)
    
    for i in range(rows):
        top = offset + i * 8
        draw.rectangle((0, top, width, top+1), fill=PADDING_COLOR)
    
    del draw
    
def stripe_image(path):
    orig_img = Image.open(path)
    (orig_w_dpi, orig_h_dpi) = orig_img.info["dpi"]
    (orig_w, orig_h) = orig_img.size
    
    dpi_factor = (float(orig_w) / orig_w_dpi) / (PRINT_WIDTH - 2*MARGIN)
    
    new_w_dpi = int(orig_w_dpi * dpi_factor)
    new_h_dpi = int(orig_h_dpi * dpi_factor)
    
    new_h = orig_h + new_h_dpi * PADDING_HEIGHT * 2;
    new_w = orig_w + new_w_dpi * (MARGIN * 2 + PADDING_GAP + PADDING_WIDTH);
    
    new_img = Image.new(orig_img.mode, (new_w, new_h))
    draw = ImageDraw.Draw(new_img)
    draw.rectangle((0, 0, new_w, new_h), fill=(255, 255, 255))
    del draw
    
    draw_stripes(new_img, 0, (new_w_dpi, new_h_dpi))
    draw_stripes(new_img, 
                 new_h - PADDING_HEIGHT*new_h_dpi, 
                (new_w_dpi, new_h_dpi))
    
    region = orig_img.crop((0, 0, orig_w, orig_h))
    left = int(new_w - (orig_w + MARGIN * new_w_dpi))
    top = int(PADDING_HEIGHT * new_h_dpi)

    new_img.paste(region, (left, top, left+orig_w, top+orig_h))
    
    new_img.save("striped.jpg", "JPEG", dpi=(new_w_dpi, new_h_dpi))
    