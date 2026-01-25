"""
Module Actions.
Contient les méthodes statiques exécutées par les commandes.
"""

# Messages d'erreur constants
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """
    Regroupe les fonctions d'action du jeu.
    Toutes les méthodes sont statiques car elles n'utilisent pas l'instance 'Actions'.
    Elles prennent l'objet 'game' comme premier paramètre.
    """

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """Gère le déplacement du joueur."""
        player = game.player
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        direction = list_of_words[1]

        # Vérification pré-déplacement : La porte du trésor
        next_room = player.current_room.exits.get(direction)

        if next_room and next_room.name == "la cave aux trésors":
            # Le gardien bloque le passage si l'équipage n'est pas complet
            if player.crew < 8:
                print("\n⛔ LE GARDIEN VOUS BARRE LA ROUTE !")
                print("Gardien : 'Halte ! Tu dois avoir un équipage au complet d'au moins "
                      "8 valeureux pirates pour pouvoir briser la porte !'")
                print(f"(Vous n'avez que {player.crew} hommes.)\n")
                return False
            print("\n🔓 Gardien : 'Je vois que vous êtes bien entouré. Vous pouvez passer.'")

        # On tente le mouvement normal
        if player.move(direction):
            # Si le mouvement réussit, on vérifie les événements de la nouvelle salle
            game.check_room_events()
            return True
        return False

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """Quitte le jeu."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """Affiche l'aide."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        """Affiche l'historique."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        game.player.get_history()
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """Revient à la salle précédente."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        if not player.history:
            print("\nImpossible de revenir en arrière : aucun historique.\n")
            return False

        previous_room = player.history.pop()
        player.current_room = previous_room
        print("\nVous êtes maintenant dans :", player.current_room.get_long_description())
        game.check_room_events()
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """Affiche l'inventaire."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        print(game.player.get_inventory())
        return True

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """Observe la salle actuelle."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room
        print(room.get_long_description())
        print(room.get_inventory())

        pnjs = getattr(room, "characters", [])
        if pnjs:
            print("PNJ présents :")
            for character in pnjs:
                print(f" - {character.name} : {character.description}")
        else:
            print("Il n'y a pas de PNJ ici.")
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """Prend un objet."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
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

        qty_room = info.get("quantity", 1)
        if qty_room <= 1:
            del room.inventory[item_name]
        else:
            info["quantity"] = qty_room - 1

        pinfo = player.inventory.get(item_name)
        if pinfo is None:
            player.inventory[item_name] = {
                "description": info.get("description", ""),
                "weight": info.get("weight", 0),
                "quantity": 1
            }
        else:
            pinfo["quantity"] = pinfo.get("quantity", 1) + 1

        print(f"\nVous avez pris '{item_name}'.\n")
        return True

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """Pose un objet."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        pinfo = player.inventory.get(item_name)
        if pinfo is None:
            print(f"\nVous ne possédez pas '{item_name}'.\n")
            return False

        qty_player = pinfo.get("quantity", 1)
        if qty_player <= 1:
            del player.inventory[item_name]
        else:
            pinfo["quantity"] = qty_player - 1

        rinfo = room.inventory.get(item_name)
        if rinfo is None:
            room.inventory[item_name] = {
                "description": pinfo.get("description", ""),
                "weight": pinfo.get("weight", 0),
                "quantity": 1
            }
        else:
            rinfo["quantity"] = rinfo.get("quantity", 1) + 1

        print(f"\nVous avez reposé '{item_name}' dans la pièce.\n")
        return True

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """Discute avec un PNJ."""
        player = game.player
        room = player.current_room
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        target_name = list_of_words[1]

        # VÉRIFICATION SPÉCIALE POUR FOURAS
        if "fouras" in target_name.lower():
            npc_present = any("fouras" in c.name.lower() for c in room.characters)
            if npc_present:
                game.handle_fouras_interaction()
                return True

        # VÉRIFICATION SPÉCIALE POUR LE MARCHAND
        if "marchand" in target_name.lower():
            npc_present = any("marchand" in c.name.lower() for c in room.characters)
            if npc_present:
                game.handle_merchant_interaction()
                return True

        # Comportement standard pour les autres PNJ
        found_character = None
        if hasattr(room, "characters"):
            for npc in room.characters:
                if target_name.lower() in npc.name.lower():
                    found_character = npc
                    break

        if found_character:
            found_character.get_msg()
            return True

        print(f"\nIl n'y a personne du nom de '{target_name}' ici.\n")
        return False

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """Affiche les quêtes."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        game.player.quest_manager.show_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """Affiche les détails d'une quête."""
        command_length = len(list_of_words)
        if command_length < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        quest_title = " ".join(list_of_words[1:])
        current_counts = {"Se déplacer": game.player.move_count}
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """Active une quête."""
        command_length = len(list_of_words)
        if command_length < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        quest_title = " ".join(list_of_words[1:])
        if game.player.quest_manager.activate_quest(quest_title):
            return True
        print(f"\nImpossible d'activer '{quest_title}'.\n")
        return False

    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """Affiche les récompenses."""
        command_length = len(list_of_words)
        if command_length != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        game.player.show_rewards()
        return True
