$(document).ready(function(){
    $('.table').paging({limit:20});
    $(".datetimeinput").datepicker(
        {
            changeYear: true,
            changeMonth: true, 
            dateFormat: 'yy-mm-dd'
        }
    );  
  });