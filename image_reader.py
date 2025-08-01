from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import easyocr

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("mps")

def read_image(image_input):
    global processor
    global model

    image = Image.open(image_input).convert("RGB")

    inputs = processor(image, return_tensors="pt").to("mps")

    with torch.no_grad():
        output = model.generate(**inputs, max_length=128, num_beams=5)

    caption = processor.decode(output[0], skip_special_tokens=True)

    reader = easyocr.Reader(['fr', 'en'], gpu=True)
    ocr_results = reader.readtext(image_input)

    visible_texts = [text for (_, text, _) in ocr_results]
    ocr_text = "\n".join(visible_texts)

    nothing = "No text detected."
    return f">>>\nDescription:\n{caption}\n\n---\n\nText:\n{ocr_text if ocr_text else nothing}\n<<<"

