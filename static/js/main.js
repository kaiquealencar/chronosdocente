const menuButton = document.getElementById('menuButton');
const menuDropdown = document.getElementById('menuDropdown');

if (menuButton && menuDropdown) {
    menuButton.addEventListener('click', () => {
        menuDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', (event) => {
        if (!menuButton.contains(event.target) && !menuDropdown.contains(event.target)) {
            menuDropdown.classList.add('hidden');
        }
    });
}

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
        padding: '2rem',
        customClass: {
            popup: 'rounded-[2rem] shadow-2xl border border-slate-100',
            title: 'text-2xl tracking-tight',
            confirmButton: 'rounded-2xl px-6 py-3 font-bold transition-all hover:-translate-y-0.5 shadow-lg shadow-indigo-100',
            cancelButton: 'rounded-2xl px-6 py-3 font-bold transition-all hover:-translate-y-0.5'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            formulario.submit(); 
        }
    });
}