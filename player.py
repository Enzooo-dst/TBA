"""
Module définissant la classe Player.
Gère l'état du joueur, son inventaire, son historique et son équipage.
"""
from quests import QuestManager

class Player:
    """
    Classe représentant le joueur.
    """

    def __init__(self, name):
        """Constructeur du joueur."""
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []
        self.crew = 6  # On commence avec 6 membres d'équipage

    def get_history(self):
        """Affiche l'historique des lieux visités."""
        print("\nVous avez déjà visité les pièces suivantes :")
        if not self.history:
            print("- (aucune pour le moment)")
        else:
            for room in self.history:
                print(f"- {room.name}")
        print()

    def get_inventory(self) -> str:
        """
        Produit une chaîne représentant l'inventaire et l'équipage.
        """
        status = f"\n👥 Équipage : {self.crew} matelots valides.\n"

        if not self.inventory:
            return status + "Votre inventaire est vide."

        lines = [status, "Vous disposez des items suivants :"]
        for item_name, info in self.inventory.items():
            description = info.get("description", "")
            weight = info.get("weight", 0)
            qty = info.get("quantity", 1)
            lines.append(f"    - {item_name} (x{qty}) : {description} ({weight} kg)")
        return "\n".join(lines)

    def move(self, direction):
        """
        Déplace le joueur dans une direction donnée.

        Returns:
            bool: True si le déplacement a réussi, False sinon.
        """
        next_room = self.current_room.exits.get(direction)
        if next_room is None:
            if direction in ["N", "E", "S", "O"]:
                print("\nNotre perroquet n'a aperçu aucune île dans cette direction !\n")
            else:
                print("\nIl n'y a pas d'échelle pour monter ou descendre !\n")
            return False

        self.history.append(self.current_room)
        self.current_room = next_room

        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

        print(self.current_room.get_long_description())
        return True

    def add_reward(self, reward):
        """Ajoute une récompense spéciale au joueur."""
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu une récompense spéciale : {reward}\n")

    def show_rewards(self):
        """Affiche les récompenses spéciales."""
        if not self.rewards:
            print("\n🎁 Aucune récompense spéciale obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses spéciales :")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()

    def lose_crew(self, amount):
        """Retire des membres d'équipage."""
        self.crew -= amount
        if self.crew < 0:
            self.crew = 0
        print(f"\n💀 Drame ! Vous avez perdu {amount} membre(s) d'équipage !")
        print(f"Il vous reste {self.crew} matelots fidèles.\n")

    def add_crew(self, amount):
        """Ajoute des membres d'équipage."""
        self.crew += amount
        print(f"\n🤝 Bienvenue à bord ! Vous avez gagné {amount} membre(s) d'équipage !")
        print(f"Vous avez maintenant {self.crew} matelots.\n")
