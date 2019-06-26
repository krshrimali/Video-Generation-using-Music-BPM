import sys, os
import cv2
import numpy as np

class ImgProcessing(object):
	"""docstring for ImgProcessing"""
	def __init__(self, image):
		super(ImgProcessing, self).__init__()
		# Should already be of type: np.array()
		# TODO: Check if image is of type np.ndarray, else cv2.imread and then proceed
		# Or use str type to check, or assert
		# if(type != np.ndarray):
		# 	self.img = cv2.imread(image, 1)
		# else:
		# 	self.img = image
		
		# Assuming image is of type np.ndarray
		self.img = image
		self.img_blur = None
		self.list_images = []

	def blur(self, kernel_size=7):
		self.img_blur = cv2.blur(self.img, (kernel_size, kernel_size))

	def zoom(self, ratio, what="in"):
		# height = int(percentage * self.img.shape[1])
		# width = int(percentage * self.img.shape[0])
		#  self.img_zoom = cv2.resize(self.img, (height, width), cv2.INTER_CUBIC)
		if(what == "in"):
			height = int(self.img.shape[0] * ratio)
			width = int(self.img.shape[1] * ratio)
			print(width, height)
			print(self.img.shape)
			self.img_zoom = cv2.pyrUp(self.img, dstsize=(width, height))
			cv2.imshow("Original", self.img)
			cv2.imshow("Zoomed", self.img_zoom)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		elif(what == "out"):
			height = self.img.shape[0]//ratio
			width = self.img.shape[1]//ratio
			print(height, width)
			print(self.img.shape)
			self.img_zoom = cv2.pyrDown(self.img, dstsize=(width, height))
			cv2.imshow("Original", self.img)
			cv2.imshow("Zoomed", self.img_zoom)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			# Apply padding
			empty_image = np.zeros(self.img.shape)
			# empty_image[]

	def join(self, type=blur):
		# Return list of frames need to be combined using fps
		self.list_images.append(img)
		if(type == "blur"):
			for i in range(3, 151, 2):
				# Call blur function
				self.blur(i)
				self.list_images.append(self.img_blur)
		if(type == "zoom"):
			# Zoom by some percentage
			# 50%, 60%, 70%, 80%
			# Kind of bump
			self.zoom(2, "in")
			self.list_images.append(self.img_zoom)
			self.zoom(2, "out")
			self.list_images.append(self.img_zoom)
			'''
			for i in range(2, 3, 1):
				if(i % 2 == 0):
					self.zoom(i, "in")
				else:
					self.zoom(i, "out")
				self.list_images.append(self.img_zoom)
			'''
		return self.list_images

# Test main function
if __name__ == "__main__":
	# Read Image
	if(len(sys.argv) > 1):
		img = cv2.imread(sys.argv[1], 1)
	else:
		img = cv2.imread("data/IMG20190609123833.jpg", 1)

	# Init class
	imgproc = ImgProcessing(img)
	images = imgproc.join(type="zoom")
	print("Images generated")

	video_name = "zoomed.avi"
	height, width = img.shape[0], img.shape[1]
	# Let's make a 5 second video
	video = cv2.VideoWriter(video_name, 0, len(images)//5, (width, height), True)

	for count, img_blurred in enumerate(images):
		print("Writing: ", count)
		video.write(img_blurred)

	# List of deblurred images 
	images_deblurred = [images[len(images)-x-1] for x in range(0, len(images))]

	for count, img_deblurred in enumerate(images_deblurred):
		print('Reverse writing: ', count)
		video.write(img_deblurred)


	video.release()