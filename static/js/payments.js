var stripe = Stripe(
  "pk_test_51Qk7KYEKN3gLB4ZgBYRHxcUyXot1O0IHNUKuVXBvfc5MvTZX8r7tnRR0bapoqV7pslajiqhmfBJN2aLhRTwAhhFF00A3jQgX3G"
);

var csrfToken = document.querySelector(
  'input[name="csrfmiddlewaretoken"]'
).value; // Get the CSRF token from the hidden input

document
  .getElementById("checkout-button")
  .addEventListener("click", async function () {
    if (!isAuthenticated) {
      // Redirect to the login page, preserving the current URL
      const currentUrl = window.location.pathname + window.location.search; // Get the current path and query params
      window.location.href = `/login/?next=${encodeURIComponent(currentUrl)}`;
      return;
    }

    // User is authenticated, proceed with creating the checkout session
    const response = await fetch(`/create-checkout-session/${courseId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });

    if (response.ok) {
      const data = await response.json();
      stripe.redirectToCheckout({ sessionId: data.id });
    } else {
      alert("Something went wrong. Please try again.");
    }
  });
