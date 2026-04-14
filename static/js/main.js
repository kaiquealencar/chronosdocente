document.addEventListener('DOMContentLoaded', function() {
    
    const menuButton = document.getElementById('menuButton');
    const menuDropdown = document.getElementById('menuDropdown');

    if (menuButton && menuDropdown) {
        menuButton.addEventListener('click', (e) => {
            e.stopPropagation();
            menuDropdown.classList.toggle('hidden');
        });

        document.addEventListener('click', (e) => {
            if (!menuDropdown.contains(e.target) && e.target !== menuButton) {
                menuDropdown.classList.add('hidden');
            }
        });
    }

    const messageContainer = document.getElementById('flask-messages');
    if (messageContainer) {
        const messages = JSON.parse(messageContainer.dataset.messages || '[]');
        
        if (messages.length > 0) {
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 4000,
                timerProgressBar: true,
                background: '#ffffff',
                color: '#1e293b',
                customClass: {
                    popup: 'rounded-2xl border border-slate-100 shadow-2xl'
                }
            });

            messages.forEach(([category, message]) => {
                Toast.fire({
                    icon: category === 'success' ? 'success' : 'error',
                    title: message,
                    iconColor: category === 'success' ? '#4f46e5' : '#ef4444'
                });
            });
        }
    }
});

function confirmarExclusao(event, elemento) {
    event.preventDefault();
    const formulario = elemento.closest('form');

    Swal.fire({
        title: '<span class="text-slate-800 font-bold">Tem certeza?</span>',
        text: "Esta ação não pode ser desfeita!",
        icon: 'warning',
        iconColor: '#f59e0b',
        showCancelButton: true,
        confirmButtonColor: '#4f46e5',
        cancelButtonColor: '#ef4444',
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar',
        reverseButtons: true,
        background: '#ffffff',
        customClass: {
            popup: 'rounded-[2rem] shadow-2xl border border-slate-100',
            confirmButton: 'rounded-2xl px-6 py-3 font-bold',
            cancelButton: 'rounded-2xl px-6 py-3 font-bold'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            formulario.submit();
        }
    });
}