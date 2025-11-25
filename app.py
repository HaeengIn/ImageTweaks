import process, os


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


# Run the single process
def run_single_process():
    print("[ Single Process ]")
    print("Select process from the menu below.")
    print("[ Compress ]")
    while True:
        input_process = input("\n> ").strip().lower()
        if input_process == "compress":
            clear_console()
            while True:
                process.single.optimize.run_optimization()
                while True:
                    print("\nDo you want to optimize another image? (Y/N)")
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
            break
        else:
            print("Invalid Input.")


# Run the multiple process
def run_multiple_process():
    pass


# Open Wiki page
def open_wiki():
    pass


# Open Tips page
def open_tips():
    pass


# Open Info page
def open_info():
    pass


# Exit the app
def exit_app():
    pass


# Run the app
def main():
    clear_console()
    print("[ Image Tweaks ]")
    print("Type and enter the menu option what you want to do.")
    print("[ Single / Multiple / Wiki / Tips / Info / Exit ]")
    while True:
        process_type = input("> ").strip().lower()
        if process_type in ["single", "multiple", "wiki", "tips", "info", "exit"]:
            if process_type == "single":
                clear_console()
                run_single_process()
            else:
                clear_console()
                run_multiple_process()
            break
        else:
            print("Invalid Input. Please enter 'Single' or 'Multiple'")


if __name__ == "__main__":
    main()
