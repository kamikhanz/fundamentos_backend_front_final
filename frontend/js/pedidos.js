function pintarDetallePedido(pedido, contenedor) {
  contenedor.replaceChildren();

  const lista = document.createElement("ul");
  pedido.items.forEach(function (item) {
    const subtotal = item.precio_unitario * item.cantidad;
    lista.appendChild(
      crearTexto(
        "li",
        item.cantidad + " x " + item.producto.nombre + " a " + textoPrecio(item.precio_unitario) + " = " + textoPrecio(subtotal)
      )
    );
  });

  contenedor.appendChild(lista);
}

function crearTarjetaPedido(pedido) {
  const tarjeta = document.createElement("article");
  tarjeta.className = "pedido";

  const detalle = document.createElement("div");

  const boton = crearTexto("button", "Ver detalle");
  boton.onclick = function () {
    peticion("/pedidos/" + pedido.id)
      .then(function (datos) {
        pintarDetallePedido(datos, detalle);
      })
      .catch(mostrarError);
  };

  tarjeta.appendChild(crearTexto("h3", "Pedido #" + pedido.id));
  tarjeta.appendChild(crearTexto("p", "Fecha: " + new Date(pedido.fecha).toLocaleString()));
  tarjeta.appendChild(crearTexto("p", "Estado: " + pedido.estado));
  tarjeta.appendChild(crearTexto("p", "Total: " + textoPrecio(pedido.total)));
  tarjeta.appendChild(boton);
  tarjeta.appendChild(detalle);

  return tarjeta;
}

if (exigirLogin()) {
  peticion("/pedidos/mis-pedidos")
    .then(function (pedidos) {
      const contenedor = document.getElementById("pedidos");

      pedidos.forEach(function (pedido) {
        contenedor.appendChild(crearTarjetaPedido(pedido));
      });

      if (pedidos.length == 0) {
        contenedor.appendChild(crearTexto("p", "Todavia no tienes pedidos"));
      }
    })
    .catch(mostrarError);
}
