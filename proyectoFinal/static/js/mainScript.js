// static/main.js

console.log("Sanity check!");
idCarrito = document.querySelector("#carritoId").value;
productos = document.getElementsByClassName('ulProductosCesta')[0].getElementsByTagName('li');

for (let i = 0; i < productos.length; i++) {
  console.log((productos[i].children[0].children[1].children[0].getElementsByTagName('span')[0].textContent).substring(0, productos[i].children[0].children[1].children[0].getElementsByTagName('span')[0].textContent.length - 1));
}

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#comprarBtn").addEventListener("click", () => {
    form = document.querySelector('.formCheckout');
    // Get Checkout Session ID
    fetch("/crear-checkout-session/"+idCarrito,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});