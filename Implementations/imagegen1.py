from diffusers import StableDiffusionPipeline
import torch
import cv2  
import numpy as np

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")


prompt = "a shark in the middle of a desert"

image = pipe(prompt).images[0]  

image_np = np.array(image)[:, :, ::-1]  


cv2.imshow("Generated Image", image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()
