import os
import cv2
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from datetime import datetime
from img_an_tm import cropping
from numpy import sum
import numpy as np


# This function is connected to the button "Calculate".
# It trigers cropping and template matching (slit search), plots, fits and saves results.
# It takes boundary value "gr" (if the value of pixel's brightness is less, we
# say that pixel is black. If the value of pixel's brightness is more (up to 255),
# say that pixel is white. Also it takes the list with pathes to all the images we choosed.
def calcs(gr, *images):
    # function for measuring distance (counting white pixels)
    def dist(hk, *thr):
        result = 0
        for il in thr[hk]:
            if il[0] != 0:
                result += 1
        return result

    angles = []
    dir = os.getcwd()

    # see description for this function in "img_an_tm.py"
    cropping()
    os.chdir(dir + '/cropped')
    images = os.listdir()
    images.sort()
    for name in images:
        image = cv2.imread(name)

        # converting image to b&w format
        thresh = cv2.threshold(image, int(gr), 255, 0)[1]
        cv2.imwrite(dir + '/thresholds/' + name[0:-12] + '_threshold.png', thresh)

        # algorithm for finding a slit on the photo
        real_height = thresh.shape[0]
        h = real_height / 3
        gaps = []
        h_max = 0
        h_min = 0
        for i in range(3):
            gaps.append(dist(int(((i + 1 / 2) * h) // 1), *thresh))
        for i in range(len(thresh)):
            if dist(i, *thresh) <= (gaps[0] + gaps[0] ** (1 / 2)):
                if dist(i + 2, *thresh) <= (gaps[0] + gaps[0] ** (1 / 2)):
                    h_max = i
                    break
        for i in range(len(thresh)):
            if dist(len(thresh) - 1 - i, *thresh) <= (gaps[-1] + gaps[-1] ** (1 / 2)):
                if dist(len(thresh) - 1 - i - 2, *thresh) <= (gaps[-1] + gaps[-1] ** (1 / 2)):
                    h_min = len(thresh) - 1 - i
                    break

        dist_data = []
        pxl = []

        # counting number of white pixels at each height
        for i in range(len(thresh)):
            dist_data.append(dist(i, *thresh))
            pxl.append(i)

        x_data = []
        y_data = []

        for i in range(h_max, h_min + 1):
            x_data.append(int(i))
            y_data.append(int(dist_data[i]))

            # fitting

        def f(x, *par):
            return par[0] * x + par[1]

        p0 = [-1, 40]
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        popt, poper = curve_fit(f, x_data, y_data, p0=p0)

        # drawing a graph
        plt.plot(pxl, dist_data, 'o-r', alpha=1, color='BLACK', label="first", lw=0.1, mew=0.05, ms=1)
        plt.plot(x_data, f(x_data, *popt), '-r')
        plt.suptitle(name)
        plt.xlabel('Height, pxl')
        plt.ylabel('Number of white pixels')
        plt.savefig(dir + '/plots/' + name[:-12] + '_plot.png')
        # plt.show()
        plt.clf()
        plt.cla()

        angle_deviation = np.arctan(popt[0])

        angles.append(float(np.degrees(np.fabs(angle_deviation))))
        del popt

    # final calculations
    av_angle = round(sum(angles) / len(angles), 4)
    sum_angl = 0
    for el in angles:
        sum_angl += (av_angle - el) ** 2
    sigma = round(0.95 * (sum_angl / (len(angles) * (len(angles) - 1))) ** (1 / 2), 4)
    os.chdir(dir)
    angles = [str(round(i, 4)) for i in angles]
    diametr = 10  # mm
    min_dist = diametr * 1000 * ((2 * (1 - np.cos(np.radians(av_angle)))) ** (1 / 2))

    # writing results to "results.txt"
    f = open('results.txt', 'w')
    f.write('Angles : ' + ' ,'.join(angles) + '\n')
    f.write('Average angle : ' + str(av_angle) + '\t')
    f.write('Error : ' + str(sigma) + '\t')
    f.write('Relative error : ' + str(round(sigma * 100 / av_angle, 1)) + '%\n')
    f.write('Minimal possible distance : ' + str(round(min_dist, 1)) + ' mkm')
    f.close()

    return 0
