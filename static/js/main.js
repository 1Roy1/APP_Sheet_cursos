// inicializacion de tooltips de bootstrap
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// confirmacion para eliminar registros
function confirmDeletion(event) {
    if (!confirm('¿Seguro que deseas eliminar este registro?')) {
        event.preventDefault();
    }
}
