"""
Module principal Game.
Initialise le jeu, les salles, les personnages et la boucle principale.
"""
from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from quests import Quest

DEBUG = True

class Game:
    """
    Classe principale du jeu.
    Gère l'initialisation et la boucle de jeu.
    """

    def __init__(self):
        """Constructeur du jeu."""
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.characters = []
        self.storm_encountered = False
        # Flags pour les messages uniques
        self.fouras_done = False
        self.fouras_hint_given = False

    def setup(self):
        """Configuration initiale du jeu."""
        self._setup_commands()
        self._setup_rooms_and_characters()
        self._setup_player()
        self._setup_quests()

    def _setup_commands(self):
        """Initialise les commandes disponibles."""
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer", Actions.go, 1)
        self.commands["history"] = Command("history", " : historique", Actions.history, 0)
        self.commands["back"] = Command("back", " : revenir en arrière", Actions.back, 0)
        self.commands["look"] = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["check"] = Command("check", " : inventaire et état", Actions.check, 0)
        self.commands["take"] = Command("take", " <item> : prendre objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <item> : poser objet", Actions.drop, 1)
        self.commands["talk"] = Command("talk", " <nom> : discuter", Actions.talk, 1)
        self.commands["quests"] = Command("quests", " : afficher les quêtes", Actions.quests, 0)
        self.commands["quest"] = Command("quest", " <nom> : détails quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate", " <nom> : activer", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " : récompenses", Actions.rewards, 0)

    def _setup_rooms_and_characters(self):
        """Initialise les salles et les PNJ."""
        # Création des salles
        entrance = Room("un vaste océan", "vous naviguez dans une eau houlante.")
        croco_island = Room("Croco Island", "un marécage rempli de crocodiles.")
        cyclone = Room("une tempête furieuse", "les vents hurlent.")
        taverne = Room("la Taverne", "l'endroit idéal pour recruter.")
        tortues = Room("Turtle Island", "des tortues très rares sont cachées.")
        pre_treasure = Room("Treasure Island", "une immense porte en bois se dresse.")
        questions = Room("le phare aux questions (F.A.Q)", "le repaire du père Fouras.")
        treasure_cave = Room("la cave aux trésors", "l'aboutissement de votre voyage !")

        self.rooms.extend([entrance, croco_island, cyclone, taverne, tortues,
                           pre_treasure, questions, treasure_cave])

        # Configuration des inventaires
        tortues.inventory["tortue"] = {
            "description": "une tortue rare", "weight": 1, "quantity": 1
        }
        taverne.inventory["pièce"] = {
            "description": "une pièce d'or", "weight": 0.1, "quantity": 10
        }

        # Configuration des sorties
        entrance.exits = {
            "N": croco_island, "E": taverne, "S": cyclone, "O": pre_treasure
        }
        croco_island.exits = {"E": questions}
        questions.exits = {"S": taverne}
        cyclone.exits = {"E": tortues}
        tortues.exits = {"N": taverne}
        taverne.exits = {"O": entrance}
        pre_treasure.exits = {"E": entrance, "D": treasure_cave}
        treasure_cave.exits = {"U": pre_treasure}

        # Configuration des PNJ
        fouras = Character("Fouras", "un vieil homme", questions,
                           ["Approche...", "Je garde les clés."])
        questions.add_character(fouras)
        self.characters.append(fouras)

        marchand = Character("Marchand", "recruteur", taverne,
                             ["J'ai des hommes et j'achète les tortues."])
        taverne.add_character(marchand)
        self.characters.append(marchand)

        gardien = Character("Gardien", "colosse", pre_treasure,
                            ["Seul un capitaine digne passera."])
        pre_treasure.add_character(gardien)
        self.characters.append(gardien)

    def _setup_player(self):
        """Configure le joueur."""
        nom_joueur = input("\nEntrez votre nom: ")
        while len(str(nom_joueur)) < 2 or len(str(nom_joueur)) > 15:
            nom_joueur = input("\nEntrez un nom entre 2 et 15 caractères : ")
        self.player = Player(nom_joueur)
        # La salle de départ est la première de la liste (Entrance)
        self.player.current_room = self.rooms[0]

    def _setup_quests(self):
        """Configure les quêtes."""
        objectives_explo = [
            f"Visiter {r.name}" for r in self.rooms if r.name != "la cave aux trésors"
        ]

        exploration_quest = Quest(
            title="Grand Explorateur",
            description="Explorez tous les lieux de ce monde (sauf la cachette finale).",
            objectives=objectives_explo,
            reward="Titre de Grand Explorateur"
        )
        self.player.quest_manager.add_quest(exploration_quest)

        # CORRECTION : Utiliser le manager pour activer la quête
        # Cela permet de l'ajouter à la liste active_quests que le manager surveille.
        self.player.quest_manager.activate_quest("Grand Explorateur")

        # Validation immédiate de la salle de départ pour cette quête
        self.player.quest_manager.check_room_objectives(self.player.current_room.name)

        storm_quest = Quest(
            title="Esquiver la tempête",
            description="Brave la tempête pour sauver ton équipage.",
            objectives=["Survivre au Cyclone"],
            reward="Compass de survie"
        )
        self.player.quest_manager.add_quest(storm_quest)

        self.player.quest_manager.add_quest(Quest(
            "Énigme du Phare I", "Réponds à la première question de Fouras.",
            ["Répondre 9"], "5 pièces d'or"
        ))
        self.player.quest_manager.add_quest(Quest(
            "Énigme du Phare II", "Réponds à la deuxième question de Fouras.",
            ["Répondre perroquet"], "5 pièces d'or"
        ))

    def play(self):
        """Lance la boucle principale du jeu."""
        self.setup()
        self.print_welcome()
        while not self.finished:
            command_string = input("> ")
            self.process_command(command_string)

            command_clean = command_string.strip()
            first_word = command_clean.split()[0].lower() if command_clean else ""
            if first_word in ["go", "back"]:
                for npc in self.characters:
                    if npc.name not in ["Marchand", "Gardien"]:
                        npc.move()
        return None

    def process_command(self, command_string) -> None:
        """Traite la commande saisie par le joueur."""
        command_string = command_string.strip()
        list_of_words = command_string.split(" ") if command_string else [""]
        command_word = list_of_words[0].lower()

        # Gestion intelligente des directions pour 'go'
        if command_word == "go" and len(list_of_words) > 1:
            raw_dir = list_of_words[1].upper()
            mapping = {
                "NORD": "N", "EST": "E", "SUD": "S", "OUEST": "O",
                "UP": "U", "DOWN": "D",
                "N": "N", "E": "E", "S": "S", "O": "O", "U": "U", "D": "D"
            }
            if raw_dir in mapping:
                list_of_words[1] = mapping[raw_dir]
            else:
                list_of_words[1] = raw_dir

        if command_word not in self.commands:
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help'.\n")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        """Affiche le message de bienvenue."""
        print(f"\nBienvenue {self.player.name} ! "
              f"Votre équipage de {self.player.crew} hommes est prêt.")
        print(self.player.current_room.get_long_description())

    # --- ÉVÉNEMENTS SPÉCIAUX ---

    def check_room_events(self):
        """Vérifie les événements liés à la salle actuelle."""
        current_room_name = self.player.current_room.name

        # Tempête
        if current_room_name == "une tempête furieuse" and not self.storm_encountered:
            self.player.quest_manager.activate_quest("Esquiver la tempête")
            self._run_storm_sequence()
            self.storm_encountered = True

        # Fouras
        if current_room_name == "le phare aux questions (F.A.Q)":
            self.player.quest_manager.activate_quest("Énigme du Phare I")
            self.player.quest_manager.activate_quest("Énigme du Phare II")

            if not self.fouras_hint_given:
                print("\n💡 Maintenant que tu as visité le phare du mystérieux Fouras,"
                      " tu as débloqué une quête :")
                print("Pour l'activer tu dois Trouver Fouras et faire 'talk Fouras', "
                      "réponds à ses questions et il te donnera des pièces d'or.\n")
                self.fouras_hint_given = True

    def _run_storm_sequence(self):
        """Exécute la séquence de la tempête."""
        print("\n⚡ UNE VAGUE SCÉLÉRATE ARRIVE SUR TOI ET TON ÉQUIPAGE ! ⚡")
        print("ACTION REQUISE IMMÉDIATE (Vous ne pouvez pas fuir)")
        print("  1 : La prendre de face (Risque pour le navire, équipage protégé)")
        print("  2 : La prendre en biais (Le navire tangue, risque de chute)")

        while True:
            choix1 = input("\nQuel est ton choix (1 ou 2) ? > ")
            if choix1 in ["1", "2"]:
                break
            print("Choix invalide.")

        if choix1 == "2":
            print("\n🌊 Le bateau tangue violemment... Un homme passe par-dessus bord !")
            self.player.lose_crew(1)
        else:
            print("\n🌊 Le bateau craque mais tient bon. L'équipage est secoué mais sauf.")

        print("\n🌪️ Le cœur du Cyclone se rapproche...")
        print("  1 : Foncez dans l'œil du cyclone (Calme mais dangereux)")
        print("  2 : Tenter de fuir la zone (Long et périlleux)")

        while True:
            choix2 = input("\nQuel est ton choix (1 ou 2) ? > ")
            if choix2 in ["1", "2"]:
                break
            print("Choix invalide.")

        if choix2 == "2":
            print("\n💨 Les vents contraires vous ralentissent. "
                  "Une déferlante emporte un autre marin !")
            self.player.lose_crew(1)
        else:
            print("\n💨 Vous traversez le mur de vent et trouvez le calme temporaire de l'œil.")

        self.player.quest_manager.complete_objective("Survivre au Cyclone")

    def handle_fouras_interaction(self):
        """Gère le dialogue interactif avec Fouras."""
        print("\n👴 Fouras : 'Héhéhé ! Tu ne sortiras pas d'ici sans avoir utilisé ta tête.'")

        q1 = self.player.quest_manager.get_quest_by_title("Énigme du Phare I")
        if q1 and q1.is_active and not q1.is_completed:
            print("\n👴 Fouras : 'Question 1 : Combien d'îles (salles) "
                  "sont présentes dans ton monde ?'")
            rep = input("Votre réponse (écrivez le chiffre) > ")
            if rep.strip() == "9":
                print("\n👴 Fouras : 'Bien joué ! Tu as gagné 5 pièces d'or.'")
                self.player.quest_manager.complete_objective("Répondre 9")
                self._give_gold(5)
            else:
                print("\n👴 Fouras : 'Faux ! Tu perds ta chance pour cette question.'")

        q2 = self.player.quest_manager.get_quest_by_title("Énigme du Phare II")
        if q2 and q2.is_active and not q2.is_completed:
            print("\n👴 Fouras : 'Question 2 : Quel animal est votre bras droit "
                  "et se place sur votre épaule ?'")
            rep = input("Votre réponse > ")
            if "perroquet" in rep.lower():
                print("\n👴 Fouras : 'Exactement ! Voici 5 pièces d'or.'")
                self.player.quest_manager.complete_objective("Répondre perroquet")
                self._give_gold(5)
            else:
                print("\n👴 Fouras : 'Non, ce n'est pas ça.'")

        print("\n👴 Fouras : 'La session est terminée.'\n")

    def handle_merchant_interaction(self):
        """Gère le dialogue avec le marchand."""
        print("\n💰 Marchand : 'Bienvenue à la taverne, Capitaine !'")
        print("💰 Marchand : 'Je peux te fournir des hommes (5 or) ou "
              "t'acheter tes tortues (5 or).'")

        while True:
            current_gold = 0
            if "pièce" in self.player.inventory:
                current_gold = self.player.inventory["pièce"]["quantity"]

            tortue_count = 0
            if "tortue" in self.player.inventory:
                tortue_count = self.player.inventory["tortue"]["quantity"]

            print(f"\n--- BOURSE: {current_gold} Or | ÉQUIPAGE: {self.player.crew} "
                  f"| TORTUES: {tortue_count} ---")
            print("1. Acheter un matelot (-5 or)")
            print("2. Vendre une tortue (+5 or)")
            print("3. Quitter la discussion")

            choice = input("Votre choix (1, 2 ou 3) > ")

            if choice == "3":
                print("\n💰 Marchand : 'À la prochaine !'")
                break

            if choice == "1":
                if current_gold >= 5:
                    self._remove_gold(5)
                    self.player.add_crew(1)
                else:
                    print("\n💰 Marchand : 'Pas assez d'argent !'")

            elif choice == "2":
                if tortue_count > 0:
                    if tortue_count == 1:
                        del self.player.inventory["tortue"]
                    else:
                        self.player.inventory["tortue"]["quantity"] -= 1
                    self._give_gold(5)
                    print("\n💰 Marchand : 'Quelle belle bête ! Voici 5 pièces d'or.'")
                else:
                    print("\n💰 Marchand : 'Tu n'as pas de tortue à vendre !'")
            else:
                print("Choix invalide.")

    def _give_gold(self, amount):
        """Ajoute de l'or à l'inventaire."""
        item_name = "pièce"
        pinfo = self.player.inventory.get(item_name)
        if pinfo is None:
            self.player.inventory[item_name] = {
                "description": "une pièce d'or",
                "weight": 0.1,
                "quantity": amount
            }
        else:
            pinfo["quantity"] += amount
        print(f"💰 (+{amount} pièces d'or ajoutées)")

    def _remove_gold(self, amount):
        """Retire de l'or de l'inventaire."""
        if "pièce" in self.player.inventory:
            self.player.inventory["pièce"]["quantity"] -= amount
            if self.player.inventory["pièce"]["quantity"] <= 0:
                del self.player.inventory["pièce"]
            print(f"💰 (-{amount} pièces d'or)")


def main():
    """Point d'entrée du jeu."""
    Game().play()


if __name__ == "__main__":
    main()
