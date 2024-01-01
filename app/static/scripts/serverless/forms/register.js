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
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Custom validation function for motivation character limit
    function validateMotivation(motivation) {
        const maxLength = 250;
        return motivation.length <= maxLength;
    }

    // Event listener for form submission
    $('form').submit(function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Validate each required field
        const firstNameValid = validateField('#first_name', '#first_name_error', value => value.trim() !== '', 'Veuillez entrer votre prénom.');
        const lastNameValid = validateField('#last_name', '#last_name_error', value => value.trim() !== '', 'Veuillez entrer votre nom de famille.');
        const emailValid = validateField('#email', '#email_error', validateEmail, 'Veuillez entrer une adresse email valide.');
        const areasOfInterestValid = validateField('#areas_of_interest', '#areas_of_interest_error', value => value.trim() !== '', 'Veuillez sélectionner une formation.');
        const paymentMethodValid = validateField('#payment_method', '#payment_method_error', value => value.trim() !== '', 'Veuillez sélectionner un mode de paiement.');
        const motivationValid = validateField('#motivation', '#motivation_error', validateMotivation, 'La motivation ne doit pas dépasser 250 caractères.');
        const phoneNumberValid = validateField('#phoneCode', '#phoneCode_error', value => value.trim() !== '', 'Veuillez entrer votre numéro de téléphone.');

        // If any required field is not valid, do not proceed with the AJAX request and disable the submit button
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
        };

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
                // Enable submit button and hide spinner
                submitButton.prop('disabled', false).html('Soumettre <i class="bi bi-send"></i>');

                // Display success message using SweetAlert
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'Votre formulaire a été envoyé avec succès',
                    showCancelButton: true,
                    confirmButtonText: 'Continue',
                    cancelButtonText: 'Cancel',
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Redirect user based on payment method (example: PayPal or Credit Card)
                        if (formData.payment_method === 'PayPal') {
                            window.location.href = 'https://www.paypal.com'; // Replace with actual PayPal URL
                        } else if (formData.payment_method === 'Credit Card') {
                            window.location.href = 'https://www.creditcardpayment.com'; // Replace with actual Credit Card URL
                        }
                        // Add more conditions for other payment methods or actions
                    }
                });
            })
            .catch(error => {
                // Enable submit button and hide spinner
                submitButton.prop('disabled', false).html('Soumettre <i class="bi bi-send"></i>');

                // Display error message using SweetAlert
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Erreur lors de l\'envoi. Veuillez réessayer',
                });
            });
    });

    // Event listeners for real-time validation on input change
    $('#first_name, #last_name, #email, #areas_of_interest, #payment_method, #motivation, #phoneCode').on('input', function () {
        validateField('#' + this.id, '#' + this.id + '_error', this.id === 'email' ? validateEmail : (this.id === 'motivation' ? validateMotivation : value => value.trim() !== ''));
    });
});
