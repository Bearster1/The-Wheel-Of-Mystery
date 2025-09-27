import locale
import os
import random
import json
import re

variable_pattern = r'(?P<var>\$(?P<arg>\w+|\+|\$))+'
guh_keys, guh_values = [], []
coins = 0
number = 0
lang_file = []
variables = {
    "number": 0,
    "coins": 0,
    "upgrade1_cost": 10,
    "upgrade2_cost": 10,
    "upgrade3_cost": 10,
    "upgrade4_cost": 10,
    "upgrade5_cost": 10
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
        "upgrade3": 15,
        "upgrade4": 5,
        "upgrade5": 1
    }

    for key in guh.keys():
        guh_keys.append(key)
        guh_values.append(guh[key])


def run():
    global number
    global coins
    number = random.choices(guh_keys, weights=guh_values)[0]
    if isinstance(number, str):
        print(format_str(lang_file["buy_upgrade"]+lang_file[number]))
        match number:
            case "upgrade1":
                print("guh")
            case "upgrade2":
                print("guh")
            case "upgrade3":
                print("guh")
            case "upgrade4":
                print("guh")
            case "upgrade5":
                print("guh")
        number = 0
        if coins >= 10:
            number = -10

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
run()
print_current()
