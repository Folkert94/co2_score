$(document).ready(function(){
  $(".btn-group, .dropdown").hover(
      function() {
        $('>.dropdown-menu', this).stop(true, true).fadeIn("fast");
        $(this).addClass('open');
      },
      function() {
        $('>.dropdown-menu', this).stop(true, true).fadeOut("fast");
        $(this).removeClass('open');
      });
  
    $(".dropdown-item").click(function select() {
      let name = $(this).text();
      $("#dLabel").text(name);
      $('input[name="name"]').val(name);
    });
});