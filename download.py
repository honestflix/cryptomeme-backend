from diffusers import StableDiffusionPipeline

model_id = "stabilityai/stable-diffusion-2-1"
local_path = "./stable-diffusion-2-1"

pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token="your_huggingface_access_token_here")
pipe.save_pretrained(local_path)
