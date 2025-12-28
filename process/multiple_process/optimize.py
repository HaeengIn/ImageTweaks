from PIL import Image
import os, json

with open("info.json", "r") as info_file:
    info_data = json.load(info_file)
    unusable_symbols = info_data.get("unusable_symbols", [])

# Print divider
def divide():
    print("\n" + "-" * 30 + "\n")

# Ask is user wants to make a subfolder
def make_subfolder():
    print("\nDo you want to make a subfolder? (Y/N)")
    while True:
        subfolder = input("> ").strip().lower()
        if subfolder not in ["y", "n"]:
            print("\nInvalid Input. Please enter Y or N.")
            continue
        elif subfolder == "y":
            return True
        else:
            return False

# Ask if user wants to overwrite original images
def overwrite_original():
    print("\nDo you want to overwrite the original image? (Y/N)")
    while True:
        overwrite = input("> ").strip().lower()
        if overwrite not in ["y", "n"]:
            print("\nInvalid Input. Please enter Y or N.")
            continue
        elif overwrite == "y":
            return True
        else:
            return False

# Get the path of folder where original images are saved
def get_input_folder():
    print("Enter the path of folder where original images are saved.")
    while True:
        input_folder = input("> ").strip().strip('"')
        if not os.path.isdir(input_folder):
            print(f"Cannot find the folder from: {input_folder}\n")
            continue
        break
    return input_folder

# Get the path of folder where optimized images will be saved
def get_output_folder():
    print("\nEnter the output folder where optimized images will be saved.")
    while True:
        output_folder = input("> ").strip().strip('"').strip("'")
        if output_folder in unusable_symbols:
            print(f"\nCannot save optimized images to \"{output_folder}\"." \
                  "\nPlease check the name of folder." \
                    "Enter 'Info' on main menu to check which symbols are unusable.")
            continue
        break
    return output_folder

# Get the integer value of quality from user
def get_quality():
    print("\nEnter the quality of optimized images. (0 ~ 100)")
    while True:
        quality = input("> ").strip()
        try:
            quality = int(quality)
            if 0 <= quality <= 100:
                return quality
            else:
                print("\nInvalid Input. Please enter a integer value between 0 and 100.")
                continue
        except ValueError:
            print("Please enter a INTEGER value between 0 and 100.")
            continue

# Optimize and save images
def optimize_and_save(input_image_path, output_image_path, quality):
    try:
        with Image.open(input_image_path) as img:
            _, extension = os.path.splitext(input_image_path)
            extension = extension.strip(".").lower()
            if extension in ["jpg", "jpeg"]:
                if img.mode in ["RGBA", "P"]:
                    img = img.convert("RGB")
                img.save(output_image_path, quality=quality, optimize=True, format="jpeg")
            elif extension == "png":
                compress_level = 9 - int(quality / 100 * 9) # Convert quality to 0 ~ 9
                print("\nSince the PNG format does not support quality factors, it is natural that the compressed image size will be similar whether you enter a high or low integer.")
                img.save(output_image_path, compress_level=compress_level, optimize=True, format="png")
            elif extension == "webp":
                method = min(6, max(0, round(quality / 100 * 6)))
                img.save(output_image_path, quality=quality, method=method, optimize=True, format="webp")
            else:
                pass
    except Exception as e:
        print(f"\nError occured while optimizing image: {e}")

# Run optimization
def run_optimize():
    pass