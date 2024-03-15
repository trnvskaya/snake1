#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 0.1

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot. Každý vnitřní uzel stromu obsahuje vždy dvě položky: název uzlu a seznam potomků (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam).

Příklady validních stromů:
    - triviální strom o 1 uzlu: [1, []]
    - triviální strom o 1 uzlu s opačným pořadím ID a potomků: [[], 2]
    - triviální strom o 3 uzlech: [1, [2, 3]]
        (listové uzly ve stromu o výšce >= 2 mohou být pro zjednodušení zapsány i bez prázdného seznamu potomků)

Příklady nevalidních stromů:
    - None
    - []
    - [666]
    - [1, 2]
    - (1, [2, 3])


Strom bude vykreslen podle následujících pravidel:
    - Vykresluje se shora dolů, zleva doprava.
    - Uzel je reprezentován jménem, které je stringovou serializací objektu daného v definici uzlu.
    - Uzel v hloubce N bude odsazen zlava o N×{indent} znaků, přičemž hodnota {indent} bude vždy kladné celé číslo > 1.
    - Má-li uzel K potomků, povede:
        - k 1. až K-1. uzlu šipka začínající znakem ├ (UTF16: 0x251C)
        - ke K. uzlu šipka začínající znakem └ (UTF16: 0x2514)
    - Šipka k potomku uzlu je vždy zakončena znakem > (UTF16: 0x003E; klasické "větší než").
    - Celková délka šipky (včetně úvodního znaku a koncového ">") je vždy {indent}, výplňovým znakem je zopakovaný znak ─ (UTF16: 0x2500).
    - Všichni potomci uzlu jsou spojeni na úrovni počátku šipek svislou čarou │ (UTF16: 0x2502); tedy tam, kde není jako úvodní znak ├ nebo └.
    - Pokud název uzlu obsahuje znak `\n` neodsazujte nijak zbytek názvu po tomto znaku.
    - Každý řádek je ukončen znakem `\n`.

Další požadavky na vypracovní:
    - Pro nevalidní vstup musí implementace vyhodit výjimku `raise Exception('Invalid tree')`.
    - Mít codestyle v souladu s PEP8 (můžete ignorovat požadavek na délku řádků - C0301 a používat v odůvodněných případech i jednopísmenné proměnné - C0103)
        - otestujte si pomocí `pylint --disable=C0301,C0103 trees.py`
    - Vystačit si s buildins metodami, tj. žádné importy dalších modulů.


Příklady vstupu a výstupu:
INPUT:
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...├──>6.023e+23
│...└──>2.718281828
├──>3
│...├──>x
│...└──>y
└──>4

INPUT:
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44

INPUT:
[6, [5, ['dva\nradky']]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>dva
radky

Potřebné UTF16-art znaky:
└ ├ ─ │

Odkazy:
https://en.wikipedia.org/wiki/Box_Drawing
"""

def validate_tree(tree):
    """
    function for validaing trees
    """
    if not isinstance(tree, list) or len(tree) != 2:
        raise ValueError('Invalid tree')
    new_list = False
    element = False

    # Check if any of two parts is a tree
    if isinstance(tree[0], list):
        new_list = tree[0]
        element = tree[1]
    if isinstance(tree[1], list):
        new_list = tree[1]
        element = tree[0]

    if new_list is False:
        raise ValueError('Invalid tree')
    return new_list, element

def printTree(tree, separator, indent, stage, parent) -> str:
    """
    function to print a tree
    """
    new_list, element = validate_tree(tree)
    result = ''

    tmp = ''
    for a in range(stage - 1):
        symbol = separator if stage < 2 or parent[a] else "│"
        tmp += symbol + separator * (indent - 1)
    #print(tmp)

    if stage != 0:
        tmp += "└" if stage >= 1 and parent[stage - 1] else "├"
        # if last:
        #     tmp += "└"
        # else:
        #     tmp += "├"
        tmp += (indent - 2) * "─"
        tmp += ">"
    else:
        tmp += ""
    #print(tmp)

    suffix = "" if "\n" in tmp else "\n"

    # Append the element and suffix to tmp
    tmp += str(element) + suffix
    result += tmp
    #print('res do ifov: ' + result)

    if len(new_list) == 2 and (isinstance(new_list[0], list) != isinstance(new_list[1], list)):
        newParent = parent.copy()
        newParent.append(True)
        #print('pervyi if do rekursiji: \n' + result)
        result += printTree(new_list, separator, indent, stage + 1, newParent)
        #print('pervyi if:\n' + result)
    else:
        for coef, child in enumerate(new_list):
            if isinstance(child, list):
                # Child is a list again
                newParent = parent.copy()
                newParent.append(coef == len(new_list) - 1)
                #print('vtoroi if do rekursiji: \n' + result)
                result += printTree(child, separator, indent, stage + 1, newParent)
                #print('vtoroi if:\n' + result)
                continue
            tmp = ''
            for a in range(stage):
                symbol = "│" if separator != " " and not parent[a] else separator
                if (separator == " " and not parent[a]):
                    symbol = "│"
                tmp += ((symbol + (separator * (indent - 1))))
            tmp += "└" if (coef == len(new_list) - 1) else "├"
            tmp += ((indent - 2) * "─") + ">"
            tmp += str(child) + ("" if '\n' in tmp else '\n')
            result += tmp

    return result

def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    """
    function that renders a tree
    """
    result = ''
    result += printTree(tree, separator, indent, 0, [])
    return result
