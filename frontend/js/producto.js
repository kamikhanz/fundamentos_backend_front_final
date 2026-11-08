const idProducto = new URLSearchParams(window.location.search).get("id");

function agregarAlCarrito(producto, cantidad) {
  if (!obtenerToken()) {
    window.location.href = "login.html?aviso=1";
    return;
  }

  if (!Number.isInteger(cantidad) || cantidad < 1) {
    alert("Ingrese una cantidad valida");
    return;
  }

  if (cantidad > producto.stock) {
    alert("Solo hay " + producto.stock + " disponibles");
    return;
  }

  peticion("/carrito/items", "POST", { producto_id: producto.id, cantidad: cantidad })
    .then(function () {
      alert("Producto agregado al carrito");
    })
    .catch(mostrarError);
}

function pintarDetalle(producto) {
  const contenedor = document.getElementById("detalle");
  contenedor.replaceChildren();

  const informacion = document.createElement("div");
  informacion.appendChild(crearTexto("h1", producto.nombre));
  informacion.appendChild(crearTexto("p", "Categoria: " + producto.categoria.nombre));
  if (producto.codigo) {
    informacion.appendChild(crearTexto("p", "Codigo: " + producto.codigo));
  }
  informacion.appendChild(crearTexto("p", producto.descripcion || ""));
  informacion.appendChild(crearTexto("h2", textoPrecio(producto.precio)));
  informacion.appendChild(crearTexto("p", textoDisponibilidad(producto.stock)));

  const cantidad = document.createElement("input");
  cantidad.type = "number";
  cantidad.id = "cantidad";
  cantidad.min = 1;
  cantidad.max = producto.stock;
  cantidad.value = 1;

  const boton = crearTexto("button", "Agregar al carrito");
  boton.id = "agregar";
  boton.onclick = function () {
    agregarAlCarrito(producto, Number(cantidad.value));
  };

  if (producto.stock == 0) {
    cantidad.disabled = true;
    boton.disabled = true;
  }

  informacion.appendChild(cantidad);
  informacion.appendChild(document.createElement("br"));
  informacion.appendChild(boton);

  contenedor.appendChild(crearImagen(producto));
  contenedor.appendChild(informacion);
}

if (idProducto == null) {
  window.location.href = "catalogo.html";
} else {
  peticion("/productos/" + idProducto)
    .then(pintarDetalle)
    .catch(mostrarError);
}
