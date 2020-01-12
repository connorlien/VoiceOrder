def get_menu():
    menu_text = open("menu.txt", "r")
    menu_list = [i[:-1] for i in menu_text.readlines()]
    menu_text.close()

    menu_dict = {}

    for line in menu_list:
        menu_line = line.split("/",4)
        menu_dict[menu_line[0].lower()] = {
            "regular": float(menu_line[1]),
            "large": float(menu_line[2]),
            "hot": float(menu_line[3])
        }
        print(menu_line)

    return menu_dict

def get_toppings():
    return {
        "boba": 0.25,
        "lychee jelly": 0.50,
        "aloe vera": 0.50,
        "pudding": 0.50,
    }