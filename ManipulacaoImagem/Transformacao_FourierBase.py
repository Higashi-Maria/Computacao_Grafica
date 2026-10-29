import io
import cv2
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\Maria\Desktop\CG\sheep.jpeg"
image = np.array(Image.open(path))

# Write your code below
grey_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

dft = np.fft.fft2(grey_image)
dft_shift = np.fft.fftshift(dft)

magnitude_spectrum = 20* np.log(np.abs(dft_shift) + 1)

# Display the results
plt.figure(figsize=(10,10))

plt.subplot(2,1,1)
plt.imshow(grey_image, cmap='gray')

plt.subplot(2,1,2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.show()