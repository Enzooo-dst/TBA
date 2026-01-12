from quests import QuestManager
# Define the Player class.
class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []  # On commence vide, on ajoutera la salle initiale après setup
        self.inventory = {}  # Inventaire vide au début
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []

    def get_history(self):
        print("\nVous avez déjà visité les pièces suivantes :")
        if not self.history:
             print("- (aucune pour le moment)")
        else:
            for room in self.history:
                print(f"- {room.name}")
        print()

    def get_inventory(self) -> str:
        """
        Produit une chaîne représentant l'inventaire du joueur.
        Retourne :
            str : Chaîne prête à afficher.
        """
        if not self.inventory:
            return "Votre inventaire est vide."

        lines = ["Vous disposez des items suivants :"]
        for item_name, info in self.inventory.items():
            description = info.get("description", "")
            weight = info.get("weight", 0)
            # On ajoute chaque ligne dans la liste

            lines.append(f"    - {item_name} : {description} ({weight} kg)")
        return "\n".join(lines)


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
        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)


        print(self.current_room.get_long_description())
        self.get_history()
        return True

    
    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.

        Args:
            reward (str): The reward to add.

        Examples:

        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")
    
    def show_rewards(self):
        """
        Display all rewards earned by the player.

        Examples:

        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()