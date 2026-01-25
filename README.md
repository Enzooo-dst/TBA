# 🏴‍☠️ Chasse au Trésor - Aventure Textuelle

Bienvenue dans **Chasse au Trésor**, un jeu d'aventure textuel (RPG) codé en Python. Incarnez un capitaine pirate, naviguez entre les îles, gérez votre équipage et résolvez des énigmes pour trouver le trésor ultime !

**Vidéo descriptive du projet**  
https://drive.google.com/file/d/1DLH7jAlYwK4VQYPt4azxpYq150Z85avq/view?usp=sharing


## 📝 Description

Ce projet est un jeu d'aventure en ligne de commande (CLI). Le joueur explore un monde composé de différents lieux (Room), interagit avec des objets (Item) et des personnages non-joueurs (PNJ).

Le but est d'explorer le monde, de survivre aux dangers (comme les tempêtes) et d'accumuler des richesses en accomplissant des quêtes dynamiques.

## ✨ Fonctionnalités Principales

* **Exploration Libre :** Déplacez-vous à travers différentes zones (Île aux Crocodiles, Taverne, Cyclone, etc.) via les points cardinaux.
* **Système de Quêtes Avancé 📜 :**
    * Activation et suivi de quêtes multiples (exploration, énigmes, survie).
    * Objectifs variés : visiter des lieux, parler à des PNJ, accumuler des objets.
* **Gestion d'Équipage 👥 :** * Vous commencez avec 10 matelots.
    * Vos choix lors des événements (comme la Tempête) impactent directement la survie de votre équipage.
* **Événements Interactifs Scriptés :**
    * ⚡ **Le Cyclone :** Une séquence de choix multiples où vous devez décider comment affronter les vagues et le vent pour minimiser les pertes.
    * 🧩 **Le Père Fouras :** Un PNJ interactif qui pose des questions via la commande `talk`. Répondre correctement vous rapporte de l'or.
* **Inventaire et Économie :** Ramassez des objets, gérez leur poids et accumulez des pièces d'or.
* **PNJ Vivants :** Les personnages (comme Fouras) se déplacent d'une pièce à l'autre de manière autonome.

## 🚀 Installation et Lancement

### Prérequis
* Python 3.x installé sur votre machine.

### Instructions
1.  **Cloner le projet :**
    ```bash
    git clone https://github.com/Enzooo-dst/TBA.git
    cd TBA
    ```

2.  **Lancer le jeu :**
    ```bash
    python game.py
    ```

## 🎮 Commandes du Jeu

Une fois le jeu lancé, utilisez les commandes suivantes dans le terminal :

| Commande | Syntaxe | Description |
| :--- | :--- | :--- |
| **Se déplacer** | `go <N/E/S/O/U/D>` | Aller vers le Nord, Est, Sud, Ouest, Haut ou Bas. |
| **Observer** | `look` | Regarder la description de la salle, les objets et les PNJ présents. |
| **État & Inventaire**| `check` | Voir votre inventaire et le nombre de matelots restants. |
| **Prendre** | `take <objet>` | Mettre un objet dans votre sac. |
| **Poser** | `drop <objet>` | Poser un objet au sol. |
| **Parler** | `talk <nom>` | Discuter avec un PNJ (ex: `talk Fouras` pour les énigmes). |
| **Quêtes** | `quests` | Afficher la liste de toutes les quêtes. |
| **Détails Quête** | `quest <nom>` | Voir les objectifs détaillés d'une quête spécifique. |
| **Activer Quête** | `activate <nom>` | Démarrer manuellement une quête. |
| **Historique** | `history` | Voir la liste des lieux visités. |
| **Retour** | `back` | Revenir à la salle précédente. |
| **Aide** | `help` | Afficher toutes les commandes disponibles. |
| **Quitter** | `quit` | Quitter le jeu. |

## 📂 Structure du Code

Le projet est organisé selon une architecture orientée objet (POO) modulaire :

* `game.py` : Le moteur principal. Initialise le monde, gère la boucle de jeu et les événements spéciaux (Tempête, Fouras).
* `player.py` : Gère le joueur, l'inventaire, l'historique de déplacement et l'équipage.
* `room.py` : Définit les lieux, les descriptions et les connexions (sorties).
* `quests.py` : Classes `Quest` et `QuestManager` pour gérer les objectifs et les statuts.
* `character.py` : Gestion des PNJ et de leur IA de déplacement.
* `item.py` : Définition des objets (poids, description).
* `command.py` & `actions.py` : Traitement des commandes textuelles et logique des actions.

## 🌟 Exemple de Scénario

```text
> Bienvenue Capitaine ! Votre équipage de 10 hommes est prêt.
> Vous êtes dans un vaste océan.

> go S
... Vous entrez dans une tempête furieuse !
⚡ UNE VAGUE SCÉLÉRATE ARRIVE SUR TOI ET TON ÉQUIPAGE ! ⚡
Tu as deux choix :
  1 : La prendre de face
  2 : La prendre en biais
Quel est ton choix (1 ou 2) ? > 2

🌊 Le bateau tangue violemment... Un homme passe par-dessus bord !
💀 Drame ! Vous avez perdu 1 membre(s) d'équipage !
