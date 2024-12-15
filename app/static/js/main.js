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


// Función genérica para manejar el envío de formularios con confirmación
function addConfirmationHandler(formSelector, confirmMessage) {
  const forms = document.querySelectorAll(formSelector);

  forms.forEach(form => {
    form.addEventListener('submit', function (event) {
      const confirmDelete = confirm(confirmMessage);

      if (!confirmDelete) {
        event.preventDefault(); // Detén el envío si se cancela la confirmación
      } else {
        // Acciones adicionales antes de enviar el formulario
        console.log('hola mundo')
      }
    });
  });
}

// Aplicar la función genérica a distintos formularios con diferentes mensajes
// alerta para avisar que si se elimina el plato se eliminaran todas las ordenes
// que estén asociadas a el.
addConfirmationHandler(
  '.delete-user-form',
  '¿Estás seguro de que deseas eliminar este usuario? Esto también eliminará todas las órdenes y platos relacionados con él.'
);
addConfirmationHandler(
  '.delete-dish-form',
  '¿Estás seguro de que deseas eliminar este plato? Esto también eliminará todas las órdenes relacionadas con él.'
);
// alerta para avisar que si se elimina el plato se eliminaran todas las ordenes
// que estén asociadas a el.

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

