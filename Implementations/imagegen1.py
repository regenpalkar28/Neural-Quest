from diffusers import StableDiffusionPipeline
import torch
import cv2  
import numpy as np

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")


prompt = "a cat wearing a cowboy hat in a desert, orange-reddish sand"

image = pipe(prompt).images[0]  

# Convert to NumPy array for OpenCV
image_np = np.array(image)[:, :, ::-1]  

# Show image using OpenCV
cv2.imshow("Generated Image", image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()
