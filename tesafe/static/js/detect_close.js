function logout() {
  $.ajax({
      type: 'GET',
      url: "logout",
      data: {},
      success: function (response) {
           if(response['msg'] == false){

           }else{

           }
      },
      error: function (response) {
           console.log(response)
      }
  })
}

window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    logout();
});