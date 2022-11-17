import discord, json, logging, pdb, validators
from argparse import ArgumentParser
from discord import Client
from shodan import Shodan

"""Tri des imports"""


class EsieaBot(Client):
    

    def __init__(self, fileconf):
        super().__init__()
        
        self.fileconf = fileconf # Définission du fichier de conf
        self.logFile = "bot.log" # Définission du fichier de log
        
        """
        Je définis le niveau de log sur INFO car je souhaite seulement récupérer les commandes que les utilisateurs font avec le BOT.
        Les autres niveau de log comme DEBUG étaient trop verbeux à mon gout
        """
        logging.basicConfig(filename=self.logFile, level=logging.INFO) 
        
        
        """On définit un dictionnaire de fonctionnalités, de cette manière si on veut ajouter plus de fonctionnalités à notre bot, on à simplement à en ajouter ici"""
        self.dict_cmd = {
            "!iplog" : self.on_iplog,
            "!mult_egypt" : self.mult_egypt,
            "!syracuse" : self.syracuse,
            "!help" : self.help,
        }
        
        try:
            with open(self.fileconf, 'r') as conf_json:     # On ouvre le fichier json de configuration 
                self.b_config = json.load(conf_json)             # On stocke le contenu du fichier dans 'config'
            
            self.token = self.b_config["token"]                  # On séléctionne le token de connexion        
            self.run(self.token) # Lancement du BOT
            
        except Exception:
            print('Fichier invalide un fichier json existant doit être séléctionné')
            
        

    
    
    
    
    async def on_ready(self):
        print("Le bot est prêt !")
        logging.info(f"{self.user} s'est connecté\n") # On notifie dans le fichier de log lorsque le bot se connecte au serveur
       
       
       
        
    async def on_message(self, message):
        
        ok = True
        """On regarde si l'on recoit le caractère des commandes du bot qui est '!' """
        try:
            if message.content[0] == '!': 
                ok = True
            
            # On ajoute une fonctionnalité qui demande d'arreter les @everyone parce que c'est chiant les spams
            elif message.content == '@everyone':
                await message.channel.send(f"{message.author} tu vas vite t'arrêter avec tes @everyone") 
                await message.channel.send(file=discord.File('images/ane.png'))         # On upload une image disuasive
                
        except Exception:
            pass
    
        
        """On regarde si la commande envoyé par l'utilisateur est dans le dico"""

        for key in self.dict_cmd:
            if message.content.startswith(key):
                """
                On utilise *args pour ne pas être embeté par le nombre d'argument que l'utilisateur va entrer. 
                Si la fonction demande 20 arguments c'est possible sans changer quoique ce soit au code
                Cela rend donc l'implémentation de nouvelles fonctions bien plus simple
                """
                logging.info(f"{message.author} a utilisé la commande {message.content.split()[0]}\n") # On rentre dans les logs l'utilisateur utilisant le bot ainsi que la commande utilisé
                """
                J'ai été un peu frustré ici car je souhaitais utiliser les logs d'une autre manière directement dans les fonctions pour plus de précison
                exemple avoir pour la commande !iplog l'ip sur lequel l'utilisateur fait une requete.
                Malheuresement je n'ai pas trouvé comment récupérer le nom d'utilisateur de celui qui envoit le message.
                """
                
                await message.channel.send("Bien reçu ! Veuillez patienter quelques instants :white_check_mark: \n")
                await message.channel.send(self.dict_cmd[key](*message.content.split()))
                
            
    def on_iplog(self, *args)->str: #On fait savoir que la classe retourne une string
        
        
        """
        Fonction permettant d'avoir les donnés de géolocalisation d'une IP publique entrée par l'utilisateur
        Prend une ip en entrée et retourne une string
        """


        """On récupère la clé d'api shodan dans le fichier de configuration json"""
        api = Shodan(self.b_config["shodan_api"])
        
        if len(args)!=2:
            logging.error(f"Erreur de syntaxe, trop peu ou trop d'arguments donné \n")
            return "Mauvause syntaxe, la commande prend un argument :x:"
        
        """On vérifie que la valeur entrée par l'utilisateur est bien une IP de type Ipv4"""
        
        try:
            if not validators.ipv4(args[1]):
                logging.error(f"Erreur IP invalide --> {args[1]} \n")
                return f"Entre une IP publique valide :x:"
            
        except Exception as e:
            
            """J'ajoute les logs en format erreur, pour avoir une traces de certaines erreurs et pouvoir debug plus facilement ensuite"""
            logging.error(f"Erreur lors de la vérification de l'IP : \n{e}")
            
            return f"Erreur lors de la vérification de l'IP, veuillez ré-essayer :x:"
        
        
        """On vérifie qu'on arrive à contacter Shodan"""
        try:
            rep = api.host(args[1])
            
        except Exception as e:
            
            """
            J'ajoute les logs en format erreur, pour avoir une traces de certaines erreurs et pouvoir debug plus facilement ensuite
            Ici on vérifie qu'il n'y a pas d'erreur en contactant shodan
            """
            logging.error(f"Erreur lors de l'appel de shodan {e}\n")
            
            return f"Erreur lors de l'appel de Shodan veuillez ré-essayer :x:"
        
        
        """On récupère la longitude et la latitude dans le résutat de shodan"""
        longitude = str(rep['longitude'])
        latitude = str(rep['latitude'])
        
        
        """On définit l'url openstreetmap"""
        url = "".join(['https://www.openstreetmap.org/?mlat=', latitude, '&mlon=', longitude, '#map=14/', latitude, '/', longitude])
        
        if not validators.url(url):
            """
            J'ajoute les logs en format erreur, pour avoir une traces de certaines erreurs et pouvoir debug plus facilement ensuite
            Ici on vérifie qu'il n'y a pas de problème avec l'URL
            """
            logging.error(f"Erreur lors de la validation de l'URL suivante : {url}")
            
            return f"Erreur lors de la construction de l'URL, veuillez ré-essayer :x:"
        
        
        else:
            
            """J'enrichis les logs avec des détails, ici l'IP utilisé"""
            logging.info(f"Une requete a été faite pour localiser l'IP {args[1]}.\n")
            
            return f"Voici les informations de géolocalisation pour l'IP **{args[1]}**\n{url} "
        
    
    
    
    def mult_egypt(self, *args)->int: #On fait savoir que la classe retourne un int
        
        """
        Fonction permettant le calcul de la multiplication egyptienne à partir de deux input de l'utilisateur
        Prend deux int en entrée et retourne un int
        """
        
        z = 0
        
        if len(args)!=3:
            logging.error(f"Erreur de syntaxe, trop peu ou trop d'arguments donné \n")
            return "Mauvaise syntaxe, la commande prend 2 arguments :x:"
        
        
        """On récupère les valeurs rentré par l'utilisateur"""
        value1 = args[1]
        value2 = args[2]
        
        
        """On regarde si les deux valeurs rentré par l'utilisateur sont des nombres entier si non on renvoie un message d'erreur """
        if value1.isnumeric() and value2.isnumeric():
            print("calcul en cours")
        else:
            return "Entrez deux nombres entier valides :x:"

        """On convertir les valeurs en int pour la suite des calculs"""
        val1 = int(value1)
        val2 = int(value2)
        
        
        """On fait le calcul de la multiplication egyptienne comme dans le 1er TP"""
        try:
            if val1 < 0 or val2 < 0:
                return "Entrez un nombre supérieur à 0"
            else :
                while val1 != 0:
                    if val1%2 != 0:
                        z += val2
                    val2 += val2
                    val1 = int(val1/2)
                    
                """J'enrichis les logs avec des détails, ici les 2 nombres utilisés pour la multiplication"""
                logging.info(f"La multiplication egyptienne a été réalisé avec les nombres {value1} et {value2}.\n")
                return f"Résultat de la multiplication --> **{z}**"
            
        #Si une erreur se présente, on l'affiche      
        except Exception as e:
            logging.error(f"Erreur lors de la multiplication egyptienne :\n{e}")
            return f"Erreur lors du calcul de la multiplication, Veuillez ré-essayer :x:"
        
        
    def syracuse(self, *args)->list: #On fait savoir que la classe retourne une liste
        
        """
        Fonction permettant de calculer la suite de syracuse à partir d'un input utilisateur
        Prend un int en entrée et retourne une liste
        """
        
        if len(args)!=2:
            logging.error(f"Erreur de syntaxe, trop peu ou trop d'arguments donné \n")
            return "Mauvaise syntaxe, la commande prend un argument :x:"
        
        #On récupère la valeur rentré par l'utilisateur
        nombre = args[1]
        liste_retour = []
        
        
        """On check si le nombre entré est un nombre entier ou non, si il ne l'est pas, on retourne un message d'erreur"""
        if nombre.isnumeric(): 
            print("calcul en cours")
        else:
            return "Entrez un nombre entier positif valide :x:"

        
        """On convertit le nombre entré par l'utilisateur en float pour la suite des calculs"""
        base_nombre = float(nombre)
        
        """On effectue la suite de syracuse comme dans le premier TP """
        while(base_nombre>1):
            if base_nombre%2==0:
                base_nombre = base_nombre/2
                liste_retour.append(base_nombre)
            else:
                base_nombre = 3*base_nombre+1
                liste_retour.append(base_nombre)
                
                
        """J'enrichis les logs avec des détails, ici le nombre utilisé pour la suite de syracuse"""
        logging.info(f"La suite de Syracuse a été réalisé avec le nombre {nombre}.\n")
        
        return f"Résultat de la suite de syracuse --> **{liste_retour}**"
                
            
            
    def help(self, *args):
        
        if len(args)!=1:
            logging.error(f"Erreur de syntaxe, un ou plusieurs arguments donné dans une commande qui n'en prend pas \n")
            return "La commande help ne prend pas d'arguments, utilisez simplement '**!help**' :thumbsup:"
        
        """"On affiche la liste des commandes disponibles pour le bot"""
        
        return """ 
    **Liste des commandes** :heart: \n
    :one: **!help** --> Voir la liste des commandes disponibles :thinking:  \n
    :two: **!iplog** __<IP>__ --> Avoir les informations de géolocalistaion sur un IP publique :earth_americas: \n
    :three: **!mult_egypt** __<entier1> <entier2>__ --> Prend deux nombres entier et effectue la multiplication égyptienne :man_teacher: \n
    :four: **!syracuse** __<entier>__ --> Prend un entier et effectue la suite de syracuse de celui-ci :loop: """



def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file", required=True, dest="config") #On configure l'option -c/--config
    return parser.parse_args()
        
        

def main():
    
    
    args = parse_args()

    fileconf = args.config      # On récupère le fichier passé en commandline
    reader = EsieaBot(fileconf)
    
    
if __name__ == '__main__':
	main()
