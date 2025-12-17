import os
from PIL import Image

# Get input folder path from user
def get_input_folder_path():
    while True:
        print("Enter the path of folder where original images are saved")
        path = input("> ").strip().strip('"')

        if os.path.isdir(path):
            return path
        else:
            print(f"Invalid Input. Cannot find the folder: {path}")

# Get output folder path from user
def get_output_folder_path():
    print("\nEnter the path of folder where optimized images will be saved")
    path = input("> ").strip().strip('"')
    return path

# Get optimization quality
def get_optimization_quality():
    while True:
        print("\nEnter the optimization quality (0 ~ 100)")
        value = input("> ").strip()

        if value.isdigit():
            value = int(value)
            if 0 <= value <= 100:
                return value
            else:
                print("Invalid Input. Quality must be between 0 and 100.")
        else:
            print("Invalid Input. Please enter an integer between 0 and 100.")

# Ask user Y/N
def ask_yes_no(question):
    while True:
        print(question)
        choice = input("> ").strip().lower()

        if choice in ["y", "n"]:
            return choice
        else:
            print("Invalid Input. Please enter Y or N")

# Optimize and save image
def optimize_image(input_path, output_path, quality):
    img = Image.open(input_path)
    img.save(output_path, optimize=True, quality=quality)

# Calculate total size of images in a folder
def calculate_total_size(folder_path):
    total = 0
    for file in os.listdir(folder_path):
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            full_path = os.path.join(folder_path, file)
            total += os.path.getsize(full_path)
    return total

# Main process
def run_optimize():
    input_folder_path = get_input_folder_path()
    output_folder_path = get_output_folder_path()
    optimization_quality = get_optimization_quality()

    same_folder = (os.path.abspath(input_folder_path) == os.path.abspath(output_folder_path))

    use_subfolder = None
    delete_originals = None
    save_folder = output_folder_path

    # If both folders are the same
    if same_folder:
        use_subfolder = ask_yes_no("\nDo you want to create a subfolder? (Y/N)")
        if use_subfolder == "y":
            save_folder = os.path.join(input_folder_path, "Optimized Images")
        else:
            delete_originals = ask_yes_no("\nDo you want to delete original images? (Y/N)")
            save_folder = input_folder_path
    else:
        # If folders are different
        pass

    # When all user inputs are completed
    print()
    print("-" * 30)
    print()

    # After all input, begin folder creation and processing
    if not same_folder:
        # Create the output folder if it does not exist
        os.makedirs(output_folder_path, exist_ok=True)
        save_folder = output_folder_path

    else:
        if use_subfolder == "y":
            os.makedirs(save_folder, exist_ok=True)

    original_total_size = calculate_total_size(input_folder_path)

    # Process images
    for file in os.listdir(input_folder_path):
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            input_file_path = os.path.join(input_folder_path, file)

            img = Image.open(input_file_path)

            # Decide output filename
            if same_folder:
                if use_subfolder == "y":
                    output_file_name = file
                    output_file_path = os.path.join(save_folder, output_file_name)
                else:
                    if delete_originals == "y":
                        output_file_name = file
                        output_file_path = os.path.join(save_folder, output_file_name)
                        
                        os.remove(input_file_path)

                        img.save(output_file_path, optimize = True, quality = optimization_quality)
                        continue
                    else:
                        file_name, extension = os.path.splitext(file)
                        output_file_name = f"{file_name}_optimized{extension}"
                        output_file_path = os.path.join(save_folder, output_file_name)
            else:
                output_file_path = os.path.join(save_folder, file)
            img.save(output_file_path, optimize=True, quality = optimization_quality)

    optimized_total_size = calculate_total_size(save_folder)

    print("Successfully optimized images!")
    print(f"{original_total_size} bytes --> {optimized_total_size} bytes")