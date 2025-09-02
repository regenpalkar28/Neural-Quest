from diffusers import StableDiffusionPipeline
import pygame as pg
import os 
import cv2
import numpy as np

image_model_path = "CharGeneration/aziibpixelmix_v10.safetensors"  
image_dir = os.path.join(os.getcwd(), "Pygame Implementations", "Images")
pipe = StableDiffusionPipeline.from_single_file(image_model_path).to("cpu")

prompts_for_Knight = {
    # "front": "Pixel art knight holding a sword, front view, standing idle, single sprite, centered, background color RGB(27, 238, 21), RPG retro pixel style",
    # "back": "Pixel art knight holding a sword, back view, standing idle, single sprite, centered, background color RGB(27, 238, 21), RPG retro pixel style",
    "left": "Pixel art knight holding a sword, left facing view, standing idle, single sprite, centered, background color RGB(27, 238, 21), RPG retro pixel style"
}
bg_color = np.array([185,197, 207])
lower = bg_color - 10
upper = bg_color + 10

for view, prompt in prompts_for_Knight.items():
    image = pipe(prompt, height = 512, width=512, guidance_scale=7.5, num_inference_steps=30).images[0]

    filename = os.path.join(image_dir, f"knight_{view}.png")
    image.save(filename)
    print(f"Saved {filename}")

    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Failed to load {filename}")

    if img.shape[2] != 4:
        b, g, r = cv2.split(img)
        a = np.ones(b.shape, dtype=b.dtype) * 255
        img = cv2.merge((b, g, r, a))

        
    mask = cv2.inRange(img[:, :, :3], lower, upper)

    img[:, :, 3][mask == 255] = 0

    cv2.imwrite(filename, img)

screen = pg.display.set_mode((1000,700))
pg.display.set_caption('Walking')

player_front = pg.image.load('Pygame Implementations/Images/knight_front.png')
player_back = pg.image.load('Pygame Implementations/Images/knight_back.png')
player_left = pg.image.load('Pygame Implementations/Images/knight_left.png')


player_front = pg.transform.scale(player_front, (50,50))
player_back = pg.transform.scale(player_back, (50,50))
player_left = pg.transform.scale(player_left, (50,50))
player_right = pg.transform.flip(player_left, flip_x=True, flip_y=False)

speed = 5
x,y = 225, 225
player_rect = player_front.get_rect(topleft=(x, y))
clock = pg.time.Clock()

cat_img = pg.image.load("Pygame Implementations/Images/cat.png")
cat_img = pg.transform.scale(cat_img, (50, 50))
cat_rect = cat_img.get_rect(topleft=(400, 300))

def draw_dialog(screen, text):
    font = pg.font.SysFont("Arial", 24)
    dialog_box = pg.Rect(50, 600, 900, 80)  
    pg.draw.rect(screen, (255, 255, 255), dialog_box, border_radius=12)
    pg.draw.rect(screen, (0, 0, 0), dialog_box, 2, border_radius=12)

    dialog_text = font.render(text, True, (0, 0, 0))
    screen.blit(dialog_text, (dialog_box.x + 20, dialog_box.y + 25))
dialog_active = False

while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
            exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_a] and player_rect.x>0:
        player_rect.x-=speed
        current_player = player_left
    elif keys[pg.K_d] and player_rect.x<500- player_rect.width:
        player_rect.x+=speed
        current_player=player_right
    elif keys[pg.K_w] and player_rect.y > 0:
        player_rect.y -= speed
        current_player = player_back
    elif keys[pg.K_s] and player_rect.y < 500 - player_rect.height:
        player_rect.y += speed
        current_player = player_front
    else:
        current_player = player_front

    if player_rect.colliderect(cat_rect.inflate(10, 10)):  
        dialog_active = True
    else:
        dialog_active = False

    screen.fill((110, 200, 36))
    screen.blit(current_player, player_rect.topleft)
    screen.blit(cat_img, cat_rect.topleft)
    if dialog_active:
        draw_dialog(screen, "Meoww")

    pg.display.update()

    clock.tick(40)