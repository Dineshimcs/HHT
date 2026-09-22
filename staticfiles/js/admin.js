/* Operations Admin Dashboard Controller */
const AuraAdmin = {
  init() {
    this.bindFilters();
  },

  bindFilters() {
    const filterInput = document.getElementById('admin-table-search');
    if (filterInput) {
      filterInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        document.querySelectorAll('#admin-trips-table-body tr').forEach(row => {
          const text = row.innerText.toLowerCase();
          row.style.display = text.includes(query) ? '' : 'none';
        });
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  AuraAdmin.init();
});
