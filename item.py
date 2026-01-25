"""
Module définissant la classe Item.
Représente les objets que le joueur peut ramasser.
"""

class Item:
    """
    Classe représentant un objet dans le jeu.

    Attributes:
        name (str): Le nom de l'objet.
        description (str): La description de l'objet.
        weight (float): Le poids de l'objet.
    """

    def __init__(self, name: str):
        """
        Constructeur de la classe Item.

        Args:
            name (str): Le nom de l'objet.
        """
        self.name = name
        self.description = ""
        self.weight = 0.0

    def __str__(self) -> str:
        """
        Représentation textuelle de l'objet.
        """
        return f"{self.name} : {self.description} ({self.weight} kg)"
