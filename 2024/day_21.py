from __future__ import annotations

from collections import Counter
from typing import Any, Optional
import itertools as it

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

number_dict = {
"77":"",      "78":">",    "79":">>",   "74":"v",    "75":"v>",  "76":"v>>", "71":"vv",   "72":"vv>", "73":"vv>>", "70":">vvv", "7A": ">>vvv",
"87":"<",     "88":"",     "89":">",    "84":"<v",   "85":"v",   "86":"v>",  "81":"<vv",  "82":"vv",  "83":"vv>",  "80":"vvv",  "8A": "vvv>",
"97":"<<",    "98":"<",    "99":"",     "94":"<<v",  "95":"<v",  "96":"v",   "91":"<<vv", "92":"<vv", "93":"vv",   "90":"<vvv", "9A": "vvv",
"47":"^",     "48":">^",   "49":"^>>",  "44":"",     "45":">",   "46":">>",  "41":"v",    "42":"v>",  "43":"v>>",  "40":">vv",  "4A": ">>vv",
"57":"<^",    "58":"^",    "59":"^>",   "54":"<",    "55":"",    "56":">",   "51":"<v",   "52":"v",   "53":"v>",   "50":"vv",   "5A": "vv>",
"67":"<<^",   "68":"<^",   "69":"^",    "64":"<<",   "65":"<",   "66":"",    "61":"<<v",  "62":"v>",  "63":"v",    "60":"<vv",  "6A": "vv",
"17":"^^",    "18":">^^",  "19":"^^>>", "14":"^",    "15":"^>",  "16":"^>>", "11":"",     "12":">",   "13":">>",   "10":">v",   "1A": ">>v",
"27":"<^^",   "28":"^^",   "29":">^^",  "24":"<^",   "25":"^",   "26":"^>",  "21":"<",    "22":"",    "23":">",    "20":"v",    "2A": "v>",
"37":"<<^^",  "38":"<^^",  "39":"^^",   "34":"<<^",  "35":"^>",  "36":"^",   "31":"<<",   "32":"<",   "33":"",     "30":"<v",   "3A": "v",
"07":"^^<",   "08":"^^^",  "09":"^>>",  "04":"^^<",  "05":"^^",  "06":">^^", "01":"^<",   "02":"^",   "03":">^",   "00":"",     "0A": ">",
"A7":"^^^<<", "A8":"<^^^", "A9":"^^^",  "A4":"^^<<", "A5":"<^^", "A6":"^^",  "A1":"^<<",  "A2":"<^",  "A3":"^",    "A0":"<",    "AA": "",
                      }

""" 
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
"""

direction_dict = {
"^^":"",   "^A":">",   "^<":"v<",  "^v":"v",  "^>":"v>",
"A^":"<",  "AA":"",    "A<":"v<<", "Av":"<v", "A>":"v",
"<^":">^", "<A":">>^", "<<":"",    "<v":">",  "<>":">>",
"v^":"^",  "vA":"^>",  "v<":"<",   "vv":"",   "v>":">",
">^":"<^", ">A":"^",   "><":"<<",  ">v":"<",  ">>":"",
}


#input_data = ["029A", "980A", "179A", "456A", "379A"]
input_data = ["671A", "083A", "582A", "638A", "341A",]
NUMBER_DIRECTIONAL_KEYPADS = 26

def convert(pairs:dict[str,int])->dict[str,int]:
    tmp=""
    new_key = {}
    for pair, repeat in pairs.items():
        if pair in number_dict:
            tmp = number_dict[pair] + "A"
        else:
            tmp = direction_dict[pair] + "A"
        for p1,p2 in it.pairwise("A"+tmp):
            new_pair = p1+p2
            if new_pair not in new_key:
                new_key[new_pair] = 0
            new_key[new_pair] += repeat

    return new_key

def main(data):
    total_complexity = 0
    for passwd in data:
        key = passwd
        pairs = dict(Counter([a + b for a, b in it.pairwise("A"+key)]))
        for i in range(NUMBER_DIRECTIONAL_KEYPADS):
            pairs = convert(pairs)
        total_punches = sum(pairs.values())
        print(total_punches, key)
        complexity = int(passwd[:-1]) * total_punches
        total_complexity += complexity

    print(total_complexity)


def find_best_arrangement(move:str, key:str):
    best_arrangement = None
    min_len = None
    for new_key in map("".join,it.permutations(key)):
        new_key += "A"
        # invalid moves
        if move == "70" and new_key == "vvv>A":
            continue
        if move == "7A" and new_key == "vvv>>A":
            continue
        if move == "40" and new_key == "vv>A":
            continue
        if move == "4A" and new_key == "vv>>A":
            continue
        if move == "10" and new_key == "v>A":
            continue
        if move == "1A" and new_key == "v>>A":
            continue
        if move == "07" and new_key == "<^^A":
            continue
        if move == "04" and new_key == "<^^A":
            continue
        if move == "01" and new_key == "<^A":
            continue
        if move == "A7" and new_key == "<<^^^A":
            continue
        if move == "A4" and new_key == "<<^^A":
            continue
        if move == "A1" and new_key == "<<^A":
            continue



        lvl1 = convert(new_key)
        lvl2 = convert(lvl1)
        if min_len is None:
            min_len = len(lvl2)
            best_arrangement = new_key
        if len(lvl2) < min_len:
            best_arrangement = new_key
            min_len = len(lvl2)
    return best_arrangement



main(input_data)



