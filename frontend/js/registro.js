document.getElementById("formRegistro").addEventListener("submit", function (event) {
  event.preventDefault();

  const usuario = {
    nombre: document.getElementById("nombre").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  peticion("/auth/register", "POST", usuario)
    .then(function () {
      alert("Cuenta creada, ahora inicia sesion");
      window.location.href = "login.html";
    })
    .catch(mostrarError);
});
