import os
import subprocess

def check_dir():
    if os.path.exists("notes"):
        if os.path.isdir("notes"):
            return 1
    
    return -1

def show_options(options):
    for idx, value in enumerate(options):
        print(f"{idx+1}. {value}")
    print(f"{len(options)+1}. Exit")

def validate(options):
    while True:
        try:
            option = int(input("Choose an option: "))
        except ValueError:
            print("The value must be a number | Try again")
        else:
            if option < 1 or option > len(options)+1:
                print(f"The option must be between 1-{len(options)+1} | Try again")
            elif option == len(options)+1:
                return -1
            else:
                return option

def add_note():
    while True:
        categories = [d for d in os.listdir() if os.path.isdir(d)]
        #if len(categories) == 0:
        #    add_categorie()
        show_options(categories)
        result = validate(categories)
        if result == -1:
            return
        notes = [n for n in os.listdir(categories[result-1]) if os.path.isfile(os.path.join(categories[result-1], n))]
        note_name = input("Write the name of the new note('*' to go back to the main menu): ")
        if note_name.strip() =="*":
            return
        elif note_name.strip() == "":
            print("You have to write something, the programm will not search a blank space | Try again")
        elif (note_name.lower() + ".txt") in notes:
            print("There is one with the same name | Try again")
        else:
            try:
                file_name = note_name.lower() + ".txt"
                path = os.path.join(categories[result-1], file_name)
                arch = open(f"{path}", "wt", encoding="UTF-8")
            except OSError as o:
                print(f"Error os: {o}")
            except Exception as e:
                print(f"Error e: {e}")
            else:
                arch.close()
                print(f"Note added")

def delete_note():
    while True:
        categories = [d for d in os.listdir() if os.path.isdir(d)]
        show_options(categories)
        result = validate(categories)
        if result == -1:
            return
        files = [n for n in os.listdir(categories[result-1]) if os.path.isfile(os.path.join(categories[result-1], n))]        
        show_options(files)
        match = validate(files)
        if match == -1:
            return
        confirmation = input(f"Are you sure?\nYES - NO: ")
        if confirmation.strip().upper() == "YES":
            path = os.path.join(categories[result-1], files[match-1])
            os.remove(path)
            print(f"The note has been removed")
 
def search_note(): 
    while True:
        categories = [d for d in os.listdir() if os.path.isdir(d)]
        show_options(categories)
        result = validate(categories)
        if result == -1:
            return
        files = [n for n in os.listdir(categories[result-1]) if os.path.isfile(os.path.join(categories[result-1], n))]
        option = input("Write the note you are looking for('*' to go back to the main menu): ")
        if option.strip() == "":
            print("You have to write something, the programm will not search a blank space | Try again")
        elif option.strip() =="*":
            return -1
        else:
            matches = []
            for f in files:
                if option.lower() in f.lower():
                    matches.append(f)
            if len(matches) == 0:
                print("The programm did not find anything | Try again")
            else:
                while True:
                    show_options(matches)
                    match = validate(matches)
                    if  match == -1:
                        break
                    path = os.path.join(categories[result-1], matches[match-1])
                    if os.name=="nt":
                        subprocess.Popen(["start", path])
                    else:
                        subprocess.Popen(["xdg-open", path])
                    print(f"{path} was opened")

def show_menu(menu, lista_opt, lista_funciones):
    while True:
        print(f"{'Welcome to the ' + menu:-^60}")
        show_options(lista_opt)
        result = validate(lista_opt)
        if result == -1:
            return
        lista_funciones[result-1]()

#M.P
if check_dir() == -1:
    os.mkdir("notes")
os.chdir("notes")
main_opt = ["Search Notes", "Add a note", "Delete a note", "Add a categorie", "Move a note"]
#main_functions = [search_note, add_note, delete_note, add_categorie, move_note]
main_functions = [search_note, add_note, delete_note]
show_menu("main menu", main_opt, main_functions)