function afficher_info(button) {
    // Exécuter une requête AJAX vers le serveur Flask
    var symbole = button.value;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/info?symbole=" + encodeURIComponent(symbole));
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Convertir la réponse JSON en objet JavaScript
                var resultat = JSON.parse(xhr.responseText)[0];

                // Récupérer l'élément où afficher le résultat
                var elementCie = document.getElementById("cie");

                // Effacer le contenu précédent de l'élément
                elementCie.innerHTML = "";

                // Créer une liste HTML pour afficher les éléments
                var contenuHTML = "<ul>";
                contenuHTML += "<li>Nom officiel: " + resultat[0] + "</li>";
                contenuHTML += "<li id=\"ticker\">Ticker: " + resultat[1] + "</li>";
                contenuHTML += "<li id=\"secteur\">Secteur d'opération: " + resultat[2] + "</li>";
                contenuHTML += "<li id=\"description\">Siteweb: " + resultat[4] + "</li>";
                contenuHTML += "<li id=\"revenueTTM\">Employés: " + resultat[5] + "</li>";
                contenuHTML += "<li id=\"profitTTM\">Description: " + resultat[3] + "</li>";
                contenuHTML += "</ul>";

                // Mettre à jour le contenu de l'élément avec l'ID 'cie'
                elementCie.innerHTML = contenuHTML;
            } else {
                console.error("Erreur lors de la requête : " + xhr.status);
            }
        }
    };
    xhr.send();
}