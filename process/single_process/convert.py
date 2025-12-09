from PIL import Image
import os

# Convert image to target format and save
def convert_and_save(input_image_path, output_folder, target_format):
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    output_image_path = os.path.join(output_folder, f"{base_name}.{target_format}")

    with Image.open(input_image_path) as img:
        if target_format in ["jpg", "jpeg"]:
            img = img.convert("RGB")

        img.save(output_image_path, format=target_format)

def get_input_image_path():
    print("Enter the path of the original image.")
    while True:
        input_image_path = input("> ").strip().strip('"').strip("'").lower()
        if not os.path.isfile(input_image_path):
            print(f"Cannot find the original file from: {input_image_path}")
            continue
        break
    return input_image_path

def get_output_folder():
    print("Enter the output folder where converted image will be saved.")
    while True:
        output_folder = input("> ").strip().strip('"').strip("'")
        if output_folder in ["", "/"]:
            print("Cannot save converted image to the root directory.")
            continue
        break
    return output_folder

def get_target_format():
    print("Enter the target image format.\n" \
    "Enter 'Formats' to see supported formats.")
    while True:
        target_format = input("> ").strip().strip(".").lower()
        if target_format == "formats":
            print("[ Supported Formats ]\n"
            "[ JPG, JPEG, PNG, WEBP ]")
            continue
        if target_format not in ["png", "jpg", "jpeg", "webp"]:
            print(f"Invalid command or Unsupported format: {target_format}")
            continue
        break
    return target_format

def run_convert():
    input_image_path = get_input_image_path()
    output_folder = get_output_folder()
    target_format = get_target_format()

    input_folder = os.path.dirname(input_image_path)
    original_extension = os.path.splitext(input_image_path)[1].strip(".").lower()

    # If the folder of original image and output folder are the same: ask if overwirte original image
    if input_folder == output_folder:
        print("Do you want to overwrite the original image? (Y/N)")
        while True:
            overwrite = input("> ").strip().lower()
            if overwrite not in ["y", "n"]:
                print("Invalid Input. Please enter Y or N.")
                continue
            break

        original_name, _ = os.path.splitext(os.path.basename(input_image_path))

        # If user wants to overwrite original image: save converted image as temporary, delete original image, and rename temporary image
        if overwrite == "y":
            temp_path = os.path.join(output_folder, f"{original_name}_temp.{target_format}")

            with Image.open(input_image_path) as img:
                if target_format in ["jpg", "jpeg"]:
                    img = img.convert("RGB")
                img.save(temp_path, format=target_format)

            os.remove(input_image_path)
            final_path = os.path.join(output_folder, f"{original_name}.{target_format}")
            os.rename(temp_path, final_path)

        # If user does not want to overwrite original image: convert and save to output folder
        else:
            convert_and_save(input_image_path, output_folder, target_format)

    # If the folder of original image and output folder are different: convert and save to output folder
    else:
        convert_and_save(input_image_path, output_folder, target_format)

    print("Successfully Converted!")
    print(f"{original_extension} --> {target_format}")