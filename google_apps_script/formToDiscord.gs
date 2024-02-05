function doPost(e) {
  // Vérifie si la demande POST contient des données JSON
  if (e.postData && e.postData.type === "application/json") {
    var jsonData = JSON.parse(e.postData.contents);

    // Parcourt chaque clé du JSON
    for (var sheetName in jsonData) {
      var data = jsonData[sheetName];

      // Accède à la feuille existante avec le nom obtenu ou la crée si elle n'existe pas
      var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
      var sheet =
        spreadsheet.getSheetByName(sheetName) ||
        spreadsheet.insertSheet(sheetName);

      // Appelle la fonction writeToSheet pour écrire les données dans la feuille qui sera convertis en PDF pour les entreprises
      writeToSheet(sheet, sheetName, data);
    }

    // Renvoie une réponse indiquant que les données ont été traitées pour toutes les feuilles
    return ContentService.createTextOutput(
      "Données traitées pour toutes les feuilles."
    );
  } else {
    // Si la demande POST ne contient pas de données JSON, renvoie les données au format JSON depuis la feuille "db_ep"
    // Ses données viennent du google form donnée aux entreprise
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("db_ep");
    var data = sheet.getDataRange().getValues();
    var jsonData = convertSheetDataToJson(data);

    return ContentService.createTextOutput(
      JSON.stringify(jsonData)
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

// écris les données dans la feuille google sheet
function writeToSheet(sheet, sheetName, data) {
  // Efface le contenu existant de la feuille
  sheet.clear();

  // Écrit le nom de la clé en tant que titre
  sheet.appendRow([sheetName]);

  // Parcourt les 'slots' et ajoute les 'logins' dans la feuille
  data.slots.forEach((slot) => {
    slot.logins.forEach((login) => {
      // Ajoute chaque 'login' sur une nouvelle ligne
      sheet.appendRow([login]);
    });
  });
}

function convertSheetDataToJson(data) {
  var jsonArray = [];
  var headers = data[0];

  // Parcourt les lignes de données dans la feuille et les transforme en un tableau JSON
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var json = {};
    for (var j = 0; j < row.length; j++) {
      json[headers[j]] = row[j];
    }
    jsonArray.push(json);
  }

  // Transforme le tableau JSON en un format valide pour le bot discord
  var jsonArrayTransformed = transformJson(jsonArray);
  return jsonArrayTransformed;
}

// Transforme les données JSON en un nouveau format valide pour le bot discord
function transformJson(jsonData) {
  let transformed = {};

  jsonData.forEach((entry) => {
    let companyName = entry.name;
    let timeSlot = entry.time;
    let nb = entry.nb;
    let linktopost = entry.linktopost;

    transformed[companyName] = {
      linktopost: linktopost,
      slots: generateTimeSlots(timeSlot, nb),
    };
  });

  return transformed;
}

function generateTimeSlots(timeSlot, nb) {
  let slots = [];
  let timeSlots = timeSlot.split(",").map((slot) => slot.trim());

  // Génère des plages horaires en fonction des données fournies
  timeSlots.forEach((slot) => {
    let startHour, endHour;
    if (slot === "MATIN") {
      startHour = 9;
      endHour = 12;
    } else if (slot === "MIDI") {
      startHour = 13;
      endHour = 16;
    } else if (slot === "SOIR") {
      startHour = 16;
      endHour = 19;
    }

    // Crée des plages horaires avec des intervalles de 15 minutes
    for (let hour = startHour; hour < endHour; hour++) {
      for (let minute = 0; minute < 60; minute += 15) {
        let endMinute = (minute + 15) % 60;
        let endHour = endMinute === 0 ? hour + 1 : hour;

        let timeLabel = `${hour}h${minute
          .toString()
          .padStart(2, "0")}-${endHour}h${endMinute
          .toString()
          .padStart(2, "0")}`;
        slots.push({
          freespot: nb,
          value: timeLabel,
          logins: ["None", "None", "None"],
        });
      }
    }
  });

  return slots;
}

// function testDoPost() {
//   // Crée un objet JSON simulé
//   var simulatedJson = {
//     "SWISSCOM": {
//       "linktopost": "https://www.swisscom.ch/de/privatkunden.html",
//       "slots": [
//         {
//           "freespot": 3,
//           "value": "9h15-9h30",
//           "logins": ["1", "2", "3"]
//         },
//         {
//           "freespot": 3,
//           "value": "9h30-9h15",
//           "logins": ["4", "5", "6"]
//         },
//         {
//           "freespot": 3,
//           "value": "11h00-12h00",
//           "logins": ["7", "8", "9"]
//         }
//       ]
//     },
//     "MUTUEL": {
//       "linktopost": "https://www.swisscom.ch/de/privatkunden.html",
//       "slots": [
//         {
//           "freespot": 3,
//           "value": "9h15-9h30",
//           "logins": ["1", "2", "3"]
//         },
//         {
//           "freespot": 3,
//           "value": "9h30-9h15",
//           "logins": ["4", "5", "6"]
//         },
//         {
//           "freespot": 3,
//           "value": "11h00-12h00",
//           "logins": ["7", "8", "9"]
//         }
//       ]
//     }
//   };

//   // Simuler un objet événement de requête POST
//   var simulatedPostData = {
//     postData: {
//       type: "application/json",
//       contents: JSON.stringify(simulatedJson)
//     }
//   };

//   // Appeler doPost avec les données simulées
//   doPost(simulatedPostData);
// }
