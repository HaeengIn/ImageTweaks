from PIL import Image
import os, json

with open("info.json", "r", encoding="utf-8") as info_file:
    info_data = json.load(info_file)
    unusable_names = info_data.get("unusable_names", [])

# Print divider
def divide():
    print("\n" + "-" * 30 + "\n")

# Ask if user wants to make a subfolder
def make_subfolder():
    print("\nDo you want to make a subfolder?")
    while True:
        subfolder = input("> ").strip().lower()
        if subfolder not in ["y", "n"]:
            print("\nInvalid Input. Please enter Y or N.")
            continue
        if subfolder == "y":
            return True
        else:
            return False
        
# Ask if user wants to overwrite original image
def overwrite_original():
    print("\nDo you want to overwrite original image?")
    while True:
        overwrite = input("> ").strip().lower()
        if overwrite not in ["y", "n"]:
            print("\nInvalid Input. Please enter Y or N.")
            continue
        if overwrite == "y":
            print("\nWarning: overwritng image might cause unexpected loss")
            return True
        else:
            return False
        
# Get the path of original image from user
def get_input_image_path():
    print("Enter the path of original image.")
    while True:
        input_image_path = input("> ").strip().strip('"')
        if os.path.isfile(input_image_path):
            return input_image_path
        else:
            print(f"\nCannot find the image.\nPlease check the path: {input_image_path}\n")
            continue

# Get the path of output folder from user
def get_output_folder():
    print("\nEnter the path of the folder where optimized image will be saved.")
    while True:
        output_folder = input("> ").strip().strip('"')
        if output_folder in unusable_names:
            print("\nCannot save at Root Folder. Please enter other path of folder.")
            continue
        elif os.path.splitext(output_folder)[1] != "":
            print("\nPlease enter a FOLDER path, not a file path.")
            continue
        else:
            return output_folder
        
# Get the integer value of quality from user
def get_quality():
    print("\nEnter the quality of your optimized image. (0 ~ 100)")
    while True:
        quality = input("> ").strip()
        try:
            quality = int(quality)
            if 0 <= quality <= 100:
                return quality
            else:
                print("Invalid Input. Please enter a integer value between 0 and 100.")
                continue
        except ValueError:
            print("Please enter a INTEGER value between 0 and 100.")
            continue

# Optimize and save image
def optmimize_and_save(input_image_path, output_image_path, quality):
    try:
        with Image.open(input_image_path) as img:
            _, extension = os.path.splitext(input_image_path)
            extension = extension.strip(".").lower()
            if extension in ["jpg", "jpeg"]:
                if img.mode in ["RGBA", "p"]:
                    img = img.convert("RGB")
            elif extension == "png":
                quality = quality / 100 * 9 # Convert quality to 0 ~ 9
            else:
                quality = str(quality)
                quality = True
            img.save(output_image_path, quality)
    except Exception as e:
        print(f"\nError occured while optmizing image: {e}")

# Run optimization
def run_optimize():
    input_image_path = get_input_image_path()
    output_folder = get_output_folder()
    quality = get_quality()

    input_folder = os.path.dirname(input_image_path) # Get the name of folder which original image is saved
    original_name, extension = os.path.splitext(input_image_path)
    extension = extension.strip(".").lower()

    original_size = os.path.getsize(input_image_path) # Get the file size of original image.

    # If the original image's folder and output folder is same: ask if user wants to make a subfolder
    if os.path.abspath(input_folder) == os.path.abspath(output_folder):
        subfolder = make_subfolder()
        # If user wants to make a subfolder: make subfolder, optimize, and save image
        if subfolder == True:
            output_folder = os.path.join(output_folder, "Optimized Images")
            os.makedirs(output_folder, exist_ok=True)

            output_image_path = os.path.join(output_folder, f"{original_name}.{extension}")
            divide()
            optmimize_and_save(input_image_path, output_image_path, quality)
            optimized_size = os.path.getsize(output_image_path)
        # If user does not want to make a subfolder: ask if user wants to overwrite original image
        else:
            overwrite = overwrite_original()
            # If user wants to overwrite original image: save optimized image as temporary, delete original image, and rename temporary image
            if overwrite == True:
                output_image_path = os.path.join(output_folder, f"{original_name}_temp.{extension}") # Temporary path of optimized image
                divide()
                optmimize_and_save(input_image_path, output_image_path, quality)
                os.remove(input_image_path)
                final_output_image_path = os.path.join(input_folder, f"{original_name}.{extension}")
                os.rename(output_image_path, final_output_image_path)
                optimized_size = os.path.getsize(final_output_image_path)
            # If user does not want to overwrite original image: add "_optimized" to original image's name, optimize, and save
            else:
                output_image_path = os.path.join(output_folder, f"{original_name}_optimized.{extension}")
                optmimize_and_save(input_image_path, output_image_path, quality)
                optimized_size = os.path.getsize(output_image_path)
    # If the original image's folder and output folder is not same: make output foler, optimize, and save
    else:
        os.makedirs(output_folder, exist_ok=True)
        output_image_path = os.path.join(output_folder, f"{original_name}.{extension}")
        optmimize_and_save(input_image_path, output_image_path, quality)
        optimized_size = os.path.getsize(output_image_path)
    
    # Print success message and reduced bytes
    print("Successfully Optimized!")
    print(f"{original_size} bytes --> {optimized_size} bytes")