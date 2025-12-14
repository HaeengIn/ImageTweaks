import os, sys, webbrowser, importlib, json

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

with open("info.json", "r", encoding="utf-8") as info_file:
    info_data = json.load(info_file)
    version = info_data.get("version")
    revision = info_data.get("revision")
    last_update = info_data.get("last_update")
    supported_formats = info_data.get("supported_formats", [])
    supported_process = info_data.get("supported_process", [])

# Run the single process
def run_single_process():
    global supported_process
    print("[ Single Process ]")
    print("Select process from the menu below.")
    print(f"[ {', '.join(supported_process)} ]")
    while True:
        input_process = input("> ").strip().lower()
        if input_process in ["optimize", "convert"]:
            break
        else:
            print("\nInvalid Input.")
    clear_console()
    if input_process:
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
                    print("\nInvalid Input. Please enter Y or N.")
            if another_process == "y":
                clear_console()
                continue
            elif another_process == "n":
                clear_console()
                break
        main()

# Run the multiple process
def run_multiple_process():
    global supported_process
    print("[ Multiple Process ]")
    print("Select process from the menu below.")
    print(f"[ {', '.join(supported_process)} ]")
    while True:
        input_process = input("> ").strip().lower()
        if input_process in ["optimize", "convert"]:
            break
        else:
            print("\nInvalid Input.")
    clear_console()
    if input_process:
        while True:
            module_path = f"process.multiple_process.{input_process}"
            module = importlib.import_module(module_path)

            function_name = f"run_{input_process}"
            function = getattr(module, function_name)
            function()

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
    global version, revision, last_update, supported_formats, supported_process  
    print("[ Image Tweaks ]\n\n" \
    "Currently supported process:\n" \
    f"[ {", ".join(supported_process)} ]\n\n" \
    "Supported formats:\n" \
    f"[ {", ".join(supported_formats).upper()} ]\n\n" \
    f"Version: {version} (r{revision})\n" \
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
            print("\nInvalid Input. Please enter Y or N.")
    if confirm == "y":
        clear_console()
        sys.exit()
    else:
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
            print("\nInvalid Input.")
            continue

if __name__ == "__main__":
    main()