import os
import cv2
import numpy as np
import NPC_info


char_num = NPC_info.character_num

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')
for NPC in range(char_num):
    NPC_sprite = os.path.join(character_path, f'NPC_{NPC+1}.png')

    img = cv2.imread(NPC_sprite)

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

    cv2.imwrite(NPC_sprite, img)
    print(f"\nBackground of NPC_{NPC+1}.png removed.")
