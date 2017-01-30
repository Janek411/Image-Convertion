import png


filename = "E:\Work2\Image\\test64_16.c32"
Height = 16
Width = 64
Type = 2
Pal_Size = [32, 512]


def load_binary(fname):
    bytes_read = open(fname, "rb").read()


    bin_data = []
    for b in bytes_read:
        bin_data.append(ord(b))

    return bin_data


def get_palette(data):
    return data[0:Pal_Size[Type]]


def get_pixel(data):
    return data[Pal_Size[Type]:]


def make_palette(raw_palette):
    p_r = []
    p_g = []
    p_b = []

    for i in xrange(0, Pal_Size[Type], 2):
        p_r.append(int(raw_palette[i]/8)*8)
        p_g.append(((raw_palette[i] % 8)*8+int(raw_palette[i+1]/32))*4)
        p_b.append((raw_palette[i+1] % 32)*8)

    return p_r, p_g, p_b


def make_png(pal_r, pal_g, pal_b, pixel):
    png_data = []
    for i in xrange(0, Height):
        row_data = ()

        if Type == 1:
            wid_cnt = Width
        elif Type == 0:
            wid_cnt = Width/2

        for j in xrange(0, wid_cnt):
            ind = pixel[i*wid_cnt+j]
            if Type == 1:
                pixel_data = (pal_r[ind], pal_g[ind], pal_b[ind])
            elif Type == 0:
                ind1 = int(ind/16)
                ind2 = ind % 16
                pixel_data = (pal_r[ind1], pal_g[ind1], pal_b[ind1])
                row_data = row_data + pixel_data
                pixel_data = (pal_r[ind2], pal_g[ind2], pal_b[ind2])

            row_data = row_data + pixel_data

        png_data.append(row_data)

    return png_data


def make_png32(c32data):
    png_data = []
    for i in xrange(0, Height):
        row_data = ()

        for j in xrange(0, Width):
            ind = (i*Width+j)*4
            pixel_data = (c32data[ind], c32data[ind+1], c32data[ind+2])

            row_data = row_data + pixel_data

        png_data.append(row_data)

    return png_data


def save_png(fname, image):
    f = open(fname, 'wb')
    w = png.Writer(Width, Height)
    w.write(f, image)
    f.close()


def main():

    try:
        info_data = load_binary(filename)

        if Type == 2:
            png_image = make_png32(info_data)

        else:
            info_palette = get_palette(info_data)
            info_pixel = get_pixel(info_data)
            palette_r, palette_g, palette_b = make_palette(info_palette)
            png_image = make_png(palette_r, palette_g, palette_b, info_pixel)

        save_png(filename + '.png', png_image)

        print "Successfully convert!"
    except IOError:
        print "IO Error! filename is incorrect!"
    except IndexError:
        print "Image size or type is incorrect!"
    except:
        print "Unknown error!"


if __name__ == '__main__':
    main()
