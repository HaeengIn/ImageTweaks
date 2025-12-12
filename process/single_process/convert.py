from PIL import Image
import os

# Convert image to target format and save
def convert_and_save(input_image_path, output_folder, target_format):
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    output_image_path = os.path.join(output_folder, f"{base_name}.{target_format}")

    with Image.open(input_image_path) as img:
        if target_format in ["jpg", "jpeg"]:
            target_format = "JPEG"
            img = img.convert("RGB")

        img.save(output_image_path, format=target_format)

# Ask if user wants to make a subfolder
def make_subfolder():
    print("\nDo you want to create a subfolder? (Y/N)")
    while True:
        subfolder = input("> ").strip().lower()
        if subfolder not in ["y", "n"]:
            print("Invalid Input. Please enter Y or N.")
            continue
        elif subfolder == "y":
            return True
        else:
            return False

# Ask if user wants to overwrite original image
def overwrite_image():
    print("\nDo you want to overwrite the original image? (Y/N)")
    while True:
        overwrite = input("> ").strip().lower()
        if overwrite not in ["y", "n"]:
            print("Invalid Input. Please enter Y or N.")
            continue
        elif overwrite == "y":
            print("\nWarning: Overwriting original images might cause data loss.")
            return True
        else:
            return False

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
    print("\nEnter the output folder where converted image will be saved.")
    while True:
        output_folder = input("> ").strip().strip('"').strip("'")
        if output_folder in ["", "/"]:
            print("Cannot save converted image to the root directory.")
            continue
        break
    return output_folder

def get_target_format():
    print("\nEnter the target image format.\n" \
    "Enter 'Formats' to see supported formats.")
    while True:
        target_format = input("> ").strip().strip(".").lower()
        if target_format == "formats":
            print("\n[ Supported Formats ]\n"
            "[ JPG, JPEG, PNG, WEBP ]\n")
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
        subfolder = make_subfolder()
        if subfolder == True:
            os.makedirs(os.path.join(input_folder, "Converted Images"), exist_ok=True)
            output_folder = os.path.join(input_folder, "Converted Images")

            convert_and_save(input_image_path, output_folder, target_format)
        else:
            overwrite = overwrite_image()
            if overwrite == True:
                # 원본 파일 이름 추출하기
                # 임시 파일 이름 붙여서 저장하고
                # 원본 파일 삭제하고
                # 임시 파일 이름을 원본 파일 이름으로 변경하기

                original_name, _ = os.path.splitext(os.path.basename(input_image_path))
                temp_image_path = f"{original_name}_tmp.{target_format}"
                output_folder = os.path.join(input_folder, temp_image_path)
                convert_and_save(input_image_path, output_folder, target_format)

                os.remove(input_image_path)
                final_output_path = os.path.join(input_folder, f"{original_name}.{target_format}")
                os.rename(output_folder, final_output_path)
            else:
                # 그냥 저장하기
                convert_and_save(input_image_path, output_folder, target_format)
    else:
        os.makedirs(output_folder, exist_ok=True)
        convert_and_save(input_image_path, output_folder, target_format)

    print("Successfully Converted!")
    print(f"{original_extension} --> {target_format}")

"""
102 ~ 105 수정
conver_and_save 함수 수정
"""