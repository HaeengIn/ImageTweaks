from PIL import Image
import os

def print_divider():
    print()
    print("-" * 30)

# Convert image to target format and save
def convert_and_save(input_folder, output_folder, target_format):
    pass

# Get the path of the folder where images are saved
def get_input_folder():
    pass

# Get the path of the folder where converted images will be saved
def get_output_folder():
    pass

# Get target format
def get_target_format():
    print("\nEnter the target image format.")

# Run conversion
def run_convert():
    input_folder = get_input_folder()
    output_folder = get_output_folder()
    target_format = get_target_format()

    # If the path of input folder and out folder are same: ask if overwirte original images
    if os.path.dirname(input_folder) == os.path.dirname(output_folder):
        print("Do you want to overwrite original images? (Y/N)")
        while True:
            overwrite = input("> ").strip().lower()
            if overwrite not in ["y", 'n']:
                print("Invalid Input. Please enter Y or N")
                continue
            break

        # If user wants to overwrite original images: save temporary converted images, delete original images, and rename temporary images
        if os.path.dirname(input_folder) == os.path.dirname(output_folder):
            pass

        # If user does not want to overwrite original images: save converted images
        else:
            print_divider()
            convert_and_save(input_folder, output_folder, target_format)