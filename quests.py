"""
Module définissant les classes Quest et QuestManager.
Gère le système de quêtes, d'objectifs et de récompenses.
"""

class Quest:
    """
    Cette classe représente une quête dans le jeu.

    Attributes:
        title (str): Titre de la quête.
        description (str): Description.
        objectives (list): Liste des objectifs textuels.
        completed_objectives (list): Liste des objectifs accomplis.
        is_completed (bool): Statut de complétion global.
        is_active (bool): Si la quête est active.
        reward (str): Description de la récompense.
    """

    def __init__(self, title, description, objectives=None, reward=None):
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.completed_objectives = []
        self.is_completed = False
        self.is_active = False
        self.reward = reward

    def activate(self):
        """Active la quête et affiche un message."""
        self.is_active = True
        print(f"\n🗡️  Nouvelle quête activée: {self.title}")
        print(f"📝 {self.description}\n")

    def complete_objective(self, objective, player=None):
        """Marque un objectif comme accompli."""
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"✅ Objectif accompli: {objective}")

            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)
            return True
        return False

    def complete_quest(self, player=None):
        """Termine la quête et donne la récompense."""
        if not self.is_completed:
            self.is_completed = True
            print(f"\n🏆 Quête terminée: {self.title}")
            if self.reward:
                print(f"🎁 Récompense: {self.reward}")
                if player:
                    player.add_reward(self.reward)
            print()

    def get_status(self):
        """Retourne le statut formaté de la quête."""
        if not self.is_active:
            return f"❓ {self.title} (Non activée)"
        if self.is_completed:
            return f"✅ {self.title} (Terminée)"
        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"⏳ {self.title} ({completed_count}/{total_count} objectifs)"

    def get_details(self, current_counts=None):
        """Retourne les détails complets de la quête avec progression."""
        details = f"\n📋 Quête: {self.title}\n"
        details += f"📖 {self.description}\n"

        if self.objectives:
            details += "\nObjectifs:\n"
            for objective in self.objectives:
                status = "✅" if objective in self.completed_objectives else "⬜"
                objective_text = self._format_objective_with_progress(objective, current_counts)
                details += f"  {status} {objective_text}\n"

        if self.reward:
            details += f"\n🎁 Récompense: {self.reward}\n"
        return details

    def _format_objective_with_progress(self, objective, current_counts):
        """Formate l'objectif avec un compteur de progression si applicable."""
        if not current_counts:
            return objective

        for counter_name, current_count in current_counts.items():
            if counter_name in objective:
                required = self._extract_number_from_text(objective)
                if required is not None:
                    return f"{objective} (Progression: {current_count}/{required})"
        return objective

    def _extract_number_from_text(self, text):
        """Extrait le premier nombre trouvé dans une chaîne."""
        for word in text.split():
            if word.isdigit():
                return int(word)
        return None

    def check_room_objective(self, room_name, player=None):
        """Vérifie les objectifs liés à la visite de lieux."""
        room_objectives = [
            f"Visiter {room_name}", f"Explorer {room_name}",
            f"Aller à {room_name}", f"Entrer dans {room_name}"
        ]
        for objective in room_objectives:
            if self.complete_objective(objective, player):
                return True
        return False

    def check_action_objective(self, action, target=None, player=None):
        """Vérifie les objectifs liés à des actions."""
        if target:
            variations = [
                f"{action} {target}", f"{action} avec {target}",
                f"{action} le {target}", f"{action} la {target}"
            ]
        else:
            variations = [action]

        for objective in variations:
            if self.complete_objective(objective, player):
                return True
        return False

    def check_counter_objective(self, counter_name, current_count, player=None):
        """Vérifie les objectifs liés à des compteurs (ex: Marcher 10 fois)."""
        for objective in self.objectives:
            if counter_name in objective and objective not in self.completed_objectives:
                words = objective.split()
                for word in words:
                    if word.isdigit():
                        required = int(word)
                        if current_count >= required:
                            self.complete_objective(objective, player)
                            return True
        return False

    def __str__(self):
        return self.get_status()


class QuestManager:
    """Classe gérant l'ensemble des quêtes du jeu."""

    def __init__(self, player=None):
        self.quests = []
        self.active_quests = []
        self.player = player

    def add_quest(self, quest):
        """Ajoute une quête au jeu."""
        self.quests.append(quest)

    def activate_quest(self, quest_title):
        """Active une quête via son titre."""
        for quest in self.quests:
            if quest.title == quest_title and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return True
        return False

    def complete_objective(self, objective_text):
        """Complète un objectif manuellement dans les quêtes actives."""
        for quest in self.active_quests:
            if quest.complete_objective(objective_text):
                if quest.is_completed:
                    self.active_quests.remove(quest)
                return True
        return False

    def check_room_objectives(self, room_name):
        """Vérifie les objectifs de salle pour toutes les quêtes actives."""
        for quest in self.active_quests[:]:
            quest.check_room_objective(room_name, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def check_action_objectives(self, action, target=None):
        """Vérifie les objectifs d'action."""
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def check_counter_objectives(self, counter_name, current_count):
        """Vérifie les objectifs de compteur."""
        for quest in self.active_quests[:]:
            quest.check_counter_objective(counter_name, current_count, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def get_quest_by_title(self, title):
        """Récupère une quête par son titre."""
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None

    def show_quests(self):
        """Affiche la liste des quêtes."""
        if not self.quests:
            print("\nAucune quête disponible.\n")
            return
        print("\n📋 Liste des quêtes:")
        for quest in self.quests:
            print(f"  {quest.get_status()}")
        print()

    def show_quest_details(self, quest_title, current_counts=None):
        """Affiche les détails d'une quête."""
        quest = self.get_quest_by_title(quest_title)
        if quest:
            print(quest.get_details(current_counts))
        else:
            print(f"\nQuête '{quest_title}' non trouvée.\n")
