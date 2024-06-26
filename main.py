import obd

print("main.py est lancé")

connection = None

def connect_obd():
    global connection
    print("tentative de connexion...")
    try:
        # chez moi: port com8
        connection = obd.OBD("COM8")
        print("Statut de la connexion :", connection.status())
        if connection.is_connected():
            print("Connecté à l'adaptateur OBD-II.")
        else:
            print("Échec de la connexion à l'adaptateur OBD-II.")
    except Exception as e:
        print(f"Erreur lors de la tentative de connexion: {e}")

def clear_error_codes():
    global connection
    if connection and connection.is_connected():
        response = connection.query(obd.commands.CLEAR_DTC)
        if response.is_positive():
            print("Les codes d'erreur ont été effacés avec succès.")
        else:
            print("Échec de l'effacement des codes d'erreur.")
    else:
        print("Non connecté à l'adaptateur OBD-II.")

def read_error_codes():
    global connection
    if connection and connection.is_connected():
        response = connection.query(obd.commands.GET_DTC)
        if response.value:
            print("Codes d'erreur trouvés :")
            for code in response.value:
                print(f"Code: {code[0]}, Description: {code[1]}")
            
            while True:
                answer = input("Voulez-vous effacer ces codes d'erreur ? (oui/non) : ").strip().lower()
                if answer == "oui":
                    clear_error_codes()
                    break
                elif answer == "non":
                    print("Les codes d'erreur n'ont pas été effacés.")
                    break
                else:
                    print("Réponse non reconnue. Veuillez répondre par 'oui' ou 'non'.")
        else:
            print("Aucun code d'erreur détecté.")
    else:
        print("Non connecté à l'adaptateur OBD-II.")


while True:
    command = input("Entrez une commande (connect, read, quit) : ").strip().lower()
    if command == "quit":
        print("Fermeture de la connexion et arrêt du programme.")
        if connection:
            connection.close()
        print("La connexion a été fermée.")
        break
    elif command == "connect":
        connect_obd()
    elif command == "read":
        read_error_codes()
    else:
        print("Commande non reconnue.")

print("Programme terminé.")
