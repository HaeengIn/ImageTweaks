from PIL import Image
import os


# Get the path of original imaghe file from user
def get_input_image_path():
    while True:
        print("\nEnter the path of original image file")
        input_image_path = input("> ").strip().strip('"')

        # Check if the file exists
        if os.path.isfile(input_image_path):
            return input_image_path
        else:
            print(f"Invalid Input. Caanot find the image: {input_image_path}")


# Get the path of output image file
def get_output_image_path(input_image_path):
    while True:
        print("\nEnter the path of output image file")
        output_image_path = input("> ").strip().strip('"')

        # Check if the folder exists
        # If the folder exists: set the name and path of the optimized image
        if os.path.isdir(output_image_path):
            base_name = os.path.basename(input_image_path)
            name, extension = os.path.splitext(base_name)
            output_file_name = f"{name}{extension}"
            output_image_path = os.path.join(output_image_path, output_file_name)
            return output_image_path
        else:
            print(f"Invalid folder path: {output_image_path}")


# Get integer value of optimization quality
def get_optimization_quality():
    while True:
        print("\nEnter the optimization quality (0~100)")
        optimization_quality = input("> ")

        # Try to convert the input to an integer
        try:
            # If the input is an integer: return the value
            optimization_quality = int(optimization_quality)
            if 0 <= optimization_quality <= 100:
                return optimization_quality
            else:
                print("Invalid Input. Please enter a integer value betwenn 0 and 100")
        except ValueError:
            print("Invalid Input. Please enter a integar value between 0 and 100")
            continue


# Optimize image and save
def optimize_and_save(input_image_path, output_image_path, optimization_quality):
    try:
        original_size = os.path.getsize(input_image_path)
        with Image.open(input_image_path) as img:
            # Convert RGBA to RGB when saving as JPEG
            image_to_save = img
            if output_image_path.lower().endswith((".jpg", ".jpeg")) and img.mode in (
                "RGBA",
                "P",
            ):
                image_to_save = img.convert("RGB")
            # Save image
            image_to_save.save(
                output_image_path, optimize=True, quality=optimization_quality
            )
            optimized_size = os.path.getsize(output_image_path)
            print("\nSuccessfully optimized!")
            print(f"{original_size} bytes -> {optimized_size} bytes")
            return True
    except Exception as e:
        print(f"Error occurred while optimizing image: {e}")
        return False


def run_optimization():
    input_image_path = (
        get_input_image_path()
    )  # Get the path of original imaghe file from user
    output_image_path = get_output_image_path(
        input_image_path
    )  # Get the path of folder of optimized image from user
    optimization_quality = (
        get_optimization_quality()
    )  # Get the integer value of optimization quality from user

    input_folder = os.path.dirname(
        os.path.abspath(input_image_path)
    )  # Get the path of folder of original image
    output_folder = os.path.dirname(
        os.path.abspath(output_image_path)
    )  # Get the path of folder of optimized image

    # If output image path is same as input image path
    if input_folder == output_folder:
        while True:
            print("\nDo you want to make a new folder? (Y/N)")
            make_new_folder = input("> ").strip().lower()
            if make_new_folder in ["y", "n"]:
                break
            else:
                print("Invalid Input. Please enter Y or N")

        # If new folder weill be created: ask if the original image will be deleted
        if make_new_folder == "y":
            new_folder_name = "Optimized Images"
            new_folder_path = os.path.join(input_folder, new_folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            base_name = os.path.basename(output_image_path)
            output_image_path = os.path.join(new_folder_path, base_name)
            print(f"\nImage will be saved at '{output_image_path}'.")
            print("-" * 30)

        # If new folder will be not created: ask if the original image will be deleted
        else:
            print(
                f"\nImage will be saved at {output_image_path}, overwriting original image."
            )
            while True:
                print("Delete original image? (Y/N)")
                delete_original_image = input("> ").strip().lower()
                if delete_original_image in ["y", "n"]:
                    break
                else:
                    print("Invalid Input. Please enter Y or N")

            # If original image will be deleted: optimize and save (optimized image will overwrite original image)
            if delete_original_image == "y":
                try:
                    print("Original image will be deleted.")
                    optimize_and_save(
                        input_image_path, output_image_path, optimization_quality
                    )
                except Exception as e:
                    print(f"Error occurred while deleting original image: {e}")
            else:
                base_name = os.path.basename(input_image_path)
                name, extension = os.path.splitext(base_name)
                optimized_name = f"{name}_optimized{extension}"
                output_image_path = os.path.join(input_folder, optimized_name)
                print(f"Compressed imaged will be saved as: {optimized_name}")
                optimize_and_save(
                    input_image_path, output_image_path, optimization_quality
                )
                return
        # If new folder was created: optimize and save normally
        optimize_and_save(input_image_path, output_image_path, optimization_quality)

    # If output image path is different from input image path: optimized and save
    else:
        optimize_and_save(input_image_path, output_image_path, optimization_quality)
