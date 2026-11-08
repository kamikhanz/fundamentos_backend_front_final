// Funciones que usan todas las paginas
const API_URL = "http://localhost:8000";

function obtenerToken() {
  return localStorage.getItem("token");
}

function cerrarSesion() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

// Si no hay sesion manda al login. Devuelve true si puede seguir.
function exigirLogin() {
  if (!obtenerToken()) {
    window.location.href = "login.html?aviso=1";
    return false;
  }
  return true;
}

function leerRespuesta(response) {
  return response.json().then(function (datos) {
    if (response.ok) {
      return datos;
    }

    if (response.status == 401 && obtenerToken()) {
      localStorage.removeItem("token");
      window.location.href = "login.html?aviso=1";
    }

    let mensaje = "Ocurrio un error";
    if (typeof datos.detail == "string") {
      mensaje = datos.detail;
    } else if (Array.isArray(datos.detail)) {
      mensaje = "Datos no validos: " + datos.detail[0].msg;
    }
    throw new Error(mensaje);
  });
}

// Hace el fetch agregando el token y el JSON cuando hacen falta
function peticion(ruta, metodo, cuerpo) {
  const opciones = { method: metodo || "GET", headers: {} };

  const token = obtenerToken();
  if (token) {
    opciones.headers["Authorization"] = "Bearer " + token;
  }

  if (cuerpo) {
    opciones.headers["Content-Type"] = "application/json";
    opciones.body = JSON.stringify(cuerpo);
  }

  return fetch(API_URL + ruta, opciones).then(leerRespuesta);
}

function mostrarError(error) {
  alert(error.message);
}

function textoDisponibilidad(stock) {
  if (stock > 0) {
    return "Disponible: " + stock;
  }
  return "Agotado";
}

function textoPrecio(valor) {
  return "$" + Number(valor).toFixed(2);
}

function crearTexto(etiqueta, texto) {
  const elemento = document.createElement(etiqueta);
  elemento.textContent = texto;
  return elemento;
}

function crearEnlace(texto, url) {
  const enlace = document.createElement("a");
  enlace.textContent = texto;
  enlace.href = url;
  return enlace;
}

function crearImagen(producto) {
  const imagen = document.createElement("img");
  imagen.alt = producto.nombre;
  if (producto.imagen) {
    imagen.src = producto.imagen;
  }
  return imagen;
}

function crearTarjetaProducto(producto) {
  const tarjeta = document.createElement("article");
  tarjeta.className = "producto";

  let breve = producto.descripcion || "";
  if (breve.length > 70) {
    breve = breve.slice(0, 70) + "...";
  }

  tarjeta.appendChild(crearImagen(producto));
  tarjeta.appendChild(crearTexto("h3", producto.nombre));
  tarjeta.appendChild(crearTexto("p", breve));
  tarjeta.appendChild(crearTexto("p", "Precio: " + textoPrecio(producto.precio)));
  tarjeta.appendChild(crearTexto("p", textoDisponibilidad(producto.stock)));
  tarjeta.appendChild(crearEnlace("Ver detalle", "producto.html?id=" + producto.id));

  return tarjeta;
}

function pintarProductos(idContenedor, productos) {
  const contenedor = document.getElementById(idContenedor);
  contenedor.replaceChildren();

  productos.forEach(function (producto) {
    contenedor.appendChild(crearTarjetaProducto(producto));
  });
}

function agregarAlMenu(lista, elemento) {
  const item = document.createElement("li");
  item.appendChild(elemento);
  lista.appendChild(item);
}

// El menu es igual en todas las paginas
function pintarMenu() {
  const nav = document.createElement("nav");
  nav.appendChild(crearEnlace("Moto Tienda", "index.html"));
  nav.firstChild.className = "marca";

  const lista = document.createElement("ul");
  lista.className = "lista_navegacion";
  nav.appendChild(lista);

  agregarAlMenu(lista, crearEnlace("Inicio", "index.html"));
  agregarAlMenu(lista, crearEnlace("Catalogo", "catalogo.html"));
  agregarAlMenu(lista, crearEnlace("Carrito", "carrito.html"));
  agregarAlMenu(lista, crearEnlace("Mis pedidos", "pedidos.html"));

  document.querySelector("header").appendChild(nav);

  if (!obtenerToken()) {
    agregarAlMenu(lista, crearEnlace("Iniciar sesion", "login.html"));
    agregarAlMenu(lista, crearEnlace("Registrarse", "registro.html"));
    return;
  }

  peticion("/auth/me")
    .then(function (usuario) {
      if (usuario.rol == "admin") {
        agregarAlMenu(lista, crearEnlace("Administrar", "admin.html"));
      }

      agregarAlMenu(lista, crearTexto("span", usuario.nombre + " (" + usuario.email + ")"));

      const botonSalir = crearTexto("button", "Cerrar sesion");
      botonSalir.onclick = cerrarSesion;
      agregarAlMenu(lista, botonSalir);
    })
    .catch(function (error) {
      console.log(error);
    });
}

pintarMenu();
