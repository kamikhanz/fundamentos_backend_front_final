function crearFila(item) {
  const fila = document.createElement("article");
  fila.className = "fila_carrito";

  const cantidad = document.createElement("input");
  cantidad.type = "number";
  cantidad.min = 1;
  cantidad.value = item.cantidad;
  cantidad.onchange = function () {
    peticion("/carrito/items/" + item.id, "PUT", { cantidad: Number(cantidad.value) })
      .then(pintarCarrito)
      .catch(function (error) {
        mostrarError(error);
        cargarCarrito();
      });
  };

  const eliminar = crearTexto("button", "Eliminar");
  eliminar.onclick = function () {
    peticion("/carrito/items/" + item.id, "DELETE")
      .then(pintarCarrito)
      .catch(mostrarError);
  };

  fila.appendChild(crearImagen(item.producto));
  fila.appendChild(crearEnlace(item.producto.nombre, "producto.html?id=" + item.producto.id));
  fila.appendChild(crearTexto("span", textoPrecio(item.producto.precio) + " c/u"));
  fila.appendChild(cantidad);
  fila.appendChild(crearTexto("strong", "Subtotal: " + textoPrecio(item.subtotal)));
  fila.appendChild(eliminar);

  return fila;
}

function pintarCarrito(carrito) {
  const contenedor = document.getElementById("items");
  contenedor.replaceChildren();

  carrito.items.forEach(function (item) {
    contenedor.appendChild(crearFila(item));
  });

  if (carrito.items.length == 0) {
    contenedor.appendChild(crearTexto("p", "Tu carrito esta vacio"));
  }

  document.getElementById("total").textContent = "Total: " + textoPrecio(carrito.total);
  document.getElementById("confirmar").disabled = carrito.items.length == 0;
}

function cargarCarrito() {
  peticion("/carrito/").then(pintarCarrito).catch(mostrarError);
}

document.getElementById("confirmar").onclick = function () {
  peticion("/pedidos/", "POST")
    .then(function () {
      alert("Compra realizada");
      window.location.href = "pedidos.html";
    })
    .catch(function (error) {
      mostrarError(error);
      cargarCarrito();
    });
};

if (exigirLogin()) {
  cargarCarrito();
}
