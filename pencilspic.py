from skimage.filters import threshold_otsu
import numpy as np
from skimage.measure import label, regionprops
import cv2 as cv

counter = 0
incounter = 0

for i in range(1, 13):
    incounter = 0
    img = cv.imread(f"C:\\study\\images\\img ({i}).jpg", cv.IMREAD_GRAYSCALE)

    _, binary_image = cv.threshold(img, 142, 255, cv.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    opened_image = cv.morphologyEx(binary_image, cv.MORPH_OPEN, kernel, iterations=2)

    closed_image = cv.morphologyEx(opened_image, cv.MORPH_CLOSE, kernel, iterations=2)

    labeled = label(closed_image)
    labeled = labeled[50:-50, 50:-50]

    min_object_size = 100
    filtered_labeled = np.where(
        np.isin(labeled, [prop.label 
        for prop in regionprops(labeled) 
        if prop.area >= min_object_size]), labeled, 0)

    filtered_labeled_1 = np.zeros_like(filtered_labeled)

    for region in regionprops(filtered_labeled):
        bbox = region.bbox

        if (region.axis_major_length / region.axis_minor_length) > 10:
            counter += 1
            incounter += 1
            filtered_labeled_1[bbox[0]:bbox[2], bbox[1]:bbox[3]] += region.image
    print("Img №", i, "Pencils: ", incounter)
    pencils_image = filtered_labeled_1

print("Total pencil number:", counter)