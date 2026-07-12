fetch("menu.json")
  .then(response => response.json())
  .then(data => {
    const precio = document.getElementById("precio");
    const primero = document.getElementById("primerPlato");
    const segundo = document.getElementById("segundoPlato");
    const bebida = document.getElementById("bebida");
    const postre = document.getElementById("postre");

    if (precio) precio.textContent = data.menuDelDia.precio;
    if (primero) primero.textContent = data.menuDelDia.primerPlato;
    if (segundo) segundo.textContent = data.menuDelDia.segundoPlato;
    if (bebida) bebida.textContent = data.menuDelDia.bebida;
    if (postre) postre.textContent = data.menuDelDia.postre;
  })
  .catch(error => console.log("Ошибка загрузки меню:", error));
