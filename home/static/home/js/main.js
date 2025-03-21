// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function () {
const alertBox = document.getElementById("alertBox");
if (alertBox) {
    // Set a timeout to hide the alert after 10 seconds
    setTimeout(() => {
    alertBox.classList.add("hidden");
    }, 5000); // 5000 milliseconds = 5 seconds
}

})

// document.getElementById('payButton').addEventListener('click', function (event) {
//     const button = event.target;

//     // Change text and disable button
//     button.innerHTML = `<svg class="animate-spin h-5 w-5 mr-3 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
//         <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
//         <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l-3 3 3 3v4a8 8 0 01-8-8z"></path>
//     </svg> Initializing Payment...`;
//     button.disabled = true;
//     button.classList.add('opacity-50', 'cursor-not-allowed');

//     // Simulate a delay for example purposes (e.g., to navigate or complete a process)
//     setTimeout(() => {
//         window.location.href = button.getAttribute('checkout');
//     }, 100); // Replace with your payment process trigger
// });

