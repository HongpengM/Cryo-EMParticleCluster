import numpy as np
import mrcfile as mf
import os
import math
import sys
# MRC_file = r'train/stack_0%s_lowpass_2x_SumCorr.mrc'
# STAR_file = r'train/stack_0%s_lowpass_2x_SumCorr_manual_lgc.star'


def read_star(fname):
    stardict = {}
    stardict['CoordinateX'] = []
    stardict['CoordinateY'] = []
    stardict['AnglePsi'] = []
    stardict['ClassNumber'] = []
    stardict['AutopickFigureOfMerit'] = []
    try:
        with open(fname) as starfile:
            for i in starfile.readlines():
                tmp = i.split()
                if len(tmp) == 5:
                    stardict['CoordinateX'].append(float(tmp[0]))
                    stardict['CoordinateY'].append(float(tmp[1]))
                    stardict['AnglePsi'].append(float(tmp[2]))
                    stardict['ClassNumber'].append(int(tmp[3]))
                    stardict['AutopickFigureOfMerit'].append(float(tmp[4]))
    except:
        # print("IO Error for STAR  ")
        pass
    else:
        print(len(stardict['CoordinateX']), "particles in " + fname[12:16])
    return stardict


def generate_mrc(stardict, MRC_file, padding, size):
    center = []
    total = 0
    for i in range(len(stardict['CoordinateX'])):
        pair = (stardict['CoordinateX'][i], stardict['CoordinateY'][i])
        center.append(list(pair))
    try:
        os.makedirs('particle_mrc/%s' % MRC_file[:-4])
    except OSError:
        print("OS Error! Existing particle_mrc derectory?")
    else:
        # print(MRC_file)
        img, img_num = sample(MRC_file, center, pad_size=padding, size=size)
        total += img_num
        for num in range(img_num):
            with mf.new(
                'particle_mrc/%s/' % MRC_file[:-4] +
                'Num_%s_class_%s.mrc' % (
                    str(num),
                    str(stardict['ClassNumber'][num]))) as smallmrc:
                tmp = np.reshape(img[num], [size, size])
                tmp = tmp.astype('float32')
                smallmrc.set_data(tmp)
                smallmrc.flush()
    return total


def sample(fname, center, pad_size=300, size=512):

    MRC_Files = mf.open(fname)
    # print(MRC_Files.data)
    # im = np.array(Image.open(fname).convert('L'))
    padding_image = MRC_Files.data[:]
    mean = np.mean(np.ravel(padding_image))
    height_stack = np.zeros([3710, pad_size])
    height_stack.fill(float(mean))
    width_stack = np.zeros([pad_size, 3710 + 2 * pad_size])
    width_stack.fill(float(mean))
    padding_image = np.hstack((padding_image, height_stack))
    padding_image = np.hstack((height_stack, padding_image))
    padding_image = np.vstack((padding_image, width_stack))
    padding_image = np.vstack((width_stack, padding_image))
    # return padding_image
    num_of_img = 0
    pos_imgs = []
    for point in center:
        # print(point)
        l_min = int(point[0] + pad_size - math.floor(size / 2))
        l_max = int(point[0] + pad_size + math.floor(size / 2))
        c_min = int(point[1] + pad_size - math.floor(size / 2))
        c_max = int(point[1] + pad_size + math.floor(size / 2))
        # tmp = np.reshape(
        # scipy.misc.imresize(
        # padding_image[l_min:l_max, c_min:c_max], [100, 100]), [100, 100, 1])
        tmp = np.reshape(padding_image[l_min:l_max, c_min:c_max], [size, size, 1])
        pos_imgs.append(tmp)
        num_of_img += 1
    return pos_imgs, num_of_img  # shape of pos_imga (i, 200, 200, 1)


# dict = read_star(STAR_file % str(101))
# print("dict: ", dict)
# generate_mrc(dict, MRC_file % str(101))

def main():
    usage = \
        """\n\nThis program generates small mrc containing particles at center.
And you can get a bunch of mrc files in a directory of the script.
\nUsage:
    python generate_particlemrc.py <STAR file path> <MRC file path> \
<padding size> <output size>\
\nExample:
    python generate_particlemrc.py "train\\\\" "train\\\\" 50 200\n\n\
If it doesn't work, think if padding size is too small,\
padding >= 0.2*size is prefered"""
    if len(sys.argv) < 5:
        print(usage)
        return 0

    STAR_file = sys.argv[1] + 'stack_0%s_lowpass_2x_SumCorr_manual_lgc.star'
    MRC_file = sys.argv[2] + 'stack_0%s_lowpass_2x_SumCorr.mrc'
    padding = int(sys.argv[3])
    size = int(sys.argv[4])
    total = 0
    # print(STAR_file, MRC_file, padding, size, sep='; ')
    for i in range(100, 200):
        try:
            dict = read_star(STAR_file % str(i))
            img_num_one = generate_mrc(dict, MRC_file % str(i), padding, size)
            # print("Cropped number %s file." % (MRC_file % str(i))[12:16])
            total += img_num_one
            # print("STAR file: ", STAR_file % str(i))
            # print("MRC file: ", MRC_file % str(i))
        except:
            # print("IO Error for %s" % str(i))
            pass
    print("removing empty dirctory...")
    for i in range(100, 200):
        try:
            dir = 'stack_0%s_lowpass_2x_SumCorr' % str(i)
            os.rmdir('particle_mrc/' + dir)
        except:
            pass
        else:
            pass
    print("All done!")
    print("Total mrc file number:", total)


if __name__ == '__main__':
    main()
