import random

# Define the Character class.
class Character:

    def __init__(self, name, description, current_room, msgs=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        # Important : éviter la liste mutable par défaut partagée entre instances
        self.msgs = list(msgs) if msgs is not None else []

    def __str__(self):
        return f"{self.name} : {self.description} ({self.current_room.name})"

    def move(self):
        """
        Déplace le PNJ aléatoirement dans une pièce adjacente.
        Retourne True si le déplacement a eu lieu, False sinon.
        """
        # IMPORT LOCAL de la variable DEBUG pour éviter l'import circulaire avec game.py
        # On le place ici et non en haut du fichier.
        try:
            from game import DEBUG
        except ImportError:
            DEBUG = False

        # 1. Le personnage a une chance sur deux de se déplacer
        if random.choice([True, False]):

            # 2. Récupérer les sorties valides (non None)
            exits = self.current_room.exits
            available_exits = [room for room in exits.values() if room is not None]

            # S'il y a des sorties disponibles
            if len(available_exits) > 0:
                # Choisir une pièce au hasard
                next_room = random.choice(available_exits)

                # Sauvegarde des noms pour le debug
                old_room_name = self.current_room.name
                new_room_name = next_room.name

                # Gestion du déplacement via les méthodes de Room
                self.current_room.remove_character(self)
                next_room.add_character(self)

                # Affichage conditionnel (Debug)
                if DEBUG:
                    print(f"DEBUG: {self.name} s'est déplacé de '{old_room_name}' vers '{new_room_name}'.")

                return True

        # Si le PNJ ne bouge pas
        if DEBUG:
            print(f"DEBUG: {self.name} a décidé de ne pas bouger.")

        return False

    def get_msg(self):
        """
        Affiche le prochain message du PNJ et le remplace en fin de liste (cycle).
        """
        # Vérification de sécurité si la liste est vide ou non définie
        if not self.msgs:
            print(f"{self.name} n'a rien à dire.")
            return
    
        # 1. On retire le premier message de la liste et on le récupère
        message = self.msgs.pop(0)
    
        # 2. On l'affiche
        print(message)
    
        # 3. On le remet à la fin de la liste pour créer le cycle
        self.msgs.append(message)