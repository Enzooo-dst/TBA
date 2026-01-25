"""
Module définissant la classe Room.
Représente les lieux du jeu, leurs sorties et leur contenu.
"""

class Room:
    """
    Classe représentant un lieu dans le jeu.

    Attributes:
        name (str): Le nom du lieu.
        description (str): La description du lieu.
        exits (dict): Les sorties disponibles vers d'autres salles.
        inventory (dict): Les objets présents dans la salle.
        characters (list): Les personnages présents dans la salle.
    """

    def __init__(self, name: str, description: str):
        """
        Constructeur de la classe Room.

        Args:
            name (str): Nom du lieu.
            description (str): Description du lieu.
        """
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = []

    def get_exit(self, direction: str):
        """
        Retourne la salle dans la direction donnée si elle existe.

        Args:
            direction (str): La direction (N, E, S, O, U, D).

        Returns:
            Room | None: L'objet Room correspondant ou None.
        """
        return self.exits.get(direction)

    def get_exit_string(self) -> str:
        """
        Retourne une chaîne décrivant les sorties disponibles.

        Returns:
            str: Liste des sorties formatée.
        """
        exit_string = "Sorties: "
        for exit_key, room in self.exits.items():
            if room is not None:
                exit_string += exit_key + ", "
        return exit_string.strip(", ")

    def get_inventory(self) -> str:
        """
        Produit une chaîne représentant l'inventaire de la pièce.

        Returns:
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

    def get_long_description(self) -> str:
        """
        Retourne une description complète de la salle (nom, desc, sorties).

        Returns:
            str: Description formatée.
        """
        return (
            f"\nVous venez d'arriver dans {self.name}, {self.description}\n\n"
            f"{self.get_exit_string()}\n"
        )

    def add_character(self, character):
        """
        Ajoute un PNJ à cette room si pas déjà présent.

        Args:
            character (Character): Le personnage à ajouter.
        """
        if character not in self.characters:
            self.characters.append(character)
            character.current_room = self

    def remove_character(self, character):
        """
        Retire un PNJ de cette room s'il y est.

        Args:
            character (Character): Le personnage à retirer.
        """
        if character in self.characters:
            self.characters.remove(character)
