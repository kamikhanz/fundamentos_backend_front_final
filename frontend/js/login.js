if (new URLSearchParams(window.location.search).get("aviso")) {
  const aviso = document.getElementById("aviso");
  aviso.className = "aviso";
  aviso.textContent = "Debes iniciar sesion para continuar";
}

document.getElementById("formLogin").addEventListener("submit", function (event) {
  event.preventDefault();

  localStorage.removeItem("token");

  // El login de FastAPI recibe un formulario, no JSON. El correo va en username.
  const datos = new URLSearchParams();
  datos.append("username", document.getElementById("email").value);
  datos.append("password", document.getElementById("password").value);

  fetch(API_URL + "/auth/login", { method: "POST", body: datos })
    .then(leerRespuesta)
    .then(function (respuesta) {
      localStorage.setItem("token", respuesta.access_token);
      window.location.href = "index.html";
    })
    .catch(mostrarError);
});
