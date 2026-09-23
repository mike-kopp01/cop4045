# Question 3
import csv 
import os
from typing import Dict, List, Tuple

SN = Dict[str, Tuple[str, List[str]]]

def add_user(sn: SN, username: str, fullname: str) -> bool:
    try:
        is_new = username not in sn
        if is_new:
            sn[username] = (fullname, [])
            return is_new
    except TypeError as error:
        print(f"Cannot add '{username}': {error}")
        raise

def add_friend(sn: SN, user1: str, user2: str) -> bool:
    try:
        if user1 == user2 or user1 not in sn or user2 not in sn:
            return False
        for a, b in ((user1, user2), (user2, user1)):
            if b not in sn[a][1]:
                sn[a][1].append(b)
        return True
    except TypeError as error:
        print(f"cannot link '{user1}' and '{user2}': {error}")
        raise

def get_friends(sn: SN, user1: str, distance: int) -> List[str]:
    try:
        if user1 not in sn or distance < 1:
            return []
        friends, level = [], [user1]
        for _ in range(distance):
            level = list(dict.fromkeys(
                f for u in level for f in sn.get(u, ("", []))[1]
                if f != user1 and f not in friends))
            friends += level
        return friends
    except TypeError as error:
        print(f"Cannot get the friends of '{user1}': {error}")

def save_network(filename: str, sn: SN) -> None:
    try:
        with open(filename, "w", newline="") as file:
            csv.writer(file).writerows(
                [user, name] + friends for user, (name, friends) in sn.items())
    except OSError as error:
        print(f"Cannot save '{filename}': {error}")
        raise

def load_network(filename: str) -> SN:
    try:
        with open(filename, newline="") as file:
            return {r[0]: (r[1], r[2:]) for r in csv.reader(file) if r}
    except (OSError, IndexError) as error:
        print(f"cannot load '(filename)' {error}")
        raise

def main() -> None:
    folder = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(folder, "network.csv")
    sn: SN = {}
    for user, name in [("alice", "Alice Smith"), ("maria", "Maria Cortez"), ("joe", "Joe Adams"), ("eve", "Evelyn Cooper"), ("david", "David Benson")]:
        add_user(sn, user, name)
    for a, b in [("alice", "maria"), ("maria", "joe"), ("maria", "david"), ("joe", "eve")]:
        add_friend(sn, a, b)

    print("network:", sn)
    print("add_user(alice) ", add_user(sn, "alice", "Alice Smith"))
    print("add_friend(zoe) ", add_friend(sn, "alice", "zoe"))
    for d in range(1, 4):
        print(f"get_friends(alice,{d}) ", get_friends(sn, "alice", d))
    print("get_friends(zoe,2) ", get_friends(sn, "zoe", 2))

    save_network(csv_file, sn)
    print("loaded == saved ", load_network(csv_file) == sn)
    print("csv_file =", csv_file)
    try:
        load_network(os.path.join(folder, "missing.csv"))
    except FileNotFoundError:
        print(" FileNotFound handled in the main()")

if __name__ == "__main__":
    main()
        

    
