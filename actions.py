# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.

# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des pièces visitées par le joueur.

        Args:
            game (Game): Objet jeu.
            list_of_words (list): Mots de la commande, ex: ["history"].
            number_of_parameters (int): Nombre de paramètres attendus (0).
        Returns:
            bool: True si exécuté correctement, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word)
                  )  # La commande 'history' ne prend pas de paramètre.
            return False

        player = game.player
        player.get_history()  # Affiche l'historique
        return True

    def back(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        if not player.history:
            print("\nImpossible de revenir en arrière : aucun historique.\n")
            return False

        # Revenir à la pièce précédente
        previous_room = player.history.pop()
        player.current_room = previous_room

        # Afficher la description et les sorties disponibles
        print("\nVous êtes maintenant dans :",
              player.current_room.get_long_description())

        player.get_history()

        return True
    def check(game, list_of_words, number_of_parameters):
        """
            Affiche la description de la pièce + les items présents dans l'inventaire.
            Paramètres :
                game (Game)
                list_of_words (list)
                number_of_parameters (int) : attendu 0 pour 'look'
            """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

                
        # Inventaire du joueur
        print(game.player.get_inventory())
        return True
        
    def looke(game, list_of_words, number_of_parameters):
        """
            Affiche la description de la pièce + les items présents dans la pièce.
            Paramètres :
                game (Game)
                list_of_words (list)
                number_of_parameters (int) : attendu 0 pour 'look'
            """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room
        # Description longue (avec sorties)
        print(room.get_long_description())
        # Inventaire de la pièce (items présents)
        print(room.get_inventory())
        return True

    def look(game, list_of_words, number_of_parameters):
        """
        Affiche la description de la pièce + les items présents + les PNJ présents.
        Paramètres :
            game (Game)
            list_of_words (list)
            number_of_parameters (int) : attendu 0 pour 'look'
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room

        # 1) Description longue (avec sorties)
        print(room.get_long_description())

        # 2) Inventaire de la pièce (items présents)
        print(room.get_inventory())

        # 3) PNJ présents (si l'attribut characters existe et n'est pas vide)
        pnjs = getattr(room, "characters", [])
        if pnjs:
            print("PNJ présents :")
            for c in pnjs:
                # suppose que Character.__str__ renvoie "Nom : description (NomDeSalle)"
                print(f" - {c}")
        else:
            print("Il n'y a pas de PNJ ici.")




    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
    
        item_name = list_of_words[1]
        player = game.player
        room = player.current_room
    
        info = room.inventory.get(item_name)
        if info is None:
            print(f"\n'{item_name}' n'est pas présent dans cette pièce.\n")
            return False
    
        # Décrémenter la quantité dans la pièce
        qty_room = info.get("quantity", 1)
        if qty_room <= 1:
            del room.inventory[item_name]
        else:
            info["quantity"] = qty_room - 1
    
        # Incrémenter la quantité chez le joueur
        pinfo = player.inventory.get(item_name)
        if pinfo is None:
            # copier description/poids, quantity=1
            player.inventory[item_name] = {
                "description": info.get("description", ""),
                "weight": info.get("weight", 0),
                "quantity": 1
            }
        else:
            pinfo["quantity"] = pinfo.get("quantity", 1) + 1
    
        print(f"\nVous avez pris '{item_name}'.\n")
        return True




    def drop(game, list_of_words, number_of_parameters):
        """
        Repose un item dans la pièce courante, en le retirant de l'inventaire du joueur.
        Usage: drop <item_name>
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))  # "prend 1 seul paramètre"
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # 1) Vérifier que l'item existe chez le joueur
        pinfo = player.inventory.get(item_name)
        if pinfo is None:
            print(f"\nVous ne possédez pas '{item_name}'.\n")
            return False

        # 2) Décrémenter la quantité chez le joueur
        qty_player = pinfo.get("quantity", 1)
        if qty_player <= 1:
            # retirer complètement l'entrée
            del player.inventory[item_name]
        else:
            pinfo["quantity"] = qty_player - 1

        # 3) Incrémenter la quantité dans la pièce (création si absent)
        rinfo = room.inventory.get(item_name)
        if rinfo is None:
            # on crée l'entrée dans la pièce avec qty=1, en copiant description/poids
            room.inventory[item_name] = {
                "description": pinfo.get("description", ""),
                "weight": pinfo.get("weight", 0),
                "quantity": 1
            }
        else:
            rinfo["quantity"] = rinfo.get("quantity", 1) + 1

        print(f"\nVous avez reposé '{item_name}' dans la pièce.\n")
        return True

    def talk(game, list_of_words, number_of_parameters):
        """
        Permet de discuter avec un PNJ présent dans la pièce.
        """
        player = game.player
        room = player.current_room

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        target_name = list_of_words[1]

        found_character = None

        if hasattr(room, "characters"):
            for npc in room.characters:
                if target_name.lower() in npc.name.lower():
                    found_character = npc
                    break

        if found_character:
            found_character.get_msg()
            return True
        else:
            print(f"\nIl n'y a personne du nom de '{target_name}' ici.\n")
            return False


    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))     
            #print(MSG1.format(command_word=command_word))    

            return False
        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True

    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True