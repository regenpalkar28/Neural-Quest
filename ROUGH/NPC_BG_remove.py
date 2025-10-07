import os
import cv2
import numpy as np

char_num = 5

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')
BG_COLOR = []

for NPC in range(char_num):
    NPC_sprite = os.path.join(character_path, f'NPC_{NPC+1}.png')

    img = cv2.imread(NPC_sprite)

    if img.shape[2] != 4:
        b, g, r = cv2.split(img)
        # alpha channel
        a = np.ones(b.shape, dtype=b.dtype)*255
        img = cv2.merge((b,g,r,a))

    BG_REGION = img[0:10, 0:10, :3]
    BG_COLOR.append(BG_REGION.mean(axis=(0,1)))

    diff = img[:, :, :3].astype(np.float32) - BG_COLOR[NPC]
    dist = np.linalg.norm(diff, axis=2)

    tolerance = 30
    mask = dist < tolerance

    img[mask, 3] = 0

    cv2.imwrite(NPC_sprite, img)
    print(f"\nBackground of NPC_{NPC+1}.png removed.")

print(BG_COLOR)