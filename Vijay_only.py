import os
import shutil
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses warnings and errors

from deepface import DeepFace

# Define paths
dataset_folder = "Vijay_HDimages"  # Folder containing 900+ images
output_folder = "selected_vijay_images"  # Folder to store Actor Vijay's images
reference_image = "vijay.jpg"  # A clear image of Actor Vijay

# Create output folder if not exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
selected_count = 0  # Counter for Vijay's images

# Iterate through images in the dataset
for file in os.listdir(dataset_folder):
    img_path = os.path.join(dataset_folder, file)

    try:
        # Verify if the face matches with Vijay's reference image
        result = DeepFace.verify(img_path, reference_image, model_name="ArcFace", enforce_detection=False)

        if result["verified"]:  # If DeepFace identifies the person as Vijay
            shutil.copy(img_path, output_folder)
            selected_count += 1
            #print(f"Selected: {file}")

    except Exception as e:
        print(f"Skipping {file}: {e}")
# Count total images in output folder
output_count = len(os.listdir(output_folder))
print(f"Filtering completed. {output_count} Vijay images saved in '{output_folder}' folder.")

#print("Filtering completed. Vijay's images are saved in the 'vijay_images' folder.")
