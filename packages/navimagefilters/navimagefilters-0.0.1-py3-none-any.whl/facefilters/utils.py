import numpy as np
import cv2


def sobelx(image, ksize=5):
	'''
	Horizontal Sobel derivative (Sobel x):
	It is obtained through the convolution of the image
	with a matrix called kernel which has always odd size.
	The kernel with size 3 is the simplest case.

	image: The numpy array of the image with 3 dimentions
	ksize: kernel size (default=5)

	utilizing fn: cv2.Sobel(original_image,ddepth,xorder,yorder,kernelsize)

	'''
	sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)

	return sobel_x


def sobely(image, ksize=5):
	'''
	Vertical Sobel derivative (Sobel y):
	It is obtained through the convolution of the image
	with a matrix called kernel which has always odd size.
	The kernel with size 3 is the simplest case.

	image: The numpy array of the image with 3 dimentions
	ksize: kernel size (default=5)


	utilizing fn: cv2.Sobel(original_image,ddepth,xorder,yorder,kernelsize)

	'''
	sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)

	return sobel_y


def laplacian(image):
	'''
	A Laplacian filter is an edge detector used to compute the 
	second derivatives of an image, measuring the rate at which 
	the first derivatives change. This determines if a change in 
	adjacent pixel values is from an edge or continuous progression

	image: The numpy array of the image with 3 dimentions
	'''
	 
	laplacian_ = cv2.Laplacian(image, cv2.CV_64F)

	return laplacian_

def canny(image, t_lower=100, t_upper=200, aperture_size=5):
	'''
	The steps to calculate the canny edge detection
	- Reduce Noise using Gaussian Smoothing.
	- Compute image gradient using Sobel filter.
	- Apply Non-Max Suppression or NMS to just jeep the local maxima
	- Finally, apply Hysteresis thresholding which that 2 threshold values T_upper and T_lower 

	image: The numpy array of the image with 3 dimentions

	'''

	canny_ = cv2.Canny(image, t_lower, t_upper, aperture_size)

	return canny_

