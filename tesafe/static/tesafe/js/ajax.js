//to popup login history
function pop(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "validate_nickname",
            data: {"pk": pk, "accType": accType},
            success: function (response) {
                // if not valid user, alert the user

                if(response["history"] == false){
                    $('#modal-body-login-history').html('<div class="h4">No login history to show</div>');
                    user_name(pk, accType);
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
                    user_name(pk, accType);
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
function user_name(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "find_username",
            data: {"pk": pk, "accType": accType},
            success: function (response) {
                if(accType == "pwg"){
                    if(response['name'] == false){
                        $("#modal-title-history").html("Use Record of "+accType);
                    } else{
                        $("#modal-title-history").html("Use Record of "+accType+" "+response['name']);
                    }
                }else{
                    if(response['name'] == false){
                        $("#modal-title-history").html("Login History of "+accType);
                    } else{
                        $("#modal-title-history").html("Login History of "+accType+" "+response['name']);
                    }
                }
            },
            error: function (response) {
                console.log(response)
            }
        })
}

// show use record
function pop3(pk, accType){

    $.ajax({
            type: 'GET',
            url: "use_record",
            data: {"pk": pk},
            success: function (response) {
                // if not valid user, alert the user

                if(response["history"] == false){
                    $('#modal-body-login-history').html('<div class="h4">No Use Record history to show</div>');
                    user_name(pk, accType);
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
                        user_name(pk, accType);
                }

                $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                $('#imagemodal').modal('show');
            },
            error: function (response) {
                console.log(response)
            }
        })

}

//to delete seller
function delete_user(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "delete",
            data: {"pk": pk, "accType": accType},
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

//to un freeze user
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

// to get pwgs pwd history
function pwd_history(pk){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "getpassword",
            data: {"pk": pk},
            success: function (response) {
                // if not valid user, alert the user
                if(response["history"] == false){
                    $("#modal-title-history").html("Password History of PWG Server");
                    $('#modal-body-login-history').html('<div class="h4">No Password history to show</div>');

                }else{
                $("#modal-title-history").html("Password History of PWG Server");
                var text = '';
                var count = 0;
                    for(i=0;i<response.length;i++){
                        var time = response[i]['fields']['login_time'];
                        var date = response[i]['fields']['login_date'];
                        var device_name = response[i]['fields']['device_name'];
                        var device_name = response[i]['fields']['last_pass'];
                        count = count + 1;
                        text += '<tr><th scope="row">'+count+'</th><td>'+date+'</td><td>'+time.slice(0,-(time.length-5))+'</td><td>'+device_name+'</td><td>'+IP+'</td></tr>';
                    }
                    $('#modal-body-login-history').html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">Sr. No.</th><th scope="col">Date</th><th scope="col">Time</th><th scope="col">Device Name</th><th scope="col">Login IP Address</th></tr></thead><tbody>'+text+'</tbody></table></div>');

                }

			$('.imagepreview').attr('src', $(this).find('img').attr('src'));
			$('#imagemodal').modal('show');
            },
            error: function (response) {
                console.log(response)
            }
        })

}

//to assign pwg to tester
function assign(pk){
        tester_pk = [];
        $('#imagemodalConfirm').modal('hide');
        // GET AJAX request
        names = $('.'+pk);
        for(i=0;i<names.length;i++){
            name = names[i]['name']
            value = names[i]['value']
            if(value != ''){
                tester_pk.push(value)
            }
        }
        $("#tester_values").attr('value', tester_pk);
        $("#pwg_pk").attr('value', pk);
        document.forms['assign_multiple'].submit();

}

//to tester list
function tester_list(pk){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "tester_list",
            data: {},
            success: function (response) {
                    if(response['data'] == false){
                        $("#tester_modal").html("<h5>Something went wrong, Try again</h5>");
                        $("#tester_modal").css("color","red");
                    }else{
                    var text = '';
                        for(i=0;i<response.length;i++){
                            text += "<label><b>"+response[i]['fields']['first_name']+" "+response[i]['fields']['last_name']+"</b></label> <input type='checkbox' value='' class='ml-5 "+pk+"' name="+response[i]['pk']+" /> <br>"
                        }

                        $("#tester_modal").html(text);
                        $("#confirm-modal-button").attr('onclick', 'assign('+pk+')');
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#imagemodalConfirm').modal('show');

                        // event listener on click on checkboxes
                        $('.'+pk).click(function() {

                            if($(this).is(':checked')){
                                var name = $(this).attr('name');
                                $(this).val(name);
                            }else{
                                $(this).val('');
                            }
                        });
                    }

            },
            error: function (response) {
                console.log(response)
            }
        })


}

// to getback pwg from tester
function getback(pk){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "getback",
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
                    }, 3000);

            },
            error: function (response) {
                console.log(response)
            }
        })

}
