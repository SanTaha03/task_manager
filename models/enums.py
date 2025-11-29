from enum import Enum

class TaskState(str, Enum):
    A_FAIRE = "À faire"
    EN_COURS = "En cours"
    REALISE = "Réalisé"
    ABANDONNE = "Abandonné"
    EN_ATTENTE = "En attente"
    ANNULE = "Annulé"