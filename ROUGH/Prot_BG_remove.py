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

BG_color = img[(10,5)]

lower = BG_color[:3] - 20
upper = BG_color[:3] + 20

mask = cv2.inRange(img[:,:,:3], lower, upper)

img[:,:,3][mask==255] = 0

cv2.imwrite(prot_sprite, img)
print("\nBackground of protagonist.png removed.")
