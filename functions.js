
<script>


function relay_function() {

  setTimeout(function(){
      
    function update_page() {
      $.ajax({
        //method: "GET",
        url: "/live/crypto/marketdata",
  
        // headers: {"X-CSRFToken": csrftoken},
        success: function(data) {
          console.log("New Data Loaded")
          $('#MARKET_PANEL').html(data);
          $('#update_notice').attr('id','OnerotationFunction');

        }
      })
    };

    update_page()


  },10000) // 15 seconds

}

  setTimeout(function(){

    $('#update_notice').attr('id','OnerotationFunctionNULL');
  },3000) // 5 seconds

  relay_function();

{% comment %} 
 {% endcomment %}

  

</script>
