/**
 * Script pour la page de connexion d'administration
 */
document.addEventListener('DOMContentLoaded', function() {
    // Sélectionner le formulaire de connexion
    const loginForm = document.querySelector('form[action="/admin-login"]');
   
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Validation côté client basique
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
           
            if (!username || !password) {
                e.preventDefault(); // Empêche la soumission du formulaire
                alert('Veuillez remplir tous les champs');
                return false;
            }
           
            // Si tout est correct, le formulaire sera soumis normalement
        });
    }
   
    // Afficher les messages flash
    const flashMessages = document.querySelectorAll('.flash-message');
   
    flashMessages.forEach(function(message) {
        // Faire disparaître les messages après 5 secondes
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 500);
        }, 5000);
    });
});