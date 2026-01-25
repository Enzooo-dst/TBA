"""
Module définissant la classe Character.
Gère les PNJ, leurs dialogues et leurs déplacements.
"""
import random

# Note: L'import de DEBUG se fait localement dans move() pour éviter l'import circulaire.

class Character:
    """
    Classe représentant un personnage non-joueur (PNJ).

    Attributes:
        name (str): Nom du personnage.
        description (str): Description du personnage.
        current_room (Room): Salle actuelle du personnage.
        msgs (list): Liste des messages que le personnage peut dire.
    """

    def __init__(self, name, description, current_room, msgs=None):
        """
        Constructeur de la classe Character.
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = list(msgs) if msgs is not None else []

    def __str__(self):
        """Représentation textuelle du personnage."""
        return f"{self.name} : {self.description} ({self.current_room.name})"

    def move(self) -> bool:
        """
        Déplace le PNJ aléatoirement dans une pièce adjacente.

        Returns:
            bool: True si le déplacement a eu lieu, False sinon.
        """
        # Import local pour éviter l'import circulaire avec game.py
        # pylint: disable=import-outside-toplevel
        try:
            from game import DEBUG
        except ImportError:
            DEBUG = False

        # 1. Le personnage a une chance sur deux de se déplacer
        if random.choice([True, False]):
            exits = self.current_room.exits
            available_exits = [room for room in exits.values() if room is not None]

            if available_exits:
                next_room = random.choice(available_exits)
                old_room_name = self.current_room.name
                new_room_name = next_room.name

                self.current_room.remove_character(self)
                next_room.add_character(self)

                if DEBUG:
                    print(f"DEBUG: {self.name} s'est déplacé de "
                          f"'{old_room_name}' vers '{new_room_name}'.")
                return True

        if DEBUG:
            print(f"DEBUG: {self.name} a décidé de ne pas bouger.")
        return False

    def get_msg(self):
        """
        Affiche le prochain message du PNJ et le remplace en fin de liste (cycle).
        """
        if not self.msgs:
            print(f"{self.name} n'a rien à dire.")
            return

        message = self.msgs.pop(0)
        print(message)
        self.msgs.append(message)
