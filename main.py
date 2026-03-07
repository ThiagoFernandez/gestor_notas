import os
import subprocess
import shutil
import json
DATA_FILE = "../data.json"
# auxiliar functions

def check_dir():
    if os.path.exists("notes"):
        if os.path.isdir("notes"):
            return 1
    
    return -1

def check_json():
    if os.path.exists("data.json"):
        return 1
    else:
        return -1

def open_file(path):
    if os.name == "nt":
        os.startfile(path)
    else: 
        if path.endswith(".pdf"):
            subprocess.Popen(["xdg-open", path])
        else:
            subprocess.Popen(["kwrite", path])

def show_options(options):
    for idx, value in enumerate(options):
        print(f"{idx+1}. {value}")
    print(f"{len(options)+1}. Exit")

def validate_number(options):
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

def validate_string(options, text, type):
    while True:
        string = input(f"{text}('*' to go back to the menu): ")
        if string.strip() == "":
            print("Only blank space as text is invalid | Try again")
        elif string.strip() == "*":
            return -1
        elif string in options:
            print("There is one with the same name | Try again")
        elif not string.endswith(".txt") and type == 0: 
            print(f"The name needs to end with a '.txt' | Try again")
        else:
            return string

def validate_category():
    categories = [d for d in os.listdir() if os.path.isdir(d)]

    if len(categories) == 0:
        print("There are no categories therefore there are no notes | Back to the main menu")
        return -1
    return categories

def validate_tag(state, path):
    while True:
        tag = input("Write the tag name('*' to go back): ")
        if tag == "*":
            return -1
        elif tag.strip() =="":
            print("Only blank space as text is invalid | Try again")
        else:
            if state == 0:
                tag_list = recover_tags(path)
                if tag_list == -1:
                    return -1
                if tag in tag_list:
                    print("The note alreeady has this tag | Try again")
                else:
                    return tag.lower()
            else:
                return tag.lower()

def recover_tags(key):
    try:
        arch = open(DATA_FILE, "rt", encoding="UTF-8")
        dic = json.load(arch)
    except json.JSONDecodeError:
        print("Error json")
        return -1
    except OSError as o:
        print(f" Error os: {o}")
        return -1
    except Exception as e:
        print(f"Error e: {e}")
        return -1
    else:
        tag_list = []
        if key in dic:
            for t in dic[key]:
                if t not in tag_list:
                    tag_list.append(t)
            arch.close()
            return tag_list
        else:
            arch.close()
            print(f"This note has no tags")
            return -1

def delete_key(path):

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.pop(path, None)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def preview_note(path, note):
    try:
        arch = open(path, "rt", encoding="UTF-8")
    except OSError as o:
        print(f"Error os: {o}")
    except Exception as e:
        print(f"Error e: {e}")
    else:
        preview = [arch.readline() for _ in range(5)]
        arch.close()
        print(f"{'':|^60}")
        print(f"Preview of {note}")
        for p in preview:
            print(p)
        print(f"{'':|^60}")
        confirmation = input(f"Is this the note that you are looking for?\nYES - NO: ")
        if confirmation.strip().upper() != "YES":
            return -1
        
        
# main functions

def add_note():
    while True:
        greeting_text("Adding note...")

        categories = [d for d in os.listdir() if os.path.isdir(d)]

        if len(categories) == 0:
            rt = add_category()
            if rt == -1:
                return
            continue

        show_options(categories)
        result = validate_number(categories)

        if result == -1:
            return

        while True:
            notes = [n for n in os.listdir(categories[result-1]) 
                     if os.path.isfile(os.path.join(categories[result-1], n))]

            rst = validate_string(notes, "Write the name of the note", 0)

            if rst == -1:
                break

            path = os.path.join(categories[result-1], rst)

            try:
                with open(path, "wt", encoding="UTF-8"):
                    pass

                tag_confirm = input("Do you want to add a tag?\nYES - NO: ")

                if tag_confirm.strip().upper() == "YES":
                    add_tag(1, path)

                print("Note added")
                open_file(path)

            except OSError as o:
                print(f"Error os: {o}")

def delete_note():
    greeting_text("Deleting note...")
    categories = [d for d in os.listdir() if os.path.isdir(d)]

    while True:
        show_options(categories)
        result = validate_number(categories)

        if result == -1:
            return -1

        notes = [n for n in os.listdir(categories[result-1])
                 if os.path.isfile(os.path.join(categories[result-1], n))]

        while True:
            show_options(notes)
            result2 = validate_number(notes)

            if result2 == -1:
                break

            path = os.path.join(categories[result-1], notes[result2-1])

            try:
                os.remove(path)
                delete_key(path)
                print("Note deleted")
            except OSError as o:
                print(f"Error: {o}")
 
