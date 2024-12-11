/*=== SHOW MENU ===*/
const navMenu = document.getElementById("nav-menu"),
  navToggle = document.getElementById("nav-toggle"),
  navClose = document.getElementById("nav-close");

/*=== MENU SHOW ===*/
/* Validate if constant exists */
if (navToggle) {
  navToggle.addEventListener("click", () => {
    navMenu.classList.add("show-menu");
  });
}

/*=== MENU HIDDEN ===*/
/* Validate if constant exists */
if (navClose) {
  navClose.addEventListener("click", () => {
    navMenu.classList.remove("show-menu");
  });
}

/*=== REMOVE MENU MOBILE ===*/
const navLink = document.querySelectorAll(".nav__link");

const linkAction = () => {
  const navMenu = document.getElementById("nav-menu");
  // When we click each nav__link, we remove the show-menu class
  navMenu.classList.remove("show-menu");
};

navLink.forEach((n) => n.addEventListener("click", linkAction));

/*=== SHOW SCROLL UP ===*/
const scrollUp = () => {
  const scrollUp = document.getElementById('scroll-up')
  this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
                      : scrollUp.classList.remove('show-scroll')
}

window.addEventListener('scroll', scrollUp)



/*=== FLASH MESSAGES ===*/
document.addEventListener("DOMContentLoaded", function () {
  // Seleccionamos todos los mensajes flash
  const flashMessages = document.querySelectorAll(".flash-message");

  flashMessages.forEach((message) => {
    // Inicia la animación de salida después de 5 segundos
    setTimeout(() => {
      message.style.animation = "slideOut 0.5s forwards";
    }, 5000);

    // Agrega un listener para el evento de fin de animación
    message.addEventListener("animationend", (event) => {
      if (event.animationName === "slideOut") {
        message.remove(); // Elimina el mensaje del DOM
      }
    });

    // Funcionalidad del botón de cierre
    const closeButton = message.querySelector(".flash-message__close");
    if (closeButton) {
      closeButton.addEventListener("click", () => {
        message.style.animation = "slideOut 0.5s forwards";
      });
    }
  });
});


// alerta para avisar que si se elimina el plato se eliminaran todas las ordenes
// que estén asociadas a el.
// Selecciona todos los formularios que tienen el botón de eliminación
// Selecciona solo los formularios de eliminación de platos
const deleteDishForms = document.querySelectorAll('.delete-dish-form');

deleteDishForms.forEach(form => {
  form.addEventListener('submit', function (event) {
    // Muestra la alerta de confirmación
    const confirmDelete = confirm(
      "¿Estás seguro de que deseas eliminar este plato? Esto también eliminará todas las órdenes relacionadas con él."
    );

    if (!confirmDelete) {
      // Si el usuario cancela, detén el envío del formulario
      event.preventDefault();
    } else {
      // Opcional: puedes realizar acciones antes de que se envíe el formulario
      console.log('Formulario enviado para eliminar el plato con ID:', this.querySelector('input[name="dish_id"]').value);
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".nav__link");
  const currentPath = window.location.pathname;

  links.forEach(link => {
    const linkPath = new URL(link.href).pathname; // Obtiene solo el pathname del href
    if (linkPath === currentPath) {
      link.classList.add("active-link");
    } else {
      link.classList.remove("active-link"); // Asegura que otros enlaces no tengan la clase activa
    }
  });
});

