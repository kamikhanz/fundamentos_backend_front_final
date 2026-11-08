const inputBuscar = document.getElementById("buscar");
const selectCategoria = document.getElementById("categoria");

function cargarProductos() {
  const parametros = new URLSearchParams();

  if (inputBuscar.value.trim() != "") {
    parametros.append("buscar", inputBuscar.value.trim());
  }
  if (selectCategoria.value != "") {
    parametros.append("categoria_id", selectCategoria.value);
  }

  peticion("/productos/?" + parametros.toString())
    .then(function (productos) {
      pintarProductos("productos", productos);
      document.getElementById("cantidad").textContent = productos.length + " productos encontrados";
    })
    .catch(mostrarError);
}

document.getElementById("formFiltros").addEventListener("submit", function (event) {
  event.preventDefault();
  cargarProductos();
});

selectCategoria.addEventListener("change", cargarProductos);

// Se cargan las categorias y luego los productos, usando lo que venga en la URL
const datosUrl = new URLSearchParams(window.location.search);
inputBuscar.value = datosUrl.get("buscar") || "";

peticion("/categorias/")
  .then(function (categorias) {
    categorias.forEach(function (categoria) {
      const opcion = crearTexto("option", categoria.nombre);
      opcion.value = categoria.id;
      selectCategoria.appendChild(opcion);
    });

    selectCategoria.value = datosUrl.get("categoria_id") || "";
    cargarProductos();
  })
  .catch(mostrarError);
