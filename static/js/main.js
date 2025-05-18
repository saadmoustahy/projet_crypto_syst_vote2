document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded and ready');
    
    // Handle form submissions and add CSRF token if needed
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log('Form submission attempt:', form.action);
            
            // Make sure CSRF token is included
            let csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            
            if (csrfToken) {
                // Check if the form already has a CSRF token input
                let existingToken = form.querySelector('input[name="csrf_token"]');
                
                if (!existingToken) {
                    // Add the token if it doesn't exist
                    let tokenInput = document.createElement('input');
                    tokenInput.setAttribute('type', 'hidden');
                    tokenInput.setAttribute('name', 'csrf_token');
                    tokenInput.setAttribute('value', csrfToken);
                    form.appendChild(tokenInput);
                    console.log('Added CSRF token to form');
                } else {
                    console.log('Form already has CSRF token');
                }
            } else {
                console.log('No CSRF token found in meta tag');
            }
        });
    });
    
    // Animation for flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        message.style.opacity = '0';
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease-in-out';
            message.style.opacity = '1';
        }, 100);
        
        // Auto-hide success messages after 5 seconds
        if (message.classList.contains('alert-success')) {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500);
            }, 5000);
        }
    });
    
    // Enhanced form validation
    const identificationForm = document.getElementById('identification-form');
    if (identificationForm) {
        identificationForm.addEventListener('submit', function(event) {
            const voterIdField = document.getElementById('voter-id');
            const emailField = document.getElementById('voter-email');
            
            if (voterIdField && voterIdField.value.trim() === '') {
                event.preventDefault();
                showValidationError(voterIdField, 'Veuillez entrer votre identifiant');
            }
            
            if (emailField) {
                const emailValue = emailField.value.trim();
                if (emailValue === '') {
                    event.preventDefault();
                    showValidationError(emailField, 'Veuillez entrer votre adresse email');
                } else if (!isValidEmail(emailValue)) {
                    event.preventDefault();
                    showValidationError(emailField, 'Veuillez entrer une adresse email valide');
                }
            }
        });
    }
    
    // Enhanced verification code validation
    const verificationForm = document.getElementById('verification-form');
    if (verificationForm) {
        verificationForm.addEventListener('submit', function(event) {
            const codeField = document.getElementById('verification_code');
            
            if (codeField && codeField.value.trim() === '') {
                event.preventDefault();
                showValidationError(codeField, 'Veuillez entrer le code de vérification');
            } else if (codeField && codeField.value.trim().length !== 6) {
                event.preventDefault();
                showValidationError(codeField, 'Le code doit contenir 6 caractères');
            }
        });
    }
});

// Helper function to validate email format
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Helper function to show validation errors
function showValidationError(inputElement, message) {
    // Remove any existing error messages
    const existingError = inputElement.parentNode.querySelector('.validation-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Create error message
    const errorElement = document.createElement('div');
    errorElement.className = 'validation-error';
    errorElement.style.color = '#e74c3c';
    errorElement.style.fontSize = '0.8rem';
    errorElement.style.marginTop = '5px';
    errorElement.textContent = message;
    
    // Add error styling to input
    inputElement.style.borderColor = '#e74c3c';
    
    // Insert error message after input
    inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
    
    // Focus on input
    inputElement.focus();
    
    // Remove error when input changes
    inputElement.addEventListener('input', function() {
        inputElement.style.borderColor = '';
        if (errorElement.parentNode) {
            errorElement.parentNode.removeChild(errorElement);
        }
    }, { once: true });
}