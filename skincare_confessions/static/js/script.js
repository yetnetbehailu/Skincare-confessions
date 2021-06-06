$('#sidebarCollapse').click( function () {
    $('#sidebar').toggleClass('active');
});

/* Listens to change event on is_vegan boolean checkboxfield, marks true when checked */
$('#is_vegan').on('change', (e) => {
  this.checkbox = e.target.checked ? 'true' : 'false';
})

