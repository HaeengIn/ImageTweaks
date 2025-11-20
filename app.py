from process import *

# Run the single process
def run_single_process():
    pass

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
    print("\n[ Image Tweaks ]")
    print("Type and enter the menu option what you want to do.")
    print("[ Single / Multiple / Wiki / Tips / Info / Exit]")
    while True:
        process_type = input("> ").strip().lower()
        if process_type in ["single", "multiple", "wiki", "tips", "info", "exit"]:
            if process_type == "single":
                run_single_process()
            else:
                run_multiple_process()
            break
        else:
            print("Invalid Input. Please enter 'Single' or 'Multiple'")

if __name__ == "__main__":
    main()