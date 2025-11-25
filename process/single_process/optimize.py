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

        # If user entered nothing or Root Folder
        if output_image_path in ["/", ""]:
            print("Cannot save optimized image at Root Folder. Please enter other folder.")
        # If the folder that user entered doesn't exist: create new folder, set the path of output image, and return
        else:
            return output_image_path


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

            # Export extension and convert to lowercase
            output_extension = os.path.splitext(output_image_path)[1].lower()

            # Reset params that will be used when saving
            save_params = {"optimize": True}

            # Process optimization by format
            if output_extension in (".jpg", ".jpeg"):
                # JPEG: Use 'quality' params (0-100)
                # Convert RGBA to RGB when saving as JPEG
                image_to_save = img
                if img.mode in ("RGBA", "P"):
                    image_to_save = img.convert("RGB")

                save_params["quality"] = optimization_quality

            elif output_extension == ".png":
                # PNG: Use 'optimize_level' params (0-9)
                # Convert quality (0~100) to optimize_level (0~9)
                optimize_level = int(optimization_quality / 100 * 9)  # Convert to 0~9
                save_params["optimize_level"] = optimize_level
                image_to_save = (
                    img  # PNG: Doesn't need to convert as it supports transparency
                )

            else:
                # Other formats (ex: GIF, BMP, Tiff, etc): ignore 'quality' and apply basic optimization
                print(
                    f"\nNote: '{output_extension}' format does not effectively support 'quality' setting. Applying basic optimization."
                )
                image_to_save = img

            # Save image
            image_to_save.save(output_image_path, **save_params)

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
            final_output_folder = os.path.join(input_folder, new_folder_name)
            os.makedirs(final_output_folder, exist_ok=True)
            base_name = os.path.basename(output_image_path)
            output_image_path = os.path.join(final_output_path, base_name)
            print(f"\nImage will be saved at '{output_image_path}'.")
            print()
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
                print(f"Optimized image will be saved as: {optimized_name}")
                optimize_and_save(
                    input_image_path, output_image_path, optimization_quality
                )
                return
        # If new folder was created: optimize and save normally
        optimize_and_save(input_image_path, output_image_path, optimization_quality)

    # If output image path is different from input image path: optimized and save
    else:
        os.makedirs(output_image_path, exists_ok=True)
        base_name = os.path.basename(input_image_path)
        name, extension = os.path.splitext(base_name)
        output_file_name = f"{name}{extension}"
        output_image_path = os.path.join(output_image_path, output_file_name)
        optimize_and_save(input_image_path, output_image_path, optimization_quality)
