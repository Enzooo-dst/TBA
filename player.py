
# Define the Player class.
class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []  # On commence vide, on ajoutera la salle initiale après setup

    def get_history(self):
        print("\nVous avez déjà visité les pièces suivantes :")
        if not self.history:
             print("- (aucune pour le moment)")
        else:
            for room in self.history:
                print(f"- {room.name}")
        print()

    def move(self, direction):
        next_room = self.current_room.exits.get(direction)
        if next_room is None:
            if direction in ["N", "E", "S", "O"]:
                print("\nNotre perroquet n'a aperçu aucune île dans cette direction !\n")
            else:
                print("\nIl n'y a pas d'échelle pour monter ou descendre !\n")
            return False


        # Ajoute la pièce actuelle dans l'historique avant de bouger
        self.history.append(self.current_room)

        # Mise à jour de la salle
        self.current_room = next_room
      

        print(self.current_room.get_long_description())
        self.get_history()
        return True
