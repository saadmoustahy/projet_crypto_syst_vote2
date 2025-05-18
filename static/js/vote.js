document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche l'envoi classique du formulaire

    const voterId = document.getElementById('voter-id').value.trim();
    const voterKey = document.getElementById('voter-key').value.trim();

    const idRegex = /^[A-Z][0-9]{4,6}$/;

    if (!idRegex.test(voterId)) {
        alert("L'identifiant doit commencer par une lettre majuscule suivie de 4 à 6 chiffres.");
        return;
    }

    if (voterKey === "") {
        alert("Veuillez entrer votre clé de vote.");
        return;
    }

    // Si tout est correct, continuer l'identification
    document.getElementById('login-area').style.display = 'none';
    document.getElementById('vote-area').style.display = 'block';
});