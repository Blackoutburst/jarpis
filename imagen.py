import torch
from datetime import datetime
from PIL import Image
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "cagliostrolab/animagine-xl-4.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    custom_pipeline="lpw_stable_diffusion_xl",
    add_watermarker=False
)
pipe.to("mps")

negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry"

def generate_image(prompt):
    global base
    global refiner
    global negative_prompt

    image = pipe(
        prompt = prompt + ", masterpiece, high score, great score, absurdres",
        negative_prompt=negative_prompt,
        width=832,
        height=1216,
        guidance_scale=5,
        num_inference_steps=28
    ).images[0]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    image.save(filename)
    
    return filename
