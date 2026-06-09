
import logging

#configuration du système de logs
logging.basicConfig(
    filename="logs/school.log",#fichier ou les logs seront stockés
    level=logging.INFO,#niveau des logs (INFO, WARNING, ERROR)
    format="%(asctime)s [%(levelname)s] %(message)s" #format des messages
)

logger = logging.getLogger() #crée l'objet logger utilisable partout

def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)

