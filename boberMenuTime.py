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

    return menu_dict

def get_toppings():
    toppings_text = open("toppings.txt", "r")
    toppings_list = [i[:-1] for i in toppings_text.readlines()]
    toppings_text.close()

    toppings_dict = {}

    for line in toppings_list:
        toppings_line = line.split("/",2)
        toppings_dict[toppings_line[0].lower()] = float(toppings_line[1])

    return toppings_dict