from PIL import Image
import os, json

# Get supported formats from info.json
with open("info.json", "r") as info_file:
    info_data = json.load(info_file)
    supported_formats = info_data.get("supported_formats", [])

# Print process divider
def divide():
    print("\n" + "-" * 30 + "\n")

# Ask if user wants to make a subfolder
def make_subfolder():
    print("\nDo you want to create a subfolder? (Y/N)")
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
def overwrite_image():
    print("\nDo you want to overwrite the original image? (Y/N)")
    while True:
        overwrite = input("> ").strip().lower()
        if overwrite not in ["y", "n"]:
            print("\nInvalid Input. Please enter Y or N.")
            continue
        elif overwrite == "y":
            print("\nWarning: Overwriting original images might cause data loss.")
            return True
        else:
            return False

# Convert image to target format and save
def convert_and_save(input_file_path, output_folder, target_format):
    file_name, extension = os.path.splitext(os.path.basename(input_file_path))
    extension = extension.strip(".").lower()
    output_image_path = os.path.join(output_folder, f"{file_name}.{target_format}")
    # If the format of original image is same as target format: skip conversion
    if extension == target_format:
        return False
    try:
        with Image.open(input_file_path) as img:            
            if target_format in ["jpg", "jpeg"]:
                target_format = "jpeg"
                img = img.convert("RGB")
            img.save(output_image_path, format=target_format)
        return True
    except Exception as e:
        print(f"Error occured while converting {os.path.basename(input_file_path)}:"\
              f"\n{e}")
        return False

# Get the path of the folder where images are saved
def get_input_folder():
    print("Enter the path of the folder where original images are saved.")
    while True:
        input_folder = input("> ").strip().strip('"').strip("'")
        if not os.path.isdir(input_folder):
            print(f"Cannot find the folder from: {input_folder}\n")
            continue
        break
    return input_folder

# Get the path of the folder where converted images will be saved
def get_output_folder():
    print("\nEnter the output folder where converted images will be saved.")
    while True:
        output_folder = input("> ").strip().strip('"').strip("'")
        if output_folder in ["", "/"]:
            print("Cannot save converted images to the root directory.")
            continue
        break
    return output_folder

# Get target format
def get_target_format():
    print("\nEnter the target image format." \
    "\nEnter 'Formats' to see supported formats.")
    while True:
        target_format = input("> ").strip().strip(".").lower()
        if target_format == "formats":
            print(f"\n[ Supported Formats ]\n[ {', '.join(supported_formats).upper()} ]\n")
            continue
        elif target_format not in supported_formats:
            print(f"\nInvalid command or Unsupported format: {target_format}")
            continue
        break
    return target_format

# Run conversion
def run_convert():
    input_folder = get_input_folder()
    output_folder = get_output_folder()
    target_format = get_target_format()
    
    # Initialize a set to collect unique original extensions
    original_extensions = set()
    
    subfolder = make_subfolder()
    # If user wants to make a subfolder: make subfolder and save converted images there
    if subfolder == True:
        output_folder = os.path.join(output_folder, "Converted Images")
        os.makedirs(output_folder, exist_ok=True)
        divide()
        for file in os.listdir(input_folder):
            if file.lower().endswith(tuple(f".{format}" for format in supported_formats)):
                _, extension = os.path.splitext(file)
                input_image_path = os.path.join(input_folder, file)

                # Add only if conversion is actually performed
                if convert_and_save(input_image_path, output_folder, target_format):
                    original_extensions.add(extension[1:].upper())

    # If user does not want to make a subfolder: ask if overwrite original images
    else:
        overwrite = overwrite_image()            
        # If user wants to overwrite original images: save temporary converted images, delete original images, and rename temporary images
        if overwrite == True:
            divide()
            for file in os.listdir(input_folder):
                if file.lower().endswith(tuple(f".{format}" for format in supported_formats)):
                    original_name, extension = os.path.splitext(file)
                    input_image_path = os.path.join(output_folder, file)
                    temp_path = os.path.join(output_folder, f"{original_name}_temp.{target_format}")

                    try:
                        with Image.open(input_image_path) as img:
                            if target_format in ["jpg", "jpeg"]:
                                target_format = "jpeg"
                                img = img.convert("RGB")
                            img.save(temp_path, format=target_format)

                        # Replace original file with the new one
                        os.remove(input_image_path)
                        final_path = os.path.join(output_folder, f"{original_name}.{target_format}")
                        os.rename(temp_path, final_path)

                        # Add only if conversion is actually performed
                        if extension[1:].lower() != target_format:
                            original_extensions.add(extension[1:].upper())
                    except Exception as e:
                        print(f"Error during overwrite process for {file}: {e}")
                            
                # If user does not want to overwrite original images: convert and save (into the same folder, risking name conflicts)
                else:
                    print("\nWarning: If the target file already exists in this folder, the conversion will be skipped to prevent unexpected overwriting.")
                    divide()                
                    for file in os.listdir(input_folder):
                        if file.lower().endswith(tuple(f".{format}" for format in supported_formats)):
                            _, extension = os.path.splitext(file)
                            input_image_path = os.path.join(input_folder, file)
                            if convert_and_save(input_image_path, output_folder, target_format):
                                original_extensions.add(extension[1:].upper())
        else:
            divide()
            # Make output folder if it does not exist
            if not os.path.isdir(output_folder):
                os.makedirs(output_folder, exist_ok=True)

            for file in os.listdir(input_folder):
                if file.lower().endswith(tuple(f".{format}" for format in supported_formats)):
                    _, extension = os.path.splitext(file)
                    input_image_path = os.path.join(input_folder, file)
                    if convert_and_save(input_image_path, output_folder, target_format):
                        original_extensions.add(extension[1:].upper())

    unique_extensions = list(original_extensions)
    sort_order = [format.upper() for format in supported_formats]
    sorted_extensions = sorted(unique_extensions, key=lambda x: sort_order.index(x) if x in sort_order else len(sort_order))
    output_extensions_str = ', '.join(sorted_extensions)

    print("Successfully Converted!")
    print(f"{output_extensions_str.upper()} --> {target_format.upper()}")