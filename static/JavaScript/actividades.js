const checkboxes = document.querySelectorAll('.tarea-checkbox');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        // Obtener las tareas completadas
        const tarea_completada = Array.from(checkboxes)
            .filter(cbx => cbx.checked)
            .map(cbx => cbx.getAttribute('data-idx')); // Obtener el índice de las tareas completadas

        // Enviar los datos al backend usando Fetch API
        fetch('/actualizar_tarea', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tarea_completada: tarea_completada })
        })
        .then(response => response.json())
        .then(data => {
            // Actualizar la racha y el color de la racha en el frontend
            const rachaElement = document.querySelector('#racha-fuego');
            rachaElement.innerText = `${data.racha} 🔥`;
            rachaElement.style.color = data.color_racha;

            // Cambiar animación dependiendo de la racha
            if (data.racha >= 5) {
                rachaElement.classList.add('gold'); // Cambiar a dorado cuando la racha es 5 o más
            } else {
                rachaElement.classList.remove('gold'); // Quitar dorado si la racha es menor a 5
            }
        });
    });
});
