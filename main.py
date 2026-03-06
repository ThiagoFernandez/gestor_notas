import os
import subprocess
import shutil
import json

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
        state = 0
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
            if state == 1:
                tag_list = recover_tags(path)
                if tag in tag_list:
                    print("The note alreeady has this tag | Try again")
                else:
                    remove_tag.lower()
            else:
                return tag.lower()

def recover_tags(key):
    try:
        arch = open("../data.json", "rt", encoding="UTF-8")
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

def add_note():
    while True:
        greeting_text("Adding note...")
        categories = [d for d in os.listdir() if os.path.isdir(d)]
        if len(categories) == 0:
            rt=add_categorie()
            if rt == -1:
                return
            else:
                categories = [d for d in os.listdir() if os.path.isdir(d)]
        show_options(categories)
        result = validate_number(categories)
        if result == -1:
            return
        notes = [n for n in os.listdir(categories[result-1]) if os.path.isfile(os.path.join(categories[result-1], n))]
        rst = validate_string(notes, "Write the name of the note", 0)
        if rst == -1:
            return -1
        else:
            try:
                path = os.path.join(categories[result-1], rst)
                arch = open(f"{path}", "wt", encoding="UTF-8")
                tag_confirm = input(f"Do you want to add a tag?\nYES - NO: ")
                if tag_confirm.strip().upper() == "YES":
                    add_tag(1, path)
            except OSError as o:
                print(f"Error os: {o}")
            except Exception as e:
                print(f"Error e: {e}")
            else:
                arch.close()
                print(f"Note added")
                open_file(path)

def delete_note():
    while True:
        greeting_text("Deleting note...")
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1
        show_options(cat_rt)
        result = validate_number(cat_rt)
        if result == -1:
            return
        files = [n for n in os.listdir(cat_rt[result-1]) if os.path.isfile(os.path.join(cat_rt[result-1], n))]        
        show_options(files)
        match = validate_number(files)
        if match == -1:
            return
        confirmation = input(f"Are you sure?\nYES - NO: ")
        if confirmation.strip().upper() == "YES":
            path = os.path.join(cat_rt[result-1], files[match-1])
            os.remove(path)
            print(f"The note has been removed")
 
def search_note(): 
    while True:
        greeting_text("Searching note...")
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1
        show_options(cat_rt)
        result = validate_number(cat_rt)
        if result == -1:
            return
        files = [n for n in os.listdir(cat_rt[result-1]) if os.path.isfile(os.path.join(cat_rt[result-1], n))]
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
                    match = validate_number(matches)
                    if  match == -1:
                        break
                    path = os.path.join(cat_rt[result-1], matches[match-1])
                    open_file(path)
                    print(f"{path} was opened")

def add_category():
    while True:
        greeting_text("Adding category...")
        categories = [d for d in os.listdir() if os.path.isdir(d)]
        rst = validate_string(categories, "Write the new category", 1)
        if rst == -1:
            return -1
        else:
            os.mkdir(rst)
            print("A new category has been created")

def remove_category():
    while True:
        greeting_text("Removing category...")
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1
        else:
            show_options(cat_rt)
            result=validate_number(cat_rt)
            if result == -1:
                return -1
            else:
                confirmation = input(f"You are going to delete all the notes inside this category - Are you sure?\nYES - NO: ")
                if confirmation.strip().upper() == "YES":
                    shutil.rmtree(cat_rt[result-1])

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

def add_tag(state, path):
    if state == 0: # normal
        while True:
            greeting_text("Adding a tag...")
            cat_rt = validate_category()
            if cat_rt == -1:
                return -1
            else:
                show_options(cat_rt)
                rt = validate_number(cat_rt)
                if rt == -1:
                    return -1
                else:
                    notes = [f for f in os.listdir(cat_rt[rt-1])]
                    show_options(notes)
                    n_rt = validate_number(notes)
                    if n_rt == -1:
                        return -1
                    else:
                        path = os.path.join((cat_rt[rt-1]), notes[n_rt-1])
                        t_rt = validate_tag(1, path)
                        if t_rt == -1:
                            return -1
                        else:
                            try:
                                arch = open("../data.json", "rt", encoding="UTF-8")
                                dic = json.load(arch)
                                arch.close()
                                arch = open("../data.json", "wt", encoding="UTF-8")
                            except json.JSONDecodeError:
                                print("Error json")
                            except OSError as o:
                                print(f" Error os: {o}")
                            except Exception as e:
                                print(f"Error e: {e}")
                            else:
                                if path not in dic:
                                    dic[path] = [t_rt]
                                else:
                                    dic[path].append(t_rt)
                                json.dump(dic, arch, indent=4)
                                arch.close()
    else: # cuando es una clave nueva
        t_rt = validate_tag(0, path)
        if t_rt == -1:
            return -1
        else:
            try:
                arch = open("../data.json", "rt", encoding="UTF-8")
                dic = json.load(arch)
                arch.close()
                arch = open("../data.json", "wt", encoding="UTF-8")
            except json.JSONDecodeError:
                print("Error json")
            except OSError as o:
                print(f" Error os: {o}")
            except Exception as e:
                print(f"Error e: {e}")
            else:
                dic[path] = [t_rt]    
                json.dump(dic, arch, indent=4)
                arch.close()  

def remove_tag():
    while True:
        greeting_text("Deleting a tag...")      
        cat_rt = validate_category()
        if cat_rt == -1:
            return -1
        else:
            show_options(cat_rt)
            rt = validate_number(cat_rt)
            if rt == -1:
                return -1
            else:
                notes = [f for f in os.listdir(cat_rt[rt-1])]
                show_options(notes)
                n_rt = validate_number(notes)
                if n_rt == -1:
                    return -1
                else:
                    key = os.path.join(cat_rt[rt-1], notes[n_rt-1])
                    tag_list = recover_tags(key)
                    if tag_list == -1:
                        return -1
                    else:
                        show_options(tag_list)
                        tl_rt = validate_number(tag_list)
                        if tl_rt == -1:
                            return -1
                        else:
                            try:
                                arch = open("../data.json", "rt", encoding="UTF-8")
                                dic = json.load(arch)
                                arch.close()
                                arch = open("../data.json", "wt", encoding="UTF-8")
                            except json.JSONDecodeError:
                                print("Error json")
                            except OSError as o:
                                print(f" Error os: {o}")
                            except Exception as e:
                                print(f"Error e: {e}")
                            else:
                                dic[key].remove(tag_list[tl_rt-1])
                                json.dump(dic, arch, indent=4)
                                arch.close()

def search_tag():
    try:
        arch = open("../data.json", "rt", encoding="UTF-8")
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
                    lista_opt_n = ["Search Notes", "Add a note", "Delete a note", "Move a note", "Rename a note"]
                    lista_fun_n = [search_note, add_note, delete_note, move_note, rename_note]
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