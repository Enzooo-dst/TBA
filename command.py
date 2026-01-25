"""
Module définissant la classe Command.
Structure les commandes disponibles dans le jeu.
"""

class Command:
    """
    Classe représentant une commande du jeu.

    Attributes:
        command_word (str): Le mot-clé de la commande.
        help_string (str): Le message d'aide.
        action (callable): La fonction à exécuter.
        number_of_parameters (int): Le nombre de paramètres attendus.
    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        """
        Constructeur de la classe Command.
        """
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    def __str__(self):
        """
        Retourne la représentation textuelle de la commande (pour l'aide).
        """
        return self.command_word + self.help_string
