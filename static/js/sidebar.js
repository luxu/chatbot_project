function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');

    // Lógica para trocar o ícone
    if (sidebar.classList.contains('active')) {
        btn.innerHTML = "✕"; // Muda para X
    } else {
        btn.innerHTML = "☰"; // Volta para Hambúrguer
    }
}
