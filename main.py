import json
import os

from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

from tools import general_tools
from tools.db_tools import start_db, delete_existent_data, load_ip_data_bulk, load_ip_data_individual, get_one_row, \
    get_all_row, dump_db
from tools.geo_tools import get_geo_bulk, get_geo_individual
from PyInquirer import prompt


def menu():
    '''
    Main method, displays a menu
    where the user can select the
    option he needs
    '''
    questions = [

        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Which option do you want to use?',
            'choices': ["Load file with IP Address", "Look for specific IP information",
                        "Look for all IP Address information stored on cache", "Export info as file .json",
                        "Dump cache", "Exit"]
        }

    ]

    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    print("Welcome to GEO locator online")
    stay_on_menu = True
    no_answer = True
    cursor, con = start_db()
    while stay_on_menu:
        print("*Menu*")

        no_answer = True
        while no_answer:

            try:
                answers = prompt(questions, style=style)
                opt = answers.get("user_option")

                no_answer = False
                if opt == "Load file with IP Address":
                    opt_file = input("Do you want to use a custom file or demo file? (custom/demo) ")
                    if opt_file.lower().__contains__("custom"):
                        url_file = input("Insert file url: ")
                        file_name = os.path.join(url_file)
                    elif opt_file.lower().__contains__("demo"):
                        current_dir = os.getcwd()
                        file_name = os.path.join(current_dir, "files", "list_of_ips.txt")
                    else:
                        print("Input error.")
                        break

                    bulk_flag = True
                    ip_text = general_tools.open_file(file_name)
                    list_ips = general_tools.to_text(ip_text)
                    list_ips = list(dict.fromkeys(list_ips))
                    while len(list_ips) != 0:
                        if bulk_flag:
                            list_ips = delete_existent_data(cursor, list_ips)
                            ips = "%2C".join(list_ips)
                            data, bulk_flag = get_geo_bulk(ips)
                            list_ips = load_ip_data_bulk(data.get("data", {}), cursor, list_ips)
                        else:
                            data = get_geo_individual(list_ips.pop(0))
                            load_ip_data_individual(data, cursor)
                        con.commit()

                elif opt == "Look for specific IP information":
                    ip_address = input("Insert ip address: ")
                    data = get_one_row(cursor, ip_address)
                    print(f"Information for IP Address {ip_address}")
                    for key, value in data.items():
                        print(f"{key.upper().replace('_', ' ')}: {value}")

                elif opt == "Look for all IP Address information stored on cache":
                    names, data = get_all_row(cursor)
                    for row in data:
                        temp_zip = dict(zip(names, row))
                        print(f"Information for IP Address {temp_zip.get('ip', '0.0.0.0')}")
                        for key, value in temp_zip.items():
                            if value != "" and value is not None:
                                print(f"{key.upper().replace('_', ' ')}: {value}")
                elif opt ==  "Export info as file .json":
                    print("Exporting...")
                    names, data = get_all_row(cursor)
                    full_data = []
                    with open('ip_lookup.txt', 'w') as outfile:
                        for row in data:
                            temp_zip = dict(zip(names, row))
                            ip_address = temp_zip.get('ip', '0.0.0.0')
                            new_json_item = {ip_address: []}
                            for key, value in temp_zip.items():
                                if value != "" and value is not None:
                                    new_json_item.get(ip_address).append({key.upper().replace('_', ' '): value})
                            full_data.append(new_json_item)
                        json.dump(full_data, outfile)
                        path = os.path.abspath("ip_lookup.txt")
                    print(f"Export ready. File location: {path}")
                elif opt == "Dump cache":
                    opt = input("Are you sure? All information is going to be deleted!! (Yes/No) ")
                    if opt.lower() == "yes":
                        dump_db(con)
                    else:
                        print("Not deleting")
                elif opt == "Exit":
                    con.close()
                    stay_on_menu = False
                    no_answer = False
                    print("Thanks for using our application!")
                else:
                    print("Insert a valid option")
                    no_answer = True
            except Exception as e:
                print(str(e))
                print("Incorrect info")
                # no_answer = True
                pass


if __name__ == "__main__":
    menu()
