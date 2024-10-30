import cv2
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import time
import os

def detect_blur_fft_cv2(image, size=60, thresh=10, vis=False):
    
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = np.float32(image)
	# grab the dimensions of the image and use the dimensions to
	# derive the center (x, y)-coordinates
	(h, w) = image.shape
	(cX, cY) = (int(w / 2.0), int(h / 2.0))

    # compute the FFT to find the frequency transform, then shift
	# the zero frequency component (i.e., DC component located at
	# the top-left corner) to the center where it will be more
	# easy to analyze
	fft = cv2.dft(image, flags=cv2.DFT_COMPLEX_OUTPUT)
	fftShift = np.fft.fftshift(fft)

    # check to see if we are visualizing our output
	if vis:
		# compute the magnitude spectrum of the transform
		# magnitude = 20 * np.log(np.abs(fftShift))
		magnitude = 20 * np.log(cv2.magnitude(fftShift[:,:,0], fftShift[:,:,1]))
		# display the original input image
		(fig, ax) = plt.subplots(1, 2, )
		ax[0].imshow(image, cmap="gray")
		ax[0].set_title("Input")
		ax[0].set_xticks([])
		ax[0].set_yticks([])
		# display the magnitude image
		ax[1].imshow(magnitude, cmap="gray")
		ax[1].set_title("Magnitude Spectrum")
		ax[1].set_xticks([])
		ax[1].set_yticks([])
		# show our plots
		plt.show()

    # zero-out the center of the FFT shift (i.e., remove low
	# frequencies), apply the inverse shift such that the DC
	# component once again becomes the top-left, and then apply
	# the inverse FFT
	fftShift[cY - size:cY + size, cX - size:cX + size] = 0
	fftShift = np.fft.ifftshift(fftShift)
	recon = cv2.idft(fftShift)

	# compute the magnitude spectrum of the reconstructed image,
	# then compute the mean of the magnitude values
	magnitude = cv2.magnitude(recon[:,:,0],recon[:,:,1])
	# magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
	magnitude = 20 * np.log(magnitude)
	mean = np.mean(magnitude)
	# cv2.imshow('magnitude', magnitude.astype(np.int8))
	# cv2.waitKey(0)

	# the image will be considered "blurry" if the mean value of the
	# magnitudes is less than the threshold value
	return (mean, mean <= thresh)


def detect_blur_fft(image, size=60, thresh=10, vis=False):    
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# grab the dimensions of the image and use the dimensions to
	# derive the center (x, y)-coordinates
	(h, w) = image.shape
	(cX, cY) = (int(w / 2.0), int(h / 2.0))

    # compute the FFT to find the frequency transform, then shift
	# the zero frequency component (i.e., DC component located at
	# the top-left corner) to the center where it will be more
	# easy to analyze
	fft = np.fft.fft2(image)
	fftShift = np.fft.fftshift(fft)

    # check to see if we are visualizing our output
	if vis:
		# compute the magnitude spectrum of the transform
		magnitude = 20 * np.log(np.abs(fftShift))
		# display the original input image
		(fig, ax) = plt.subplots(1, 2, )
		ax[0].imshow(image, cmap="gray")
		ax[0].set_title("Input")
		ax[0].set_xticks([])
		ax[0].set_yticks([])
		# display the magnitude image
		ax[1].imshow(magnitude, cmap="gray")
		ax[1].set_title("Magnitude Spectrum")
		ax[1].set_xticks([])
		ax[1].set_yticks([])
		# show our plots
		plt.show()

    # zero-out the center of the FFT shift (i.e., remove low
	# frequencies), apply the inverse shift such that the DC
	# component once again becomes the top-left, and then apply
	# the inverse FFT
	fftShift[cY - size:cY + size, cX - size:cX + size] = 0
	fftShift = np.fft.ifftshift(fftShift)
	recon = np.fft.ifft2(fftShift)

	# compute the magnitude spectrum of the reconstructed image,
	# then compute the mean of the magnitude values
	magnitude = 20 * np.log(np.abs(recon))
	mean = np.mean(magnitude)
	# cv2.imshow('mag', magnitude.astype(np.int8))
	# cv2.waitKey(0)

	# the image will be considered "blurry" if the mean value of the
	# magnitudes is less than the threshold value
	return (mean, mean <= thresh)


def detect_blur_hsv(image, thresh=10):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	avg = np.mean(hsv[:,:, 2])
	return (avg, avg >= thresh)

count = 0
t_time_1280 = 0
t_time_640 = 0
blur_thres = 500
root = 'D:/datasets/MAAS_smart_pole'
# root = 'E:/datasets/maas_fogs'
# root = 'E:/datasets/maas_fogs/test'
scores = {}
scores_640 = {}
gaps = {}
for dir in os.listdir(root):
	dir2 = os.path.join(root, dir)
	if os.path.isdir(dir2):
		print(dir2)
		for file in glob(f'{dir2}/*.jpg'):
			img = cv2.imread(file)
			count+=1

			# rows, cols, c = img.shape
			# s_time = time.time()
			# score, blur = detect_blur_fft(img, thresh=blur_thres, vis=False)
			# t_time_1280+= time.time()-s_time
			# score = round(score, 1)
			# if score in scores:
			# 	scores[score]+=1
			# else:
			# 	scores[score]=1

			# im0 = img.copy()
			# if blur:
			# 	print(file, round(score, 1), sep=' ')
			# 	im0 = cv2.putText(im0, f'{score}', (10, 25), 0, 1, (255,0,0), thickness=2, lineType=cv2.LINE_AA)
			# 	filename = file.split("\\")[-1]
			# 	# cv2.imwrite(f'output/{dir_name}/{filename}', img)
			# 	cv2.imwrite(f'D:/yuting/output/fog_total_1280/{dir}-{filename}', im0)
				
			img = cv2.resize(img, (640,640))
			s_time = time.time()
			# score_640, blur = detect_blur_fft_cv2(img, thresh=blur_thres, vis=False)
			score_640, blur = detect_blur_fft(img, thresh=blur_thres, vis=False)
			t_time_640+= time.time()-s_time			
			score_640 = round(score_640, 1)
			im0 = img.copy()
			# if blur:
			# 	print(file, round(score_640, 1), sep=' ')
			# 	im0 = cv2.putText(im0, f'{score_640}', (10, 25), 0, 1, (255,0,0), thickness=2, lineType=cv2.LINE_AA)
			# 	filename = file.split("\\")[-1]
			# 	# cv2.imwrite(f'output/{dir_name}/{filename}', img)
			# 	cv2.imwrite(f'D:/yuting/output/fog_total_640/{dir}-{filename}', im0)
			if score_640 in scores_640:
				scores_640[score_640]+=1
			else:
				scores_640[score_640]=1
			# gap = round(abs(score - score_640), 1)
			# if gap in gaps:
			# 	gaps[gap]+=1
			# else:
			# 	gaps[gap]=1


			
		# print(f'1280 FPS: {count / t_time_1280}')
		print(f'640 FPS: {count / t_time_640}')
			
# print(scores)
print(scores_640)
				
# plt.bar(list(scores.keys()), list(scores.values()))
# plt.savefig(f'{root.split("/")[-1]}_scores_1280.png')
# plt.close()
plt.bar(list(scores_640.keys()), list(scores_640.values()))
plt.savefig(f'{root.split("/")[-1]}_scores_640.png')
plt.close()
# plt.bar(list(gaps.keys()), list(gaps.values()))
# plt.savefig(f'{root.split("/")[-1]}_gaps.png')
# plt.close()