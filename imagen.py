from diffusers import AutoPipelineForText2Image
import torch
from datetime import datetime
from PIL import Image

pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
pipe.to("mps")

def generate_image(prompt):
    global pipe

    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    image.save(filename)
    
    return filename

