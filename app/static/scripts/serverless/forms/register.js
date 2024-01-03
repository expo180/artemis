$(document).ready(function () {
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
        return emailRegex.test(email) || email === '';
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
        return motivation.length <= maxLength || motivation === '';
    }

    // Event listener for input on each field
    $('#first_name, #last_name, #email, #areas_of_interest, #payment_method, #motivation, #phoneCode').on('input', function () {
        const isValid = validateField('#' + this.id, '#' + this.id + '_error', this.id === 'email' ? validateEmail : (this.id === 'motivation' ? validateMotivation : value => value.trim() !== ''));

        // Enable or disable the submit button based on overall form validity
        const isFormValid = validateForm();
        $('button[type="submit"]').prop('disabled', !isFormValid);
    });

    // Function to validate the entire form
    function validateForm() {
        const firstNameValid = validateField('#first_name', '#first_name_error', value => value.trim() !== '', 'Veuillez entrer votre prénom.');
        const lastNameValid = validateField('#last_name', '#last_name_error', value => value.trim() !== '', 'Veuillez entrer votre nom de famille.');
        const emailValid = validateField('#email', '#email_error', validateEmail, 'Veuillez entrer une adresse email valide.');
        const areasOfInterestValid = validateField('#areas_of_interest', '#areas_of_interest_error', validateAreasOfInterest, 'Veuillez sélectionner une formation.');
        const paymentMethodValid = validateField('#payment_method', '#payment_method_error', validatePaymentMethod, 'Veuillez sélectionner un mode de paiement.');
        const motivationValid = validateField('#motivation', '#motivation_error', validateMotivation, 'La motivation ne doit pas dépasser 250 caractères.');
        const phoneNumberValid = validateField('#phoneCode', '#phoneCode_error', value => value.trim() !== '', 'Veuillez entrer votre numéro de téléphone.');

        return firstNameValid && lastNameValid && emailValid && areasOfInterestValid && paymentMethodValid && motivationValid && phoneNumberValid;
    }

    // Event listener for form submission
    $('form').submit(function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Validate the entire form
        const isFormValid = validateForm();

        // If the entire form is valid, proceed with AJAX request
        if (isFormValid) {
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
            fetch("https://bit-t2kb.onrender.com/inscription/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    submitButton.prop('disabled', false).html('Soumettre <i class="bi bi-send"></i>');

                    // Store user information in local storage
                    localStorage.setItem('user_info', JSON.stringify(formData));

                    Swal.fire({
                        icon: 'success',
                        title: 'Envoi réussi!',
                        text: 'Votre formulaire a été envoyé avec succès. Vous pouvez maintenant continuer en versant les frais d\'inscription en utilisant votre carte de crédit, Paypal ou un autre moyen.',
                        showCancelButton: true,
                        confirmButtonText: 'Continue',
                        cancelButtonText: 'Retour',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            if (formData.payment_method === 'Paypal') {
                                window.location.href = 'https://ekki.onrender.com';
                            } else if (formData.payment_method === 'Credit Card') {
                                window.location.href = 'https://ekki.onrender.com';
                            } else {
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
        } else {
            // Show an error message or handle invalid form submission as needed
        }
    });
});
