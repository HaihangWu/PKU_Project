import os

import torch
from vggt.models.vggt import VGGT
from vggt.utils.load_fn import load_and_preprocess_images

#os.environ['HF_HOME']='/root/autodl-tmp/cache/'

device = "cuda" if torch.cuda.is_available() else "cpu"
# bfloat16 is supported on Ampere GPUs (Compute Capability 8.0+)
dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16

# Initialize the model and load the pretrained weights.
# This will automatically download the model weights the first time it's run, which may take a while.
#model = VGGT.from_pretrained("facebook/VGGT-1B").to(device)

model=VGGT()
checkpoint_path="/root/autodl-tmp/pretrained_models/VGGT/model.pt"
state_dict=torch.load(checkpoint_path, map_location=device)
model.load_state_dict(state_dict)
model.to(device)  # move model and all its parameters to device

# Load and preprocess example images (replace with your own image paths)
#image_names = ["/root/data/NRGBD/breakfast_room/images/img0.png"]
image_dir="/root/autodl-tmp/data/NRGBD/breakfast_room/images/" #"/root/autodl-tmp/PKU_Project/VGGT/examples/llff_fern/images/" #
image_names = [os.path.join(image_dir,f) for f in os.listdir(image_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

images = load_and_preprocess_images(image_names).to(device)

with torch.no_grad():
    with torch.cuda.amp.autocast(dtype=dtype):
        # Predict attributes including cameras, depth maps, and point maps.
        predictions = model(images)