// Ce script servait à avoir une base de données pour visualiser dans un google sheet
// les données des élevents inscrit sur discord (login, cv ,linkpost, slot reservé, ...)
// CE SCRIPT A ÉTÉ ABANDONNÉ PAR LA SUITE

function testDoPost() {
  console.log("Test Function is running");
  // Créer un JSON simulé pour le test
  var simulatedJson = {
    jdoe: {
      Name: "John",
      Surname: "Doe",
      Linkedin: "https://www.linkedin.com/in/johndoe",
      Cv: "https://example.com/cv/johndoe",
      Slot1: "selected",
      Slot5: "selected",
      Slot6: "selected",
      // Ajoutez d'autres slots si nécessaire
    },
  };

  // Simuler un objet e comme il serait reçu dans doPost
  var simulatedEvent = {
    postData: {
      type: "application/json",
      contents: JSON.stringify(simulatedJson),
    },
  };

  console.log("Simulated Event:", simulatedEvent);

  // Appeler doPost avec l'objet simulé
  doPost(simulatedEvent);
}

function doPost(e) {
  console.log("Received Event:", e);

  var jsonData = JSON.parse(e.postData.contents);

  // Vérifier si la commande existe et l'éxécute
  if (isValideJson(jsonData)) {
    console.log("valid format");
    updateUser(jsonData);
    return ContentService.createTextOutput(
      JSON.stringify({ result: "success" })
    ).setMimeType(ContentService.MimeType.JSON);
  }
  console.log("invalid format");
  return ContentService.createTextOutput(
    JSON.stringify({ result: "command not found" })
  ).setMimeType(ContentService.MimeType.JSON);
}

function isValideJson(jsonData) {
  // Obtenir le nom de la clé principale (comme 'jdoe')
  var dynamicKeyName = Object.keys(jsonData)[0];
  var user = jsonData[dynamicKeyName];

  // Liste des clés requises
  var requiredKeys = ["Name", "Surname", "Linkedin", "Cv"];

  // Vérifie si toutes les clés requises existent et ont une valeur non vide
  for (var i = 0; i < requiredKeys.length; i++) {
    var key = requiredKeys[i];
    if (!user[key] || user[key].trim() === "") {
      console.log("Required key missing or empty:", key);
      return false;
    }
  }

  // Validation supplémentaire pour les URL LinkedIn et CV
  // if (!isValidUrl(user['Linkdin']) || !isValidUrl(user['Cv'])) {
  //   console.log("Invalid URL format");
  //   return false;
  // }

  // Vérifie si les slots sont présents et ont un format correct
  var slotPattern = /^Slot\d+\(\d+h\d+\)$/;
  for (var key in user) {
    if (slotPattern.test(key) && user[key].trim() === "") {
      console.log("Invalid slot format or empty:", key);
      return false;
    }
  }

  return true;
}

function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

function updateUser(userData) {
  var sheet = SpreadsheetApp.openById(
    "1Y191yEJ6vzsKIQZfbtCiqdBBLmWL58rKe8sKUIu1rvg"
  ).getSheetByName("db");
  var dataRange = sheet.getDataRange();
  var values = dataRange.getValues();

  var dynamicKeyName = Object.keys(userData)[0];
  var user = userData[dynamicKeyName];

  var rowIndex = values.findIndex((row) => row[0] === dynamicKeyName);

  if (rowIndex !== -1) {
    console.log("Utilisateur trouvé");
    var columns = dataRange.offset(0, 0, 1).getValues()[0];
    columns.forEach(function (column, colIndex) {
      var value = colIndex === 0 ? dynamicKeyName : user[column] || "";
      sheet.getRange(rowIndex + 1, colIndex + 1).setValue(value);
    });
  } else {
    console.log("Ajout d'un nouvel utilisateur");
    var newUserRow = [dynamicKeyName];
    var headers = values[0];
    headers.slice(1).forEach(function (header) {
      newUserRow.push(user[header] || "");
    });
    sheet.appendRow(newUserRow);
  }
}