# ===========================================================================================
# DIJKSTRA CODE USED TO REFINE DICTIONARIES USED ABOVE
# ===========================================================================================
# from astar import AStar, Node
# input_data = ["029A", "980A", "179A", "456A", "379A"]
# input_data = ["671A", "083A", "582A", "638A", "341A",]
# NUMBER_DIRECTIONAL_KEYPADS = 6
#
#
# def main(data):
#     def cb(obj: DijkstraObj) -> bool:
#         return obj.required_number == ""
#
#     total_complexity = 0
#
#     for passwd in data:
#         key_pads: list[DirectionalKeyPad|NumberKeyPad] = []
#         for kp in range(NUMBER_DIRECTIONAL_KEYPADS):
#             key_pads.append(DirectionalKeyPad())
#         key_pads.append(NumberKeyPad())
#
#         start = DijkstraObj(key_pads, passwd)
#         astar = AStar(start)
#         final_node = astar.find_until(cb)
#         path_nodes = astar.get_path(final_node)
#
#         total_punches = len(path_nodes) - 1
#         print(total_punches, passwd)
#         complexity = int(passwd[:-1]) * total_punches
#         total_complexity += complexity
#
#     print(total_complexity)
#
#
# class DijkstraObj:
#     def __init__(self, key_pads: list[NumberKeyPad|DirectionalKeyPad], required_number):
#         self.key_pads = key_pads
#         self.required_number = required_number
#
#     def key(self) -> str:
#         str = ""
#         for kp in self.key_pads:
#             str += kp.current
#         return f"{str}_{self.required_number}"
#
#     def push_button(self,symbol,keypads:list[NumberKeyPad|DirectionalKeyPad])->Optional[str]:
#         this_keypad, *rest_keypads = keypads
#         if this_keypad.can_move(symbol):
#             this_keypad.move(symbol)
#         else:
#             return None
#         if isinstance(this_keypad,DirectionalKeyPad) and symbol == "A":
#             return self.push_button(this_keypad.current, rest_keypads)
#         if isinstance(this_keypad, NumberKeyPad) and symbol == "A":
#             if this_keypad.current == self.required_number[0]:
#                 return self.required_number[1:]
#             return None
#         return self.required_number
#
#     def children(self) -> list[DijkstraObj]:
#         if self.required_number == "":
#             return []
#
#         valid_next_states = []
#
#         # human can hit any of toplevel keypad buttons
#         keypad_buttons = "^v><A"
#         for kpb in keypad_buttons:
#             new_keypads: list[NumberKeyPad|DirectionalKeyPad] = [kp.copy() for kp in self.key_pads]
#             current_keypad, *rest_keypads = new_keypads
#             current_keypad.current = kpb
#             number_to_press = self.push_button(kpb,rest_keypads)
#             if number_to_press is not None:
#                 valid_next_states.append(DijkstraObj( new_keypads, number_to_press) )
#
#         return valid_next_states
#
#     def __str__(self):
#         return self.key()
#
#     def __repr__(self):
#         return self.key()
#
#     def edge_cost(self, prev: DijkstraObj) -> int:
#         return 1000*len(self.required_number)
#
#     def eta(self, node=None) -> int:
#             return 0
#
#
# """
#
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
# """
#
#
# class NumberKeyPad:
#     move_dict = {
#         "7A": "7", "7>": "8", "7v": "4",
#         "8A": "8", "8>": "9", "8<": "7", "8v": "5",
#         "9A": "9", "9<": "8", "9v": "6",
#         "4A": "4", "4^": "7", "4>": "5", "4v": "1",
#         "5A": "5", "5^": "8", "5>": "6", "5v": "2", "5<": "4",
#         "6A": "6", "6^": "9", "6v": "3", "6<": "5",
#         "1A": "1", "1>": "2", "1^": "4",
#         "2A": "2", "2^": "5", "2<": "1", "2>": "3", "2v": "0",
#         "3A": "3", "3^": "6", "3<": "2", "3v": "A",
#         "0A": "0", "0^": "2", "0>": "A",
#         "AA": "A", "A<": "0", "A^": "3",
#     }
#
#     def __init__(self, current="A"):
#         self.current = current
#
#     def copy(self):
#         return NumberKeyPad(self.current)
#
#     def can_move(self, symbol: str) -> bool:
#         return self.current + symbol in NumberKeyPad.move_dict
#
#     def move(self, symbol: str) -> Optional[str]:
#         if self.can_move(symbol):
#             self.current = NumberKeyPad.move_dict[self.current + symbol]
#             return self.current
#         else:
#             raise KeyError("Cannot move to that position")
#
#     def movable_directions(self):
#         return [key[1] for key in NumberKeyPad.move_dict if key[0] == self.current]
#
#     def __str__(self):
#         return self.current
#
# """
#         +---+---+
#         | ^ | A |
#     +---+---+---+
#     | < | v | > |
#     +---+---+---+
# """
#
#
# class DirectionalKeyPad:
#     move_dict = {
#         "^A": "^", "^>": "A", "^v": "v",
#         "AA": "A", "Av": ">", "A<": "^",
#         "<A": "<", "<>": "v",
#         "vA": "v", "v^": "^", "v>": ">", "v<": "<",
#         ">A": ">", "><": "v", ">^": "A",
#     }
#
#     def __init__(self,current="A"):
#         self.current = current
#
#     def copy(self):
#         return DirectionalKeyPad(self.current)
#
#     def can_move(self, symbol: str) -> bool:
#         tmp = self.current + symbol
#         return tmp in DirectionalKeyPad.move_dict.keys()
#
#     def move(self, symbol: str) -> Optional[str]:
#         if self.can_move(symbol):
#             self.current = DirectionalKeyPad.move_dict[self.current + symbol]
#             return self.current
#         else:
#             raise KeyError("Cannot move to that position")
#
#     def movable_directions(self):
#         return [key[1] for key in DirectionalKeyPad.move_dict if key[0] == self.current]
#
#     def __str__(self):
#         return self.current
#
#
# main(input_data)
