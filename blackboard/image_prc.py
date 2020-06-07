from PIL import Image

class Image_prc():

    def change_clr(self, img_name: str, rgb: list, new_rgb: list,
                   alpha=255, img_ext='PNG'):
        if img_ext == 'PNG' and not(img_name.endswith('.png')):
            raise ValueError('img_ext',img_ext, 'does not match with image name', img_name)
        img = Image.open(img_name)
        img = img.convert('RGBA')
        data = img.getdata()
        new_data = []

        for el in data:
            if el[0] == rgb[0] and el[1] == rgb[1] and el[2] == rgb[2]:
                new_data.append((new_rgb[0], new_rgb[1],
                                new_rgb[2], alpha))
            else:
                new_data.append(el)
        img.putdata(new_data)
        img.save(img_name, img_ext)

    def invert_clrs(self, img_name: str, img_ext: str = 'PNG',
                    alpha=255, excl_rgb=[-1, -1, -1]):
        img = Image.open(img_name)
        img = img.convert('RGBA')
        data = img.getdata()
        new_data = []

        for el in data:
            if el[0] == excl_rgb[0] and el[1] == excl_rgb[1] and el[2] == excl_rgb[2]:
                new_data.append(el)
            else:
                rgb = (255-el[0], 255-el[1], 255-el[2], alpha)
                new_data.append(rgb)

        img.putdata(new_data)
        img.save(img_name, img_ext)

image_prc = Image_prc()
