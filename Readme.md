# Feature Based Seamless Image Stitching

## Description

An image stitching algorithm which uses SIFT features to find matches between the images and then compute the homography matrix. Then the right image is aligned in the plane of the left image. Then again using SIFT features matching, the 2 images are blended and finally to smooth the seam generated between the 2 images, alpha feathering is used.

## How To

* Run the game: 	
	```console
	bar@foo:~$ python3 stitchy.py <path to left image> <path to right image>
	```
The output will also be saved in 'merged.jpg' in the current directory. Few sample images for testing purposes are also included in this directory.

## Built With

* [Python3](https://www.python.org/download/releases/3.0/)
* [OpenCV](https://docs.opencv.org/3.0-beta/index.html)

## Author

* Vaibhav Garg

