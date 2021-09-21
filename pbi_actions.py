from functions import get_access_token
from functions import refresh_dataset
from functions import refresh_dataset_by_names
from functions import get_dataset_id_in_workspace_by_name
from functions import get_environment_settings
from functions import get_workspace_id_by_name
import json
from sys import argv

commands = {
    "refresh_dataset": refresh_dataset,
    "refresh_dataset_by_names": refresh_dataset_by_names,
    "get_access_token": get_access_token
}

# #Bestandsnaam is altijd eerste value in argv, die mag dus weg
argv.pop(0)

# #Opslaan opgegeven omgeving
environment = argv.pop(0)
ENV_FILE = '.env.json'

#Ophalen van omgevingsvariabelen voor authenticatie
environment_settings = get_environment_settings(ENV_FILE)
sa_name = environment_settings[environment][0]['sa_name']
client_id = environment_settings[environment][0]['client_id']
client_token = environment_settings[environment][0]['client_token']

# Check of er uberhaupt een command meegegeven is, wanneer geen gevonden exit het script
if not argv:
       print("Geen commando meegegeven!")
       exit(1)

# Aargument daarna is altijd de uit te voeren command, print ook statements om te kunnen debuggen
received_command = argv.pop(0)
print('Opgegeven input aan het script: ' + str(argv))
print('Command wat uitgevoerd gaat worden: ' + '\'' + received_command + '\'' + ' op omgeving ' + '\'' + environment + '\'')

# match command naar functie met de dictionary, bestaat deze niet dan krijgen we None terug
matched_command = commands.get(received_command)

#check of command bestaat, als dat het geval is roep deze aan met de rest van de argumenten
if not matched_command:
       print("Geen geldig commando gevonden.")
       exit(1)
matched_command(*argv, client_id, client_token)
exit(0)