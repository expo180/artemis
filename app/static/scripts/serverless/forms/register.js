$(document).ready(function() {
    // Function to validate and show error or success messages
    function validateField(fieldId, errorMessageId, validationFunction, errorMessage) {
        const field = $(fieldId);
        const errorContainer = $(errorMessageId);

        // Perform custom validation
        const isValid = validationFunction(field.val());

        // Check if the field is valid
        if (!isValid) {
            // Show error message and apply red styling
            errorContainer.text(errorMessage).css('color', 'red').show();
            field.addClass('is-invalid');
        } else {
            // Clear error message and apply green styling
            errorContainer.text('').hide();
            field.removeClass('is-invalid');
        }

        return isValid;
    }

    // Custom validation function for email format
    function validateEmail(email) {
        let emailInput = $("#email").val();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if(emailRegex.test(email)|| emailInput ===''){
            return true
        }
        else{
            return false
        }
    }

    function validateAreasOfInterest(areasOfInterest) {
        return areasOfInterest.trim() !== '';
    }
    
    function validatePaymentMethod(paymentMethod) {
        return paymentMethod.trim() !== '';
    }

    // Custom validation function for motivation character limit
    function validateMotivation(motivation) {
        const maxLength = 250;
        let motivationInput = $('#motivation').val()
        if(motivation.length <= maxLength || motivationInput ===''){
            return true
        } else{
            return false
        }
    }

    // Event listener for form submission
$('form').submit(function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // Validate each required field
    const firstNameValid = validateField('#first_name', '#first_name_error', value => value.trim() !== '', 'Veuillez entrer votre prénom.');
    const lastNameValid = validateField('#last_name', '#last_name_error', value => value.trim() !== '', 'Veuillez entrer votre nom de famille.');
    const emailValid = validateField('#email', '#email_error', validateEmail, 'Veuillez entrer une adresse email valide.');
    const areasOfInterestValid = validateField('#areas_of_interest', '#areas_of_interest_error', validateAreasOfInterest, 'Veuillez sélectionner une formation.');
    const paymentMethodValid = validateField('#payment_method', '#payment_method_error', validatePaymentMethod, 'Veuillez sélectionner un mode de paiement.');
    const motivationValid = validateField('#motivation', '#motivation_error', validateMotivation, 'La motivation ne doit pas dépasser 250 caractères.');
    const phoneNumberValid = validateField('#phoneCode', '#phoneCode_error', value => value.trim() !== '', 'Veuillez entrer votre numéro de téléphone.');

    // If any required field is not valid, disable the submit button and do not proceed with the AJAX request
    if (!firstNameValid || !lastNameValid || !emailValid || !areasOfInterestValid || !paymentMethodValid || !motivationValid || !phoneNumberValid) {
        $('button[type="submit"]').prop('disabled', true);
        return;
    } else {
        $('button[type="submit"]').prop('disabled', false);
    }

    // Collect form data
    const formData = {
        first_name: $('#first_name').val(),
        last_name: $('#last_name').val(),
        email: $('#email').val(),
        areas_of_interest: $('#areas_of_interest').val(),
        payment_method: $('#payment_method').val(),
        motivation: $('#motivation').val(),
        phone_number: $('#hiddenCountryCode').val() + $('#phoneCode').val(),
        privacy_policy_agreement: $('#privacyPolicyAgreement').prop('checked')
    }

    // Disable submit button and show spinner
    const submitButton = $('button[type="submit"]');
    submitButton.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Envoi...');

    // Perform AJAX request using Fetch API
    fetch("http://127.0.0.1:5000/inscription/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
        .then(response => response.json())
        .then(data => {
            submitButton.prop('disabled', false).html('Soumettre <i class="bi bi-send"></i>');
            Swal.fire({
                icon: 'success',
                title: 'Envoi réussi!',
                text: 'Votre formulaire a été envoyé avec succès. Vous pouvez maintenant continuer en versant les <strong>frais d\'inscription</strong> en utilisant votre <strong>carte de crédit</strong>, <strong>Paypal</strong> ou un autre moyen.',
                showCancelButton: true,
                confirmButtonText: 'Continue',
                cancelButtonText: 'Cancel',
            }).then((result) => {
                if (result.isConfirmed) {
                    if (formData.payment_method === 'Paypal') {
                        window.location.href = 'http://127.0.0.1:5000/paiement/formation/';
                    } else if(formData.payment_method === 'Credit Card'){
                        window.location.href = 'http://127.0.0.1:5000/paiement/formation/';
                    } else{
                        window.location.href = 'http://127.0.0.1:5000/autre/paiement/';
                    }
                }
            });
        })
        .catch(error => {
            submitButton.prop('disabled', false).html('Soumettre <i class="bi bi-send"></i>');
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Erreur lors de l\'envoi. Veuillez réessayer',
            });
        });
});
// Event listener for input on each field
$('#first_name, #last_name, #email, #areas_of_interest, #payment_method, #motivation, #phoneCode').on('input', function () {
    validateField('#' + this.id, '#' + this.id + '_error', this.id === 'email' ? validateEmail : (this.id === 'motivation' ? validateMotivation : value => value.trim() !== ''));
});

});
