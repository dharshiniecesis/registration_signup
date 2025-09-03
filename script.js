document
  .getElementById("registrationForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    // Get form values
    let firstName = document.getElementById("firstName").value.trim();
    let lastName = document.getElementById("lastName").value.trim();
    let dob = document.getElementById("dob").value.trim();
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();
    let confirmPassword = document
      .getElementById("confirmPassword")
      .value.trim();

    // Error placeholders
    let errors = {
      firstName: "",
      lastName: "",
      dob: "",
      username: "",
      password: "",
      confirmPassword: "",
    };

    // Validation
    if (!firstName) errors.firstName = "First Name is required";
    if (!lastName) errors.lastName = "Last Name is required";
    if (!dob) errors.dob = "Date of Birth is required";
    if (!username) errors.username = "Username is required";
    if (!password) errors.password = "Password is required";
    if (!confirmPassword)
      errors.confirmPassword = "Confirm Password is required";
    if (password && confirmPassword && password !== confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }

    // Check if username already exists in localStorage
    let users = JSON.parse(localStorage.getItem("users")) || [];
    let userExists = users.some((user) => user.username === username);
    if (userExists) {
      errors.username = "Username already taken";
    }

    // Display Errors
    document.getElementById("firstNameError").innerText = errors.firstName;
    document.getElementById("lastNameError").innerText = errors.lastName;
    document.getElementById("dobError").innerText = errors.dob;
    document.getElementById("usernameError").innerText = errors.username;
    document.getElementById("passwordError").innerText = errors.password;
    document.getElementById("confirmPasswordError").innerText =
      errors.confirmPassword;

    // If no errors, save data
    if (
      !errors.firstName &&
      !errors.lastName &&
      !errors.dob &&
      !errors.username &&
      !errors.password &&
      !errors.confirmPassword
    ) {
      let newUser = { firstName, lastName, dob, username, password };
      users.push(newUser);
      localStorage.setItem("users", JSON.stringify(users));

      document.getElementById("successMsg").classList.remove("d-none");
      document.getElementById("successMsg").innerText =
        "Registration Successful!";
    }
    // Reset form
    document.getElementById("registrationForm").reset();
  });