def search_note():
    greeting_text("Searching note...")
    categories = [d for d in os.listdir() if os.path.isdir(d)]

    while True:
        show_options(categories)
        result = validate_number(categories)

        if result == -1:
            return -1

        category = categories[result-1]

        while True:
            files = [n for n in os.listdir(category)
                     if os.path.isfile(os.path.join(category, n))]

            text = input("Enter search term: ")

            if text == "*":
                break

            result_list = [f for f in files if text in f]

            if not result_list:
                print("No results")
                continue

            while True:
                show_options(result_list)
                rst = validate_number(result_list)

                if rst == -1:
                    break

                path = os.path.join(category, result_list[rst-1])
                open_file(path)

def search_content():
    while True:
        greeting_text("Searching by content...")

        word = input("Write the word you want to search('*' to go back): ")

        if word.strip() == "":
            print("You must write something | Try again")
            continue
        elif word.strip() == "*":
            return -1

        word = word.lower()
        matches = []

        categories = [d for d in os.listdir() if os.path.isdir(d)]

        for cat in categories:
            files = [f for f in os.listdir(cat) if os.path.isfile(os.path.join(cat, f))]

            for file in files:
                path = os.path.join(cat, file)

                try:
                    with open(path, "rt", encoding="UTF-8") as arch:
                        for line in arch:
                            if word in line.lower():
                                matches.append(path)
                                break
                except OSError as o:
                    print(f"Error os: {o}")

        if len(matches) == 0:
            print("No matches found | Try again")
            continue

        while True:
            show_options(matches)
            match = validate_number(matches)

            if match == -1:
                return -1

            path = matches[match-1]
            note = os.path.basename(path)

            p_rt = preview_note(path, note)

            if p_rt == -1:
                break

            open_file(path)
            print(f"{path} was opened")

def add_category():
    greeting_text("Adding category...")

    while True:
        name = input("Write category name: ")

        if name == "*":
            return -1

        if os.path.exists(name):
            print("Category already exists")
            continue

        try:
            os.mkdir(name)
            print("A new category has been created")
            return
        except OSError as o:
            print(f"Error: {o}")

def remove_category():
    greeting_text("Deleting category...")

    cat_rt = [d for d in os.listdir() if os.path.isdir(d)]

    while True:
        show_options(cat_rt)
        result = validate_number(cat_rt)

        if result == -1:
            return -1

        category = cat_rt[result-1]

        notes = [f for f in os.listdir(category)]

        for n in notes:
            path = os.path.join(category, n)
            delete_key(path)

        try:
            shutil.rmtree(category)
            print("Category deleted")
        except OSError as o:
            print(f"Error: {o}")

        cat_rt = [d for d in os.listdir() if os.path.isdir(d)]

def rename_category():
    while True:
        greeting_text("Renaming category...")
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1
        else:
            show_options(cat_rt)
            result = validate_number(cat_rt)
            if result == -1:
                return -1
            else:
                rst = validate_string(cat_rt, "Write the new name for the category", 1)
                if rst == -1:
                    return -1
                else:
                    os.rename(cat_rt[result-1], rst)
                    print("The category has been renamed")

def rename_note():
    while True:
        greeting_text("Renaming note...")
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1

        show_options(cat_rt)
        result = validate_number(cat_rt)

        if result == -1:
            return -1

        notes = [f for f in os.listdir(cat_rt[result-1]) if os.path.isfile(os.path.join(cat_rt[result-1], f))]

        if len(notes) == 0:
            print("There are no notes in this category")
            return

        show_options(notes)
        rt = validate_number(notes)

        if rt == -1:
            return -1

        rst = validate_string(notes, "Write the new name for the note", 0)

        if rst == -1:
            return -1

        old_path = os.path.join(cat_rt[result-1], notes[rt-1])
        new_path = os.path.join(cat_rt[result-1], rst)

        os.rename(old_path, new_path)

        print("The note has been renamed")

def move_note():
    while True:
        greeting_text("Moving note...")
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1

        show_options(cat_rt)
        result = validate_number(cat_rt)

        if result == -1:
            return -1

        notes = [f for f in os.listdir(cat_rt[result-1]) if os.path.isfile(os.path.join(cat_rt[result-1], f))]

        if len(notes) == 0:
            print("There are no notes in this category")
            return

        show_options(notes)
        rt = validate_number(notes)

        if rt == -1:
            return -1

        old_path = os.path.join(cat_rt[result-1], notes[rt-1])

        greeting_text("Choose destination category")
        show_options(cat_rt)

        while True:
            nrt = validate_number(cat_rt)

            if nrt == -1:
                return -1

            if nrt == result:
                print("The note is already in this category | Try again")
            else:
                new_path = os.path.join(cat_rt[nrt-1], notes[rt-1])
                shutil.move(old_path, new_path)

                print("The note has been moved")
                return

