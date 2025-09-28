import locale
import os
import random
import json
import re

variable_pattern = r'(?P<var>\$(?P<arg>\w+|\+|\$))+'
guh_keys, guh_values = [], []
guh = {}
coins = 0
number = 0
lang_file = []
variables = {
    "number": 0,
    "coins": 0,
    "upgrade1_cost": 10,
    "upgrade2_cost": 10,
    "upgrade3_cost": 15,
    "upgrade4_cost": 20,
    "upgrade5_cost": 25,
    "upgrade_cost": 0,
    "guh": guh
}


def initialize():
    global lang_file
    current_locale = locale.getdefaultlocale()[0]
    if not os.path.exists('locales'):
        os.mkdir('locales')
    if not os.path.exists(os.path.join('locales', f'{current_locale}.json')):
        print(f"Locale {current_locale} not found, falling back to en_US")
        current_locale = 'en_US'

    with open(os.path.join('locales', f'{current_locale}.json'),
              encoding='utf-8') as file:
        lang_file = json.load(file)
    guh = {
        -5: 15,
        -4: 14,
        -3: 13,
        -2: 12,
        -1: 11,
        1: 10,
        2: 9,
        3: 8,
        4: 7,
        5: 6,
        6: 5,
        7: 4,
        8: 3,
        9: 2,
        10: 1,
        "upgrade1": 15,
        "upgrade2": 15,
        "upgrade3": 10,
        "upgrade4": 5,
        "upgrade5": 1
    }

    variables["guh"] = guh

    for key in guh.keys():
        guh_keys.append(key)
        guh_values.append(guh[key])


def run():
    global number
    global coins
    number = random.choices(guh_keys, weights=guh_values)[0]
    if isinstance(number, str):
        print(format_str(lang_file["buy_upgrade"]+lang_file[number]+"."))
        buy_upgrade = input("Y/N: ") # this would probably be a button when ported over to c#
        if buy_upgrade.upper() == "Y":
            match number:
                case "upgrade1":
                    variables["upgrade_cost"] = variables["upgrade1_cost"]
                case "upgrade2":
                    variables["upgrade_cost"] = variables["upgrade2_cost"]
                case "upgrade3":
                    variables["upgrade_cost"] = variables["upgrade3_cost"]
                case "upgrade4":
                    variables["upgrade_cost"] = variables["upgrade4_cost"]
                case "upgrade5":
                    variables["upgrade_cost"] = variables["upgrade5_cost"]
            if coins < variables["upgrade_cost"]:
                print(format_str(lang_file["insufficent_funds"]))
                number = 0
            else:
                print(format_str(lang_file["upgrade_bought"]))
                match number:
                    case "upgrade1":
                        print(format_str(lang_file["select_keys"] + lang_file["probability_upgrades"]))
                    case "upgrade2":
                        variables["upgrade_cost"] = variables["upgrade2_cost"]
                    case "upgrade3":
                        variables["upgrade_cost"] = variables["upgrade3_cost"]
                    case "upgrade4":
                        variables["upgrade_cost"] = variables["upgrade4_cost"]
                    case "upgrade5":
                        variables["upgrade_cost"] = variables["upgrade5_cost"]
                # I wasn't sure what to do other than duplicated the code so it isn't the most efficent
                number = variables["upgrade_cost"]
        else:
            print(format_str(lang_file["upgrade_not_bought"]))
            number = 0

    coins += number
    variables["number"] = number
    variables["coins"] = coins


def compile_variable(arg: re.Match[str]) -> str:
    sb = ""
    variable_argument = arg.group('arg')
    match variable_argument:
        case '$': sb += '$ '
        case '+': sb += '\010'
        case _: sb += f"{str(variables[variable_argument])} "
    return sb


def format_str(string) -> str:
    s = ""
    for i in string.split(' '):
        r = re.compile(variable_pattern)
        m = r.match(i)
        if not m:
            s += f"{i} "
            continue
        v = compile_variable(m)
        s += f"{r.sub('arg', v)}"
    return s.rstrip(' ')


def print_current():
    formatted_string = format_str(lang_file["show_coins"])
    print(formatted_string)


initialize()
for i in range(100):
    run()
    print_current()
