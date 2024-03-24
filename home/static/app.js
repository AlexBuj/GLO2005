function afficher_info(button) {
    var symbole = button.value;

    // Effectuer une requête AJAX vers la route /info avec le symbole comme paramètre
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/info?symbole=" + encodeURIComponent(symbole));
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Convertir la réponse JSON en objet JavaScript
                var data = JSON.parse(xhr.responseText);

                // Afficher les informations sur l'entreprise
                afficherEntreprise(data.cie);

                // Afficher les données du bilan
                afficherBilan(data.bilan);
            } else {
                console.error("Erreur lors de la requête : " + xhr.status);
            }
        }
    };
    xhr.send();
}

function afficherEntreprise(info) {
    var elementCie = document.getElementById("cie");
    elementCie.innerHTML = ""; // Effacer le contenu précédent

    var HTML_cie = "<ul>";
    HTML_cie += "<li>Nom officiel: " + info[0][0] + "</li>";
    HTML_cie += "<li>Ticker: " + info[0][1] + "</li>";
    HTML_cie += "<li>Secteur d'opération: " + info[0][2] + "</li>";
    HTML_cie += "<li>Description: " + info[0][3] + "</li>";
    HTML_cie += "<li>Siteweb: <a href=\"" + info[0][4] + "\">" + info[0][4] + "</a></li>";
    HTML_cie += "<li>Employés: " + info[0][5] + "</li>";
    HTML_cie += "</ul>";

    elementCie.innerHTML = HTML_cie;
}

function afficherBilan(info) {
    var elementBilan = document.getElementById("bilan");
    elementBilan.innerHTML = ""; // Effacer le contenu précédent

    var HTML_bilan = "<ul>";
    HTML_bilan += "<li>Central Index Key: " + info[0][0] + "</li>";
    HTML_bilan += "<li>Operating Expenses: " + info[0][2] + "</li>";
    HTML_bilan += "<li>R&D Expenses: " + info[0][3] + "</li>";
    HTML_bilan += "<li>Selling: " + info[0][4] + "</li>";
    HTML_bilan += "<li>Revenue: " + info[0][4] + "</li>";
    HTML_bilan += "<li>Gross Profit: " + info[0][6] + "</li>";
    HTML_bilan += "</ul>";

    elementBilan.innerHTML = HTML_bilan;
}


function ajout_fav(button) {
    var symbole = button.value;

    // Effectuer une requête AJAX POST vers la route /insertion avec le symbole comme paramètre
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/insertion");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("symbole=" + encodeURIComponent(symbole));
    //location.reload();
}