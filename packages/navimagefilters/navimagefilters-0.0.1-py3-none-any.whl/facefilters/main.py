import numpy as np
import cv2
from facefilters.utils import sobelx, sobely, laplacian, canny


def edge_detect(image_path, algorithm="canny", show=True):
	image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
	if algorithm=="sobelx":
		if show:
			cv2.imshow('Image', sobelx(image))
			cv2.waitKey(1000)
		return sobelx(image)
	elif algorithm=="sobely":
		if show:
			cv2.imshow('Image', sobely(image))
			cv2.waitKey(1000)
		return sobely(image)
	elif algorithm=="laplacian":
		if show:
			cv2.imshow('Image', laplacian(image))
			cv2.waitKey(1000)
		return laplacian(image)
	else:
		if show:
			cv2.imshow('Image', canny(image))
			cv2.waitKey(1000)
		return canny(image)
