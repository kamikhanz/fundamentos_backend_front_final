peticion("/productos/aleatorios?limite=8")
  .then(function (productos) {
    pintarProductos("aleatorios", productos);
  })
  .catch(mostrarError);

peticion("/productos/destacados")
  .then(function (productos) {
    pintarProductos("destacados", productos);
  })
  .catch(mostrarError);

peticion("/categorias/")
  .then(function (categorias) {
    const lista = document.getElementById("categorias");

    categorias.forEach(function (categoria) {
      const item = document.createElement("li");
      item.appendChild(crearEnlace(categoria.nombre, "catalogo.html?categoria_id=" + categoria.id));
      lista.appendChild(item);
    });
  })
  .catch(mostrarError);
