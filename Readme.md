# Seamless Multiple Image-Stitching

## Description

An Image-stitching algorithm which uses SIFT features to find matches between the images and then compute the homography matrix. Using this matrix, the to_be_added image is aligned in the plane of the root image and merged accordingly. This code is capable of merging multiple images present in any orientation and ordering. The result is displayed in stages, similar to how a puzzle is completed, by adding one image at a time. 

## How To

* Run the code: 	
	```console
	bar@foo:~$ jupyter notebook
	```

## Built With

* [Python3](https://www.python.org/download/releases/3.0/)
* [OpenCV](https://docs.opencv.org/3.0-beta/index.html)
* [Jupyter](https://jupyter.org/)

## Author

* Vaibhav Garg

