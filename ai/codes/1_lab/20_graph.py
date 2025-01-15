graph_a = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": ["G"],
    "E": ["H"],
    "F": [],
    "G": [],
    "H": []
}


graph = {
    "Biratnagar": {"Itahari": 22, "Rangeli": 25, "Biratchowk": 30},
    "Itahari": {"Biratnagar": 22, "Dharan": 20, "Biratchowk": 11},
    "Dharan": {"Itahari": 20},
    "Biratchowk": {"Biratnagar": 30, "Itahari": 11, "Kanepokhari": 10},
    "Kanepokhari": {"Biratchowk": 10, "Rangeli": 25, "Urlabari": 12},
    "Rangeli": {"Biratnagar": 25, "Kanepokhari": 25, "Urlabari": 40},
    "Urlabari": {"Kanepokhari": 12, "Rangeli": 40, "Damak": 6},
    "Damak": {"Urlabari": 6},
}


