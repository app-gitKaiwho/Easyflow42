# Web App pour la gestion des données des entres les google sheet et le bot discord (formToDiscord.gs)

Ce script est une application web (Web App) conçue pour gérer la communication entre les feuilles Google Sheets et le bot Discord. Le bot Discord peut demander à la Web App une mise à jour des informations sur les entreprises présentes à l'événement ou envoyer ce que les utilisateurs ont entré dans l'interface Discord (login, CV, LinkedIn, créneaux horaires choisis). Ce script à besoin d'être link au google sheet link au google form des entreprises sinon il ne fonctionnera pas.

**Fonctionnement du script :**

1. L'application reçoit des demandes POST, et elle vérifie si la demande contient des données JSON.

2. Si la demande POST contient des données JSON :

   - Elle traite ces données en parcourant chaque clé représentant une entreprise participant à l'événement.
   - Pour chaque entreprise, elle accède à une feuille Google Sheets existante avec le nom de l'entreprise ou la crée si elle n'existe pas.
   - Elle appelle la fonction `writeToSheet` pour écrire les données dans la feuille. Ces données seront ensuite converties en PDF.
     Chaque entreprise utilisera se pdf pour avoir la liste des créneaux horaires (`slots`) des personnes pariticipant aux entretiens.

3. Après avoir traité toutes les clés du JSON, l'application renvoie une réponse indiquant que les données ont été traitées pour toutes les feuilles. Cela confirme au bot discord que leurs données ont été reçues et traitées avec succès.

4. Si la demande POST ne contient pas de données JSON :
   - L'application récupère des données au format JSON depuis la feuille "db_ep" dans Google Sheets. Ces données proviennent d'un formulaire Google donné aux entreprises.
   - Elle renvoie ces données au format JSON en réponse à la demande. Cette fonctionnalité permet au bot Discord de mettre à jour sa base de données à partir des informations fournies par les entreprises.

**Exemple de JSON reçu :**

```json
{
  "SWISSCOM": {
    "linktopost": "https://www.swisscom.ch/de/privatkunden.html",
    "slots": [
      {
        "freespot": 3,
        "value": "9h15-9h30",
        "logins": ["1", "2", "3"]
      }
      // Autres créneaux horaires...
    ]
  },
  "MUTUEL": {
    "linktopost": "https://www.mutuel.com",
    "slots": [
      {
        "freespot": 3,
        "value": "10h00-10h15",
        "logins": ["4", "5", "6"]
      }
      // Autres créneaux horaires...
    ]
  }
}
```
