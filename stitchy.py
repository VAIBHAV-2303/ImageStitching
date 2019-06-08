import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

def sifty(Im1, Im2):
	# Computing sift features and corresponding keypoint locations
	sift = cv2.xfeatures2d.SIFT_create(300)
	kp1, desc1 = sift.detectAndCompute(Im1, None)
	kp2, desc2 = sift.detectAndCompute(Im2, None)	
	
	# Sift matching between 2 images using ratio testing
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(desc1, desc2, k=2)
	good = []
	for m,n in matches:
	    if m.distance < 0.5*n.distance:
	        good.append(m)

	# Sorting by distance
	good = sorted(good, key = lambda x: x.distance)

	# Match plot
	# img3 = cv2.drawMatches(I1, kp1, I2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
	# plt.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
	# plt.show()

	return kp1, kp2, good

# Reading the images
I1 = cv2.imread(sys.argv[1])
I2 = cv2.imread(sys.argv[2])

# Finding sift features and matches
kp1, kp2, good = sifty(I1, I2)

# Finding corresponding points in both images
pts_src = []
pts_dst = []
for i in range(len(good)):
	pts_src.append([kp2[good[i].trainIdx].pt[0], kp2[good[i].trainIdx].pt[1]])
	pts_dst.append([kp1[good[i].queryIdx].pt[0], kp1[good[i].queryIdx].pt[1]])

# Calculating the homography matrix
pts_src = np.array(pts_src)
pts_dst = np.array(pts_dst)
h, status = cv2.findHomography(pts_src, pts_dst)

# Changing the plane of the right image
warped = cv2.warpPerspective(I2, h, (3*I2.shape[1], I2.shape[0]))
# plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
# plt.show()

# Sift features and a matching point for the warped image and left image
kp1, kp2, good = sifty(I1, warped)
best_match = good[0]
left_img_pos = np.floor(kp1[best_match.queryIdx].pt).astype(np.int64)
right_img_pos = np.floor(kp2[best_match.trainIdx].pt).astype(np.int64)
warped = warped[:, right_img_pos[0]+1:, :]

# Creating the final image
Window = 100
final = np.zeros([I1.shape[0]+Window, 3*I1.shape[1], 3], np.uint8)
final[(Window//2):I1.shape[0]+(Window//2), :left_img_pos[0], :] = I1[:, :left_img_pos[0], :]
final[(Window//2)-right_img_pos[1]+left_img_pos[1]:(Window//2)-right_img_pos[1]+left_img_pos[1]+warped.shape[0], left_img_pos[0]:left_img_pos[0]+warped.shape[1], :] = warped[:, :, :]

# Smoothening the seam using alpha featheering
left_window = I1[:, left_img_pos[0]:I1.shape[1], :].astype(np.float64)
right_window = final[(Window//2):I1.shape[0]+(Window//2), left_img_pos[0]:I1.shape[1], :].astype(np.float64)

for i in range(left_window.shape[1]):
	left_window[:, i, :] *= (1-(i/left_window.shape[1]))

for i in range(right_window.shape[1]):
	right_window[:, i, :] *= (i/right_window.shape[1])

final[(Window//2):I1.shape[0]+(Window//2), left_img_pos[0]:I1.shape[1], :] = left_window.astype(np.uint8)+right_window.astype(np.uint8)

# Removing the black boundary
final = final[(Window//2):I1.shape[0]+(Window//2), :, :]

# Plotting
cv2.imwrite('merged.jpg', final)
plt.subplot(221)
plt.imshow(cv2.cvtColor(I1, cv2.COLOR_BGR2RGB))
plt.subplot(222)
plt.imshow(cv2.cvtColor(I2, cv2.COLOR_BGR2RGB))
plt.subplot(212)
plt.imshow(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))
plt.show()