
//to transfer PWG and PWGS
function transfer_pwgs(checkbox_values){
        // GET AJAX request

        $.ajax({
            type: 'GET',
            url: "transfer_pwgs",
            data: JSON.stringify({ "value": checkbox_values }),
            success: function (response) {
                    if(response['name'] == false){
                        console.log(response['name']);
                        $("#confirm-message").html("Something went wrong, Try again");
                        $("#confirm-message-color").css("color","red");
                    }else{
                        $("#confirm-message").html(response['msg']);
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#confirm').modal('show');
                    }

            },
            error: function (response) {
                console.log(response)
            }
        })
}