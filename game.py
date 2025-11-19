# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms

        Entrance = Room("un vaste océan", "vous naviguez dans une eau houlante. Vous apercevez une île à l'horizon.")
        self.rooms.append(Entrance)
        CrocoIsland = Room("Croco Island", "vous allez devoir traverser un marécage rempli de crocodiles, attention à ne pas perdre de matelots !")
        self.rooms.append(CrocoIsland)
        Cyclone = Room("une tempête furieuse", "vous devrez faire les bon choix pour la traverser avec brio.")
        self.rooms.append(Cyclone)
        Taverne = Room("la Taverne", "vous avez l'opportunité de recruter des membres d'équipage contre des pièces d'or.")
        self.rooms.append(Taverne)
        Tortues = Room("Turtle Island", "des tortues très rares sont cachées sur l'île, vous pouvez en attraper quelques-unes pour les vendre à la taverne.")
        self.rooms.append(Tortues)
        PreTReasure = Room("Treasure Island", "après une heure de marche dans la forêt vous voilà dans une grotte, une immense porte en bois se dresse devant vous.")
        self.rooms.append(PreTReasure)
        Questions = Room("le phare aux questions (F.A.Q)", "plus précisément dans le phare du terrifiant père Fouras, répondez à ses questions et il vous laissera récupérer des pièces d'or venant de la cage aux tigres. ")
        self.rooms.append(Questions)
        TreasureCave = Room("la cave aux trésors", "vous avez réussi à regrouper un équipage de valereux pirates et méritez entièrement votre trésor !")
        self.rooms.append(TreasureCave)



        # Create exits for rooms

        Entrance.exits = {"N" : CrocoIsland, "E" : Taverne, "S" : Cyclone, "O" : PreTReasure, "U" : None, "D" : None}
        CrocoIsland.exits = {"N" : None, "E" : Questions, "S" : None, "O" : None, "U" : None, "D" : None}
        Questions.exits = {"N" : None, "E" : None, "S" : Taverne, "O" : None, "U" : None, "D" : None}
        Cyclone.exits = {"N" : None, "E" : Tortues, "S" : None, "O" : None, "U" : None, "D" : None}
        Tortues.exits = {"N" : Taverne, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        Taverne.exits = {"N" : None, "E" : None, "S" : None, "O" : Entrance, "U" : None, "D" : None}
        Taverne.exits = {"N" : None, "E" : None, "S" : None, "O" : Entrance, "U" : None, "D" : None}           
        PreTReasure.exits = {"N" : None, "E" : Entrance,  "S" : None, "O" : None, "U" : None, "D" : TreasureCave}
        TreasureCave.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : PreTReasure, "D" : None}
        
        # Setup player and starting room

        nom_joueur = input("\nEntrez votre nom: ")
        print(nom_joueur)
        while (len(str(nom_joueur)) < 3) or (len(str(nom_joueur)) > 15):
            nom_joueur= input("\nEntrez un nom entre 2 et 15 caractères : ")
        self.player = Player(nom_joueur)
        self.player.current_room = Entrance

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        # On traite les exceptions pour les commandes avec plusieurs mots 
        command_string = command_string.strip()
        list_of_words = command_string.split(" ") if command_string else [""]

        direction_valide = True
        command_word = list_of_words[0]
        direction_word = ""
        if len(list_of_words) > 1:
            direction_word = list_of_words[1].upper()
        direction_possible = ["N", "E", "S", "O", "U", "D", "NORD", "EST", "SUD", "OUEST", "UP","DOWN"]
        
        #gestion de la commande go
        
        if command_word == "go" and len(list_of_words) >= 2: # On vérifie que la commande go est bien suivie d'une direction
            if direction_word in direction_possible:  #si commande après go est une direction valide 
                list_of_words[1] = direction_word[0]  #on remplace le nom de la direction par la lettre correspondante
                direction_valide = True
            else : 
                print("\nLa commande 'go' prend 1 seul paramètre parmi N, E, S, O, U, D, NORD, EST, OUEST, SUD, UP, DOWN. \n")
                direction_valide = False
        elif command_word == "go" : 
            print("Il faut indiquer une direction après avoir écrit 'go'. \n")
            direction_valide = False
        
        # If the command is not recognized, print an error message
        if command_word == "":
            print("")
        elif command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        elif (direction_valide == True) and (command_word in self.commands.keys()):
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue dans cette chasse au trésor, {self.player.name} le brave !")
        print("Entrez 'help' si jamais vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
