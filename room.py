# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string



    def get_inventory(self) -> str:
            """
            Produit une chaîne représentant l'inventaire de la pièce.
            Retour:
                str: Chaîne prête à afficher.
            """
            if not self.inventory:
                return "Il n'y a rien ici."

            lines = ["La pièce contient :"]
            for item_name, info in self.inventory.items():
                desc = info.get("description", "")
                weight = info.get("weight", 0)
                lines.append(f"    - {item_name} : {desc} ({weight} kg)")
            return "\n".join(lines)
                    # Define the get_exit method. 

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous venez d'arriver dans {self.name}, {self.description}\n\n{self.get_exit_string()}\n"
