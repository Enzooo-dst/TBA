Lien de présentation vidéo du projet : https://drive.google.com/file/d/1DLH7jAlYwK4VQYPt4azxpYq150Z85avq/view?usp=drive_link

# 🏴‍☠️ Chasse au Trésor - Aventure Textuelle

**Hissez les voiles, Capitaine !**
Bienvenue dans **Chasse au Trésor**, un jeu de rôle (RPG) textuel codé en Python. Explorez des îles mystérieuses, gérez votre équipage et amassez de l'or pour atteindre le trésor ultime.

## 📝 Synopsis

Vous incarnez un capitaine pirate naviguant sur des eaux dangereuses. Votre objectif est d'entrer dans la **Cave aux Trésors**. Cependant, l'entrée est gardée par un colosse qui ne laisse passer que les capitaines dirigeant un équipage complet et puissant.

Vous devrez explorer, résoudre des énigmes, chasser des animaux rares et commercer pour renforcer vos rangs avant d'atteindre la victoire.

## ✨ Fonctionnalités Clés

### 1. Gestion d'Équipage et Économie 💰
* **Votre Équipage :** Vous commencez l'aventure avec **6 matelots**.
* **Le Recrutement :** Pour gagner, vous devez recruter de nouveaux pirates à la **Taverne**. Le Marchand vous vendra des hommes contre de l'or (5 pièces/homme).
* **Gagner de l'Or :**
    * Chassez des **tortues rares** sur *Turtle Island* et revendez-les au Marchand.
    * Répondez aux énigmes du **Père Fouras** dans le Phare pour gagner des bourses d'or.

### 2. Événements Interactifs & Dangers ⚡
Le monde est vivant et réagit à vos actions :
* **La Tempête (Cyclone) :** Une zone dangereuse où vous devrez faire des choix rapides (QCM) pour sauver votre navire. **Attention :** de mauvaises décisions entraîneront la mort définitive de vos marins.
* **Le Gardien du Trésor :** Il bloque l'accès à la salle finale si votre équipage n'est pas au complet (Minimum 8 ou 10 membres selon la difficulté).

### 3. Système de Quêtes Avancé 📜
Le jeu intègre un gestionnaire de quêtes (`QuestManager`) :
* **Grand Explorateur :** Visitez tous les lieux de la carte.
* **Esquiver la tempête :** Survivez au passage dans le Cyclone.
* **Énigmes du Phare :** Trouvez les bonnes réponses aux questions de Fouras.

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

## 🎮 Guide des Commandes

Utilisez ces commandes pour interagir avec le monde :

| Commande | Syntaxe | Description |
| :--- | :--- | :--- |
| **Se déplacer** | `go <N/E/S/O>` | Se déplacer vers le Nord, l'Est, le Sud ou l'Ouest. |
| **Parler** | `talk <Nom>` | **Vital !** Permet de commercer avec le `Marchand` ou de répondre à `Fouras`. |
| **Observer** | `look` | Affiche la description de la salle, les objets et les personnages. |
| **État Joueur** | `check` | Affiche votre **inventaire**, votre **or** et le nombre de **matelots**. |
| **Prendre** | `take <objet>` | Ramasser un objet (ex: `take tortue`). |
| **Poser** | `drop <objet>` | Poser un objet au sol. |
| **Quêtes** | `quests` | Voir la liste des quêtes et leur statut. |
| **Détails Quête**| `quest <Nom>` | Voir les objectifs précis d'une quête. |
| **Historique** | `history` | Voir les lieux visités. |
| **Quitter** | `quit` | Quitter la partie. |

## 🗺️ Aperçu du Monde

* **L'Océan (Départ) :** Le point central.
* **La Taverne :** Le lieu de commerce (Achat d'équipage / Vente de tortues).
* **Turtle Island :** Lieu de chasse (Tortues).
* **Le Cyclone :** Zone de danger (Risque de perte d'équipage).
* **Le Phare (F.A.Q) :** Lieu de savoir et de gain d'or rapide via Fouras.
* **Treasure Island :** L'antichambre du trésor, gardée par le Gardien.

## 🌟 Exemple de Scénario (Spoilers !)

1.  Allez à *Turtle Island*, ramassez une `tortue`.
2.  Allez à la *Taverne*, faites `talk Marchand`.
3.  Choisissez l'option pour **vendre la tortue** (+5 Or).
4.  Utilisez l'or pour **acheter un matelot**.
5.  Allez voir *Fouras*, répondez à son énigme pour gagner encore plus d'or.
6.  Une fois votre équipage au complet, foncez vers *Treasure Island* et affrontez le Gardien !

## 📂 Architecture du Code

* `game.py` : Moteur principal, initialise le monde et les événements (Tempête, Fouras).
* `player.py` : Gère le joueur, l'inventaire et le **compteur d'équipage**.
* `room.py` : Définit les lieux et leurs connexions.
* `character.py` : Gère les PNJ (Personnages Non Joueurs) et leurs déplacements.
* `quests.py` : Système de gestion des objectifs et récompenses.
* `actions.py` : Contient la logique de toutes les commandes (`go`, `talk`, etc.).

---
*Projet réalisé en Python - Bon vent et bonne chasse !* 🏴‍☠️