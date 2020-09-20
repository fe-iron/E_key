//to popup login history
function pop(pk){
        // GET AJAX request

        $.ajax({
            type: 'GET',
            url: "validate_nickname",
            data: {"pk": pk},
            success: function (response) {
                // if not valid user, alert the user
                if(response["history"] == false){
                    $('#modal-body-login-history').html('<div class="h4">No login history to show</div>');
                    user_name(pk);
                }else{
                var text = '';
                var count = 0;
                    for(i=0;i<response.length;i++){
                        var date = response[i]['fields']['login_date'];
                        var time = response[i]['fields']['login_time'];
                        var IP = response[i]['fields']['login_IP'];
                        var device_name = response[i]['fields']['device_name'];
                        count = count + 1;
                        text += '<tr><th scope="row">'+count+'</th><td>'+date+'</td><td>'+time.slice(0,-(time.length-5))+'</td><td>'+device_name+'</td><td>'+IP+'</td></tr>';
                    }
                    $('#modal-body-login-history').html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">Sr. No.</th><th scope="col">Date</th><th scope="col">Time</th><th scope="col">Device Name</th><th scope="col">Login IP Address</th></tr></thead><tbody>'+text+'</tbody></table></div>');
                    user_name(pk);
                }

			$('.imagepreview').attr('src', $(this).find('img').attr('src'));
			$('#imagemodal').modal('show');
            },
            error: function (response) {
                console.log(response)
            }
        })
}


//to fetch seller name for the login history
function user_name(pk){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "find_username",
            data: {"pk": pk},
            success: function (response) {
                if(response['name'] == false){
                    $("#modal-title-history").html("Login History of Seller");
                } else{
                    $("#modal-title-history").html("Login History of Seller "+response['name']);
                }
            },
            error: function (response) {
                console.log(response)
            }
        })
}


//to delete seller
function delete_user(pk){
        // GET AJAX request

        $.ajax({
            type: 'GET',
            url: "delete",
            data: {"pk": pk},
            success: function (response) {
                    if(response['msg'] == false){
                        $("#confirm-message").html("Something went wrong, Try again");
                        $("#confirm-message-color").css("color","red");
                    }else{
                        $("#confirm-message").html(response['msg']);
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#confirm').modal('show');
                    }
                    window.setTimeout(function(){
                        location.reload(true);
                    }, 2000);

            },
            error: function (response) {
                console.log(response)
            }
        })
}


//to freeze seller
function freeze_user(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "freeze",
            data: {"pk": pk, "user": accType},
            success: function (response) {
                    if(response['msg'] == false){
                        $("#confirm-message").html("Something went wrong, Try again");
                        $("#confirm-message-color").css("color","red");
                    }else{
                        $("#confirm-message").html(response['msg']);
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#confirm').modal('show');
                    }
                    window.setTimeout(function(){
                        location.reload(true);
                    }, 2000);

            },
            error: function (response) {
                console.log(response)
            }
        })
}


function unfreeze_user(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "unfreeze",
            data: {"pk": pk, "user": accType},
            success: function (response) {
                    if(response['msg'] == false){
                        $("#confirm-message").html("Something went wrong, Try again");
                        $("#confirm-message-color").css("color","red");
                    }else{
                        $("#confirm-message").html(response['msg']);
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#confirm').modal('show');
                    }
                    window.setTimeout(function(){
                        location.reload(true);
                    }, 2000);

            },
            error: function (response) {
                console.log(response)
            }
        })

}
