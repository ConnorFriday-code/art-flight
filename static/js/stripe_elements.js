var stripePublicKey = document.getElementById('id_stripe_public_key').textContent.trim().slice(1, -1);
var clientSecret = document.getElementById('id_client_secret').textContent.trim().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Roboto", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': { color: '#aab7c4' }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle real-time validation errors
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        errorDiv.innerHTML = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    document.getElementById('submit-button').setAttribute('disabled', true);
    
    // Hide form & show loading
    document.getElementById('payment-form').style.display = 'none';

    var saveInfo = document.getElementById('id-save-info')?.checked || false;
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };

    fetch('/checkout/cache_checkout_data/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(postData)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
    })
    .then(() => {
        return stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: form.full_name.value.trim(),
                    phone: form.phone_number.value.trim(),
                    email: form.email.value.trim(),
                    address: {
                        line1: form.street_address1.value.trim(),
                        line2: form.street_address2.value.trim(),
                        city: form.town_or_city.value.trim(),
                        country: form.country.value.trim(),
                        state: form.county.value.trim(),
                    }
                }
            },
            shipping: {
                name: form.full_name.value.trim(),
                phone: form.phone_number.value.trim(),
                address: {
                    line1: form.street_address1.value.trim(),
                    line2: form.street_address2.value.trim(),
                    city: form.town_or_city.value.trim(),
                    country: form.country.value.trim(),
                    postal_code: form.postcode.value.trim(),
                    state: form.county.value.trim(),
                }
            },
        });
    })
    .then(result => {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            errorDiv.innerHTML = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            document.getElementById('payment-form').style.display = 'block';
            card.update({ 'disabled': false });
            document.getElementById('submit-button').removeAttribute('disabled');
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    })
    .catch(error => {
        var errorDiv = document.getElementById('card-errors');
        errorDiv.innerHTML = `<span>${error.message}</span>`;
        document.getElementById('payment-form').style.display = 'block';
        card.update({ 'disabled': false });
        document.getElementById('submit-button').removeAttribute('disabled');
    });
});