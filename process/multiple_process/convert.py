from PIL import Image
import os, json

def print_divider():
    print()
    print("-" * 30)

# Convert image to target format and save
def convert_and_save(input_folder, output_folder, target_format):
    file_name = os.path.splitext(os.path.basename(input_folder))[0]
    output_image_path = os.path.join(output_folder, f"{file_name}.{target_format}")

    with Image.open(input_folder) as img:
        if target_format in ["jpg", "jpeg"]:
            target_format = "JPEG"
            img = img.convert("RGB")

        img.save(output_image_path, format=target_format)

# Get the path of the folder where images are saved
def get_input_folder():
    print("Enter the path of the folder where original images are saved.")
    while True:
        input_folder = input("> ").strip().strip('"').strip("'")
        if not os.path.isdir(input_folder):
            print(f"Cannot find the folder from: {input_folder}")
            continue
        break
    return input_folder

# Get the path of the folder where converted images will be saved
def get_output_folder():
    print("Enter the output folder where converted images will be saved.")
    while True:
        output_folder = input("> ").strip().strip('"').strip("'")
        if output_folder in ["", "/"]:
            print("Cannot save converted images to the root directory.")
            continue
        break
    return output_folder

# Get target format
def get_target_format():
    with open("info.json", "r") as info_file:
        info_data = json.load(info_file)

    supported_formats = info_data.get("supported_formats", [])

    print("\nEnter the target image format." \
    "Enter 'Formats' to see supported formats.")
    while True:
        target_format = input("> ").strip().strip(".").lower()
        if target_format == "formats":
            print(f"\n[ Supported Formats ]\n[ {', '.join(supported_formats).upper()} ]")
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

    # If the path of input folder and out folder are same: ask if make subfolder
    if os.path.dirname(input_folder) == os.path.dirname(output_folder):
        print("Do you want to make a subfolder? (Y/N)")
        while True:
            subfolder = input("> ").strip().lower()
            if subfolder not in ["y", "n"]:
                print("Invalid Input. Please enter Y or N")
                continue
            break

        # If user wants to make a subfolder: make subfolder and save converted images there
        if subfolder == "y":
            os.makedirs(os.path.join(output_folder, "Converted_Images"), exist_ok=True)
            output_folder = os.path.join(output_folder, "Converted_Images")

            print_divider()

            for file in os.listdir(input_folder):
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    input_image_path = os.path.join(input_folder, file)
                    convert_and_save(input_image_path, output_folder, target_format)

        # If user does not want to make a subfolder: ask if overwrite original images
        else:
            print("Do you want to overwrite the original images? (Y/N)")
            while True:
                overwrite = input("> ").strip().lower()
                if overwrite not in ["y", "n"]:
                    print("Invalid Input. Please enter Y or N")
                    continue
                break
            
            # If user wants to overwrite original images: save temporary converted images, delete original images, and rename temporary images
            if overwrite == "y":
                print_divider()

                for file in os.listdir(input_folder):
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        input_image_path = os.path.join(output_folder, file)

                        original_name, _ = os.path.splitext(os.path.basename(input_image_path))
                        temp_path = os.path.join(output_folder, f"{original_name}_temp.{target_format}")

                        with Image.open(input_image_path) as img:
                            if target_format in ["jpg", "jpeg"]:
                                target_format = "JPEG"
                                img = img.convert("RGB")
                            img.save(temp_path, format=target_format)

                        os.remove(input_image_path)
                        final_path = os.path.join(output_folder, f"{original_name}.{target_format}")
                        os.rename(temp_path, final_path)
            
            # If user does not want to overwrite original images: convert and save
            else:
                print_divider()

                for file in os.listdir(input_folder):
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        input_image_path = os.path.join(input_folder, file)
                        convert_and_save(input_image_path, output_folder, target_format)

    # If the path of input folder and out folder are different: convert and save
    else:
        print_divider()

        if not os.path.isdir(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(input_folder):
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                input_image_path = os.path.join(input_folder, file)
                convert_and_save(input_image_path, output_folder, target_format)

    print("Successfully Converted!")
    print(f"{original_extensions.upper()} --> {target_format.upper()}")
    """
    original_extensions 리스트 만들고 각 파일들 스캔하면서 확장자 추가하기.
    이미 있는 확장자면 추가 X
    정렬은 JPG, JPEG, PNG, WEBP 순으로
    마지막에 ', '로 join 해서 출력
    """