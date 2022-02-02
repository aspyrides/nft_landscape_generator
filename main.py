from PIL import Image
import random
import os
import numpy as np

# SET PARAMETERS
TOTAL_IMAGES = 100 # Number of random unique images we want to generate
input_dir = "./layers"
output_dir = "./images"


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

bottom = ["concrete1", "concrete2", "dirt1", "dirt2", "dirt3", "dirt4",
"dirt5", "grass1", "grass2", "grass3", "mars1", "mars2", "sand1", "sand2"]
bottom_weights = [6, 6, 10, 10, 7, 7, 8, 11, 10, 10, 2, 2, 6, 5]
#checks
len(bottom) == len(bottom_weights)
np.sum(bottom_weights)

top = ["moon_star1", "moon_star2", "moon_star3", "sky_sun_clouds1",
"sky_sun_clouds2", "sky_sun1"]
#checks
top_weights = [10, 19, 17, 20, 18, 16]
len(top) == len(top_weights)
np.sum(top_weights)

middle = ["grass_mid1", "grass_trees1", "pond1", "sea1", "sea2"]
middle_weights = [22, 15, 18, 22, 23]
#checks
len(middle) == len(middle_weights)
np.sum(middle_weights)



bottom_files = {
    "concrete1": "concrete1",
    "concrete2": "concrete2",
    "dirt1": "dirt1",
    "dirt2": "dirt2",
    "dirt3": "dirt3",
    "dirt4": "dirt4",
    "dirt5": "dirt5",
    "grass1": "grass1",
    "grass2": "grass2",
    "grass3": "grass3",
    "mars1": "mars1",
    "mars2": "mars2",
    "sand1": "sand1",
    "sand2": "sand2"
}

top_files = {
    "moon_star1": "moon_star1",
    "moon_star2": "moon_star2",
    "moon_star3": "moon_star3",
    "sky_sun_clouds1": "sky_sun_clouds1",
    "sky_sun_clouds2": "sky_sun_clouds2",
    "sky_sun1": "sky_sun1"
}

middle_files = {
    "grass_mid1": "grass_mid1",
    "grass_trees1": "grass_trees1",
    "pond1": "pond1",
    "sea1": "sea1",
    "sea2": "sea2"
}




## Generate Traits
all_images = []

# A recursive function to generate unique image combinations
def create_new_image():

    new_image = {} #

    # For each trait category, select a random trait based on the weightings
    new_image["Bottom"] = random.choices(bottom, bottom_weights)[0]
    new_image["Top"] = random.choices(top, top_weights)[0]
    new_image["Middle"] = random.choices(middle, middle_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):

    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))
# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = f"landscape_id_{i}"
    i = i + 1


# check actual traits in all_images
bottom_count = {}
for item in bottom:
    bottom_count[item] = 0

top_count = {}
for item in top:
    top_count[item] = 0

middle_count = {}
for item in middle:
    middle_count[item] = 0


for image in all_images:
    bottom_count[image["Bottom"]] += 1
    top_count[image["Top"]] += 1
    middle_count[image["Middle"]] += 1



# create image and save
if(not os.path.exists(f'{output_dir}')):
    os.mkdir(f'{output_dir}')

for item in all_images:

    im1 = Image.open(f'{input_dir}/bottom/{bottom_files[item["Bottom"]]}.png').convert('RGBA')
    im2 = Image.open(f'{input_dir}/top/{top_files[item["Top"]]}.png').convert('RGBA')
    im3 = Image.open(f'{input_dir}/middle/{middle_files[item["Middle"]]}.png').convert('RGBA')

    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)

    #Convert to RGB
    rgb_im = com2.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save(f'{output_dir}/{file_name}')
