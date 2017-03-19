> Something was wrong about I told you before about CTF. And here is the right summary.



### Related  terms

* Point spread function(PSF)
* Contrast transfer function(CTF)
* Fourier transform



1. Point spread function: It represent how a single particle looks like in an EM photo. Namely, PSF tell us how an image is.

   $I = O \ast PSF$

   $I$ is image, $O$ is object in sample, $\ast$ means convolution 

   If we use $\mathscr{F}\left\{ \right\}$  means Fourier transform, and the formula above will be

   $\mathscr{F}\left\{ I\right\}=\mathscr{F}\left\{O \right\}\cdot\mathscr{F}\left\{ PSF\right\}=\mathscr{F}\left\{O\right\}\cdot CTF$

   $\cdot$ means multiplication. 

   And it's clearly give out the definition of $CTF$. 

   ​

2. Contrast transfer function: 

   Is Fourier transformation of PSF, and vice versa.

   Finally, we can obtain the formula below:

   $I=\mathscr{F}^{-1}\left[\mathscr{F}\left\{O\right\}\cdot CTF\right]$

   This is how the EM process an image and finally output a .mrc file.

   ​

> Now what we need to do is reverse the computation above and obtain the $O$ which represent the structure of a particle.



3. Fourier transformation for image processing

   In this project, we just deal with the 2D Fourier transformation.

   [See some not-so-important detail here](https://www.cs.unm.edu/~brayer/vision/fourier.html)

   It seems that both Numpy and opencv have function to do something about that.

   [See documentation here](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html)

### Image processing

[See some tutorials here](http://www.msg.ucsf.edu/local/programs/eman/ctfc/ctfc.html)

1. Compute $CTF$

   Use CTFFIND3 or 4 to compute CTF

   [CTFFINDx software](http://grigoriefflab.janelia.org/ctf) But it seems hard to use, because it needs .mrc file as input, maybe we have to split a large .mrc file into a bunch of small ones.


2. Apply Fourier transformation towards .mrc file 

   Maybe it is right to use functions in opencv or numpy. But I'm not sure about that, probably there will be something wrong.

3. Obtain the object $O$

   $O=\mathscr{F}^{-1}\left[\frac{\mathscr{F}\left\{I\right\}}{CTF}\right]$

   I'm sure it is hard in this step.



### Clustering

I'm not sure how to do this, but we may need a good scoring step in k-means. 

