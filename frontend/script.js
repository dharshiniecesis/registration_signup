document.getElementById("registrationForm").addEventListener("submit", function (e) {
  e.preventDefault();

  // Clear old errors
  document.querySelectorAll("small.text-danger").forEach(el => el.textContent = "");

  let firstName = document.getElementById("firstName").value.trim();
  let lastName = document.getElementById("lastName").value.trim();
  let dob = document.getElementById("dob").value.trim();
  let username = document.getElementById("username").value.trim();
  let email = document.getElementById("email").value.trim();
  let mobile = document.getElementById("mobile").value.trim();
  let password = document.getElementById("password").value.trim();
  let confirmPassword = document.getElementById("confirmPassword").value.trim();

  const data = { firstName, lastName, dob, username, email, mobile, password, confirmPassword };

  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(result => {
    if(result.errors){ 
      // Show errors under inputs
      Object.keys(result.errors).forEach(key => {
        document.getElementById(key + "Error").textContent = result.errors[key];
      });
    } else {
      // Redirect to users.html after success
      window.location.href = "/users";
    }
  })
  .catch(err => console.error("Error:", err));
});
