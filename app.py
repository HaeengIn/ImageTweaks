import process, os, sys, webbrowser, importlib, json

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Run the single process
def run_single_process():
    print("[ Single Process ]")
    print("Select process from the menu below.")
    print("[ Optimize, Convert ]")
    while True:
        input_process = input("> ").strip().lower()
        if input_process in ["optimize", "convert"]:
            break
        else:
            print("Invalid Input.")
    
    clear_console()

    if input_process:
        clear_console()
        while True:
            module_path = f"process.single_process.{input_process}"
            module = importlib.import_module(module_path)

            function_name = f"run_{input_process}"
            function = getattr(module, function_name)

            function()

            while True:
                print(f"\nDo you want to {input_process} another image? (Y/N)")
                another_process = input("> ").strip().lower()
                if another_process in ["y", "n"]:
                    break
                else:
                    print("Invalid Input. Please enter Y or N.")

            if another_process == "y":
                clear_console()
                continue
            elif another_process == "n":
                clear_console()
                break

        main()

# Run the multiple process
def run_multiple_process():
    print("[ Multiple Process ]")
    print("Select process from the menu below.")
    print("[ Optimize ]")
    while True:
        input_process = input("> ").strip().lower()
        if input_process in ["optimize"]:
            break
        else:
            print("Invalid Input.")
    if input_process == "optimize":
        clear_console()
        while True:
            process.multiple.optimize.run_optimization()
            while True:
                print("\nDo you want to optimize another folder? (Y/N)")
                another_optimization = input("> ").strip().lower()
                if another_optimization in ["y", "n"]:
                    break
                else:
                    print("Invalid Input. Please enter Y or N.")
            if another_optimization == "y":
                clear_console()
                continue
            elif another_optimization == "n":
                clear_console()
                break
        main()

# Open Wiki page
def open_wiki():
    webbrowser.open("https://messy-yak-716.notion.site/Image-Tweaks-Official-Wiki-2b96afdf1918807f8063f42a75ba5cbd")
    main()

# Open Info page
def open_info():
    with open("version.json", "r", encoding="utf-8") as version_file:
        version_data = json.load(version_file)

    version = version_data.get("version")
    revision = version_data.get("revision")
    last_update = version_data.get("last_update")

    print("[ Image Tweaks ]\n\n" \
    "Currently supported process:\n" \
    "[ Optimize ]\n\n" \
    "Supported formats:\n" \
    "[ JPG, JPEG, PNG, WEBP, AVIF ]\n\n" \
    f"Version: {version}\n" \
    f"Revision: {revision}\n" \
    f"Last Update: {last_update}")
    input("\nPress Enter to return to the main menu... ")
    clear_console()
    main()

# Exit the app
def exit_app():
    while True:
        print("Do you really want to exit the app? (Y/N)")
        confirm = input("> ").strip().lower()
        if confirm in ["y", "n"]:
            break
        else:
            print("Invalid Input. Please enter Y or N.")
    
    if confirm == "y":
        clear_console()
        sys.exit()
    elif confirm == "n":
        clear_console()
        main()

# Run the app
def main():
    clear_console()
    print("[ Image Tweaks ]")
    print("Type and enter the menu option what you want to do.")
    print("[ Single / Multiple / Wiki / Info / Exit ]")
    while True:
        process_type = input("> ").strip().lower()
        if process_type in ["single", "multiple", "wiki", "info", "exit"]:
            if process_type == "single":
                clear_console()
                run_single_process()
            elif process_type == "multiple":
                clear_console()
                run_multiple_process()
            elif process_type == "wiki":
                clear_console()
                open_wiki()
            elif process_type == "info":
                clear_console()
                open_info()
            elif process_type == "exit":
                clear_console()
                exit_app()
            break
        else:
            print("Invalid Input.")

if __name__ == "__main__":
    main()