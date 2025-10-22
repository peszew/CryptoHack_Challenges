import os
from PIL import Image
import numpy as np


image1_path = 'flag.png'
image2_path = 'lemur.png'
output_path = 'xored.png'

def xor_images(img1_path, img2_path, output_path):
    
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')
    
    if img1.size != img2.size:
        raise ValueError('Images must be the same size')
    
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    
    xor_arr = np.bitwise_xor(arr1, arr2)
    xor_img = Image.fromarray(xor_arr.astype('uint8'), 'RGB')
    xor_img.save(output_path)
    print(f'Revealed image saved to: {output_path}')

if __name__ == '__main__':
    xor_images(image1_path, image2_path, output_path)