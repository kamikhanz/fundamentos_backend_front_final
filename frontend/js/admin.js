const ESTADOS = ["pendiente", "procesando", "enviado", "entregado"];

function celda(fila, contenido) {
  const td = document.createElement("td");
  if (typeof contenido == "object") {
    td.appendChild(contenido);
  } else {
    td.textContent = contenido;
  }
  fila.appendChild(td);
  return td;
}

function eliminar(ruta, recargar) {
  if (!confirm("Desea eliminar este registro?")) {
    return;
  }

  peticion(ruta, "DELETE").then(recargar).catch(mostrarError);
}

// ---------- CATEGORIAS ----------
function cargarCategorias() {
  peticion("/categorias/")
    .then(function (categorias) {
      const tabla = document.getElementById("tablaCategorias");
      const select = document.getElementById("productoCategoria");
      tabla.replaceChildren();
      select.replaceChildren();

      categorias.forEach(function (categoria) {
        const fila = document.createElement("tr");
        celda(fila, categoria.id);
        celda(fila, categoria.nombre);
        celda(fila, categoria.descripcion || "");

        const editar = crearTexto("button", "Editar");
        editar.onclick = function () {
          document.getElementById("categoriaId").value = categoria.id;
          document.getElementById("categoriaNombre").value = categoria.nombre;
          document.getElementById("categoriaDescripcion").value = categoria.descripcion || "";
        };

        const borrar = crearTexto("button", "Eliminar");
        borrar.onclick = function () {
          eliminar("/categorias/" + categoria.id, cargarCategorias);
        };

        celda(fila, editar).appendChild(borrar);
        tabla.appendChild(fila);

        const opcion = crearTexto("option", categoria.nombre);
        opcion.value = categoria.id;
        select.appendChild(opcion);
      });
    })
    .catch(mostrarError);
}

document.getElementById("formCategoria").addEventListener("submit", function (event) {
  event.preventDefault();

  const id = document.getElementById("categoriaId").value;
  const categoria = {
    nombre: document.getElementById("categoriaNombre").value,
    descripcion: document.getElementById("categoriaDescripcion").value,
  };

  let respuesta;
  if (id == "") {
    respuesta = peticion("/categorias/", "POST", categoria);
  } else {
    respuesta = peticion("/categorias/" + id, "PUT", categoria);
  }

  respuesta
    .then(function () {
      alert("Categoria guardada");
      limpiarFormulario("formCategoria", "categoriaId");
      cargarCategorias();
      cargarProductos();
    })
    .catch(mostrarError);
});

// ---------- PRODUCTOS ----------
function llenarFormularioProducto(producto) {
  document.getElementById("productoId").value = producto.id;
  document.getElementById("productoNombre").value = producto.nombre;
  document.getElementById("productoCodigo").value = producto.codigo || "";
  document.getElementById("productoDescripcion").value = producto.descripcion || "";
  document.getElementById("productoPrecio").value = producto.precio;
  document.getElementById("productoStock").value = producto.stock;
  document.getElementById("productoImagen").value = producto.imagen || "";
  document.getElementById("productoCategoria").value = producto.categoria_id;
  document.getElementById("productoDestacado").checked = producto.destacado;
  document.getElementById("formProducto").scrollIntoView();
}

function cargarProductos() {
  peticion("/productos/")
    .then(function (productos) {
      const tabla = document.getElementById("tablaProductos");
      tabla.replaceChildren();

      productos.forEach(function (producto) {
        const fila = document.createElement("tr");
        celda(fila, producto.id);
        celda(fila, producto.nombre);
        celda(fila, producto.categoria.nombre);
        celda(fila, textoPrecio(producto.precio));
        celda(fila, producto.stock);

        const editar = crearTexto("button", "Editar");
        editar.onclick = function () {
          llenarFormularioProducto(producto);
        };

        const borrar = crearTexto("button", "Eliminar");
        borrar.onclick = function () {
          eliminar("/productos/" + producto.id, cargarProductos);
        };

        celda(fila, editar).appendChild(borrar);
        tabla.appendChild(fila);
      });
    })
    .catch(mostrarError);
}

document.getElementById("formProducto").addEventListener("submit", function (event) {
  event.preventDefault();

  const id = document.getElementById("productoId").value;
  const producto = {
    nombre: document.getElementById("productoNombre").value,
    codigo: document.getElementById("productoCodigo").value || null,
    descripcion: document.getElementById("productoDescripcion").value,
    precio: Number(document.getElementById("productoPrecio").value),
    stock: Number(document.getElementById("productoStock").value),
    imagen: document.getElementById("productoImagen").value || null,
    destacado: document.getElementById("productoDestacado").checked,
    categoria_id: Number(document.getElementById("productoCategoria").value),
  };

  let respuesta;
  if (id == "") {
    respuesta = peticion("/productos/", "POST", producto);
  } else {
    respuesta = peticion("/productos/" + id, "PUT", producto);
  }

  respuesta
    .then(function () {
      alert("Producto guardado");
      limpiarFormulario("formProducto", "productoId");
      cargarProductos();
    })
    .catch(mostrarError);
});

// El boton Limpiar no borra los campos ocultos, por eso se hace aparte
function limpiarFormulario(idFormulario, idOculto) {
  document.getElementById(idFormulario).reset();
  document.getElementById(idOculto).value = "";
}

document.getElementById("formCategoria").addEventListener("reset", function () {
  document.getElementById("categoriaId").value = "";
});

document.getElementById("formProducto").addEventListener("reset", function () {
  document.getElementById("productoId").value = "";
});

// ---------- PEDIDOS ----------
function crearSelectEstado(pedido) {
  const select = document.createElement("select");

  ESTADOS.forEach(function (estado) {
    const opcion = crearTexto("option", estado);
    opcion.value = estado;
    select.appendChild(opcion);
  });

  select.value = pedido.estado;
  select.onchange = function () {
    peticion("/pedidos/" + pedido.id + "/estado", "PUT", { estado: select.value })
      .then(function () {
        alert("Estado actualizado");
      })
      .catch(function (error) {
        mostrarError(error);
        cargarPedidos();
      });
  };

  return select;
}

function cargarPedidos() {
  peticion("/pedidos/admin/todos")
    .then(function (pedidos) {
      const tabla = document.getElementById("tablaPedidos");
      tabla.replaceChildren();

      pedidos.forEach(function (pedido) {
        const productos = pedido.items.map(function (item) {
          return item.cantidad + " x " + item.producto.nombre;
        });

        const fila = document.createElement("tr");
        celda(fila, pedido.id);
        celda(fila, pedido.usuario.email);
        celda(fila, new Date(pedido.fecha).toLocaleString());
        celda(fila, textoPrecio(pedido.total));
        celda(fila, productos.join(", "));
        celda(fila, crearSelectEstado(pedido));
        tabla.appendChild(fila);
      });
    })
    .catch(mostrarError);
}

// Solo el administrador ve el panel
if (exigirLogin()) {
  peticion("/auth/me")
    .then(function (usuario) {
      if (usuario.rol != "admin") {
        const aviso = document.getElementById("aviso");
        aviso.className = "aviso";
        aviso.textContent = "No tienes permiso para ver esta pagina. Solo el administrador puede entrar.";
        return;
      }

      document.getElementById("panel").hidden = false;
      cargarCategorias();
      cargarProductos();
      cargarPedidos();
    })
    .catch(mostrarError);
}
