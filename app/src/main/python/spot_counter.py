# -*- coding: utf-8 -*-
"""
Contains several functions which are useful for counting the number of spots in
a photo and predicting the number of dna copies these spots represent.
"""

from autocrop import crop
import cv2 as cv2
import numpy as np
import os


def increase_contrast(img):
    """
    Returns a more contrasted version of img. This constrast is applied mainly
    through first erosion then contrast limited adaptive histogram
    equalization.
    Returns:
    - contrasted_img: contrasted version of img
    """
    kernel_size = 5
    iterations = 3
    contrast_threshold = 1
    grid_size = 5
    alpha = 3  # (1.0-3.0)
    beta = 0  # (0-100)

    # kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # eroded_img = cv2.erode(img, kernel, iterations=iterations)

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=contrast_threshold,
                            tileGridSize=(grid_size, grid_size))
    clahe_img = clahe.apply(img)

    contrast = 10
    f = 131 * (contrast + 127) / (127 * (131 - contrast))
    alpha_c = f
    gamma_c = 127 * (1 - f)

    buf = cv2.addWeighted(clahe_img, alpha_c, clahe_img, 0, gamma_c)

    #contrasted_img = apply_contrast(clahe_img)
    #adjusted = cv2.convertScaleAbs(clahe_img, alpha=alpha, beta=beta)

    return buf


def apply_blur(img):
    """
    Returns a blurred version of img using a bilateral filter.
    Parameters:
    - img: the image to be blurred
    Returns:
    - blurred_img: blurred version of img
    """
    diameter = 50
    sigma_color = 50
    sigma_space = 50
    blurred_img = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
    return blurred_img


def isolate_spots(img):
    """
    Returns a version of img with its spots isolated.
    Parameters:
    - img: the image to be analyzed
    Returns:
    - markers: the markers, or connected components of img
    """
    max_threshold_value = 255
    block_threshold_size = 61
    threshold_constant = 0
    kernel_size = 1
    iterations = 1

    threshold_img = cv2.adaptiveThreshold(img, max_threshold_value,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY,
                                          block_threshold_size,
                                          threshold_constant)

    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # img_opening = cv2.morphologyEx(threshold_img, cv2.MORPH_OPEN, kernel,
    #                               iterations=iterations)
    diameter = 10
    sigma_color = 200
    sigma_space = 50
    blurred_img = cv2.bilateralFilter(threshold_img, diameter, sigma_color, sigma_space)
    return blurred_img


def produce_output_image(img, circles, filepath):
    """
    Produces and save and an image that has img as its backgound and overlays
    the circles specified by the circles paramater in green. Saves this image
    at path as filepath.
    Parameters:
    - img: the background of the image being saved, should be an RGB image
    - circles: the circles overlayed on the image in green, should be the
               return of cv2.HoughCircles)
    - filepath: the path that the resulting image is saved at
    """
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 255), 2)
        # draw the center of the circle
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imwrite(filepath, img)


def number_of_spots(img_path, result_img_path=None):
    """
    Returns the number of spots in the img at img_path. If result_img_path is
    specified, saves an image representating the spots found at the path
    result_img_path. If result_img_path is not specified, does not save any
    images.
    Parameters:
    - img_path: the image to be analyzed
    - result_img_path: resutling image path, optional
    Returns:
    - num_spots: the number of spots in img
    """
    img = crop(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    contrasted_img = increase_contrast(gray_img)

    blurred_img = apply_blur(contrasted_img)

    markers_img = isolate_spots(blurred_img)

    dp = 0.75
    min_dist = 40
    param1 = 300
    param2 = 35
    min_radius = 20
    max_radius = 60
    circles = cv2.HoughCircles(markers_img, cv2.HOUGH_GRADIENT, dp=dp,
                               minDist=min_dist, param1=param1, param2=param2,
                               minRadius=min_radius, maxRadius=max_radius)

    # There are no circles
    if circles is None:
        return 0

    if result_img_path:
        # kernel = np.ones((19,19),np.uint8)
        # erosion = cv2.erode(cimg,kernel,iterations = 1)
        # dilation = cv2.dilate(erosion,kernel,iterations = 1)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        lab_planes = cv2.split(lab)
        contrast_threshold = 4# 2.5
        grid_size = 11# 3
        clahe = cv2.createCLAHE(clipLimit=contrast_threshold,
                                tileGridSize=(grid_size, grid_size))
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv2.merge(lab_planes)
        cimg = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        cimg *= 2

        produce_output_image(cimg, circles, result_img_path)

    return len(circles[0, :])


def number_of_dna_copies(spot_count):
    """
    Returns the estimated number of cDNA copies based on the given spot count
    found using least squares polynomial regression.
    Paramters:
    - spot_count: number of spots used to predict cDNA copies
    Returns:
    - n_initial_dna: the estimated number of cDNA copies based on the given
    spot count
    """
    # standard curve
    cdna = [25, 50, 100, 500, 1000]
    log_cdna = np.log10(cdna)
    avg_spot_count = [2, 2.01, 6.48, 25.09, 31.33]

    lin_reg_line = np.polyfit(log_cdna, avg_spot_count, 1)
    polynomial = np.poly1d(lin_reg_line)

    intercept = polynomial[0]
    slope = polynomial[1]

    # initial DNA calculations from standard curve
    log_initial_cdna = (spot_count - intercept) / slope
    n_initial_dna = round(10 ** log_initial_cdna)

    return n_initial_dna


def average_number_of_spots(dir_name):
    """
    Returns the average number of spots in the images in the directory
    dir_name.
    Parameters:
    - dir_name: the directory to be analyzed. Assumes this directory is
    populated solely with jpeg images.
    Returns:
    - num_spots: the average number of spots.
    """

    spot_sum = 0
    photos = os.listdir(dir_name)
    for photo_name in photos:
        photo_path = os.path.join(dir_name, photo_name)
        spot_sum += number_of_spots(photo_path)
    avg_spot_count = spot_sum / len(photos)
    return avg_spot_count

def main():
    # spot_count = number_of_spots('TestImages/300cps_R.jpg', 'test.png')
    filename = os.path.join(os.path.dirname(__file__), '300cps_R.jpg')

    spot_count = number_of_spots(filename)
    return "Spot Count: " + str(spot_count) + " DNA Copies: " + str(number_of_dna_copies(spot_count))
    #average_number_of_spots('TestImages/81 frames_1')