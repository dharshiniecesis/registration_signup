document.getElementById("registrationForm").addEventListener("submit", function (e) {
  e.preventDefault();

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
    if(result.error){
      alert(result.error);
    } else {
      alert(result.message);
      document.getElementById("registrationForm").reset();
    }
  })
  .catch(err => console.error("Error:", err));
});

