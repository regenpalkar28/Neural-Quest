import os
import cv2
import numpy as np

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')
prot_sprite = os.path.join(character_path, 'protagonist.png')

img = cv2.imread(prot_sprite)

if img.shape[2] != 4:
    b, g, r = cv2.split(img)
    # alpha channel
    a = np.ones(b.shape, dtype=b.dtype)*255
    img = cv2.merge((b,g,r,a))

BG_region = img[0:10, 0:10, :3].astype(np.float32)
BG_color = BG_region.mean(axis=(0,1))

diff = img[:, :, :3].astype(np.float32) - BG_color
dist = np.linalg.norm(diff, axis=2)

tolerance = 30  
mask = dist < tolerance

img[mask, 3] = 0

cv2.imwrite(prot_sprite, img)
print("\nBackground of protagonist.png removed.")