def add_tag(mode, path=None):
    greeting_text("Adding tag...")

    while True:

        if mode == 0:
            categories = [d for d in os.listdir() if os.path.isdir(d)]
            show_options(categories)
            result = validate_number(categories)

            if result == -1:
                return -1

            notes = [n for n in os.listdir(categories[result-1])
                     if os.path.isfile(os.path.join(categories[result-1], n))]

            show_options(notes)
            result2 = validate_number(notes)

            if result2 == -1:
                continue

            path = os.path.join(categories[result-1], notes[result2-1])

        tag = validate_tag(mode, path)

        if tag == -1:
            return -1

        data = {}

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.setdefault(path, []).append(tag)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Tag added")
        return

def remove_tag():
    greeting_text("Removing tag...")

    while True:
        categories = [d for d in os.listdir() if os.path.isdir(d)]

        show_options(categories)
        result = validate_number(categories)

        if result == -1:
            return -1

        notes = [n for n in os.listdir(categories[result-1])
                 if os.path.isfile(os.path.join(categories[result-1], n))]

        show_options(notes)
        result2 = validate_number(notes)

        if result2 == -1:
            continue

        path = os.path.join(categories[result-1], notes[result2-1])

        tags = recover_tags(path)

        if tags == -1 or not tags:
            print("No tags")
            continue

        show_options(tags)
        rst = validate_number(tags)

        if rst == -1:
            continue

        data = {}

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        data[path].remove(tags[rst-1])

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Tag removed")

def search_tag():
    try:
        arch = open(DATA_FILE, "rt", encoding="UTF-8")
        dic = json.load(arch)
    except json.JSONDecodeError:
        print("Error json")
        return -1
    except OSError as o:
        print(f" Error os: {o}")
        return -1
    except Exception as e:
        print(f"Error e: {e}")
        return -1
    else:
        arch.close()
        tag_list = []
        for value in dic.values():
            for t in value:
                if t not in tag_list:
                    tag_list.append(t)
        if len(tag_list) == 0:
            arch.close()
            print("There are no tags to search | Try adding one first")
            return -1
        else:
            show_options(tag_list)
            t_rt = validate_number(tag_list)
            if t_rt == -1:
                return -1
            else:
                notes_with_tag = []
                for clave, value in dic.items():
                    if tag_list[t_rt-1] in value:
                        notes_with_tag.append(clave)
                show_options(notes_with_tag)
                nt_rt = validate_number(notes_with_tag)
                if nt_rt == -1:
                    return -1
                else:
                    idx = notes_with_tag[nt_rt-1].index("/")
                    note = notes_with_tag[nt_rt-1][idx+1:]
                    p_rt = preview_note(notes_with_tag[nt_rt-1], note)
                    if p_rt == -1:
                        return -1
                    open_file(notes_with_tag[nt_rt-1])

def show_menu(menu, lista_opt, lista_funciones):
    while True:
        print(f"{' Welcome to the ' + menu+" ":-^60}")
        show_options(lista_opt)
        result = validate_number(lista_opt)
        if result == -1:
            return
        lista_funciones[result-1]()

def show_main_menu():
    while True:
        print(f"{' Welcome to the main menu ':-^60}")
        show_options(["Notes Menu", "Categories Menu", "Tags Menu"])
        result = validate_number(["Notes Menu", "Categories Menu", "Tags Menu"])
        if result == -1:
            return
        else:
            match result:
                case 1:
                    lista_opt_n = ["Search Notes", "Search By Content", "Add a note", "Delete a note", "Move a note", "Rename a note"]
                    lista_fun_n = [search_note, search_content, add_note, delete_note, move_note, rename_note]
                    menu_f = "notes menu"
                    show_menu(menu_f, lista_opt_n, lista_fun_n)
                case 2:
                    lista_opt_c = ["Add a category", "Remove a category", "Rename a category"]
                    lista_fun_c = [add_category, remove_category, rename_category]
                    menu_c = "categories menu"
                    show_menu(menu_c, lista_opt_c, lista_fun_c)
                case 3:
                    lista_opt_t = ["Add a tag", "Remove a tag", "Search by tag"]
                    lista_fun_t = [add_tag, remove_tag, search_tag]
                    menu_t = "tags menu"
                    show_menu(menu_t, lista_opt_t, lista_fun_t)

def greeting_text(text):
    print(f"{' ' + text + ' ':-^60}")

#M.P
if check_json() == -1:
    dic = {}
    arch = open("data.json", "wt", encoding="UTF-8")
    json.dump(dic, arch, indent=4)
    arch.close()

if check_dir() == -1:
    os.mkdir("notes")
os.chdir("notes")

show_main_menu()