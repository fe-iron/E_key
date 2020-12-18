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

// to show chat history
function chat_history(user_name, fk){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "chat_history",
            data: {"fk": fk},
            success: function (response) {
                // if not valid user, alert the user

                if(response["history"] == false){
                    $("#modal-title-history").html("Chat History of "+user_name);
                    $('#modal-body-login-history').html('<div class="h4">No Chat history to show with '+user_name+'</div>');
                }else{
                var text = '';
                var count = 0;
                    for(i=0;i<response.length;i++){
                        var timestamp = response[i]['fields']['timestamp'];
                        var msg = response[i]['fields']['body'];
                        var date = timestamp.slice(0,10)
                        var time = timestamp.slice(12,17)

                        count = count + 1;
                        text += '<tr><th scope="row">'+count+'</th><td>'+msg+'</td><td>'+time+' & '+date+'</td></tr>';
                    }
                    $("#modal-title-history").html("Chat History of "+user_name);
                    $('#modal-body-login-history').html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">Sr. No.</th><th scope="col">Message</th><th scope="col">Timestamp</th></tr></thead><tbody>'+text+'</tbody></table></div>');
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
            data: {"pk": pk, "accType": accType},
            success: function (response) {
                // if not valid user, alert the user

                if(response["history"] == false){
                    $('#modal-body-login-history').html('<div class="h4">No Use Record history to show</div>');
                    user_name(pk, accType);
                }else{
                    var text = '';
                    var count = 0;
                    for(i=0;i<response.length;i++){
                            var date = response[i]['fields']['date'];
                            var time = response[i]['fields']['time'];
                            var my_password = response[i]['fields']['password'];
                            count = count + 1;
                            text += '<tr><th scope="row">'+count+'</th><td>'+date+'</td><td>'+time.slice(0,-(time.length-5))+'</td><td><input id="RevRec'+count+'" type="password" readonly value="'+my_password+'" style="background-color: white;border: none"><i class="far fa-eye togglePassword" data-to="'+count+'"></i></td></tr>';
                        }
                    $('#modal-body-login-history').html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">Sr. No.</th><th scope="col">Date</th><th scope="col">Time</th><th scope="col">Password</th></tr></thead><tbody>'+text+'</tbody></table></div>');
                    user_name(pk, accType);

                    //togglePassword = document.querySelector('.togglePassword');

                    $(".togglePassword").on('click', function (e) {
                        // toggle the type attribute
                        var pass_id = $(this).attr("data-to");
                        var type = $("#RevRec"+pass_id).attr('type') === 'password' ? 'text' : 'password';
                        $("#RevRec"+pass_id).attr('type', type);
                        // toggle the eye slash icon
                        this.classList.toggle('fa-eye-slash');
                    });
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
                        var last_pass = response[i]['fields']['last_pass'];
                        count = count + 1;
                        text += '<tr><th scope="row">'+count+'</th><td>'+date+'</td><td>'+time.slice(0,-(time.length-5))+'</td><td>'+device_name+'</td><td><input type="password" value="'+last_pass+'" style="background-color: white;border: none" id="'+count+'"><i class="far fa-eye" onclick="togglePassword1('+count+')" id="toggle'+count+'"></i></td></tr>';
                    }
                    $('#modal-body-login-history').html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">Sr. No.</th><th scope="col">Date</th><th scope="col">Time</th><th scope="col">Device Name</th><th scope="col">Last Password</th></tr></thead><tbody>'+text+'</tbody></table></div>');

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
                            text += "<tr><td>"+response[i]['fields']['first_name']+" "+response[i]['fields']['last_name']+"</td><td> <input type='checkbox' value='' class='ml-5 "+pk+"' name="+response[i]['pk']+" /> </td></tr>"
                        }

                        $("#tester_modal").html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">Tester Name</th><th scope="col">Select</th></tr><tbody>'+text+'</tbody></table></div>');
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

//to tester list
function userToUser_list(pk, pwg_id, action){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "user_list",
            data: {"pk": pk},
            success: function (response) {
                    if(response['data'] == false){
                        $("#tester_modal").html("<h5>You have no users yet!</h5>");
                        $("#tester_modal").css("color","red");
                        $("#confirm-modal-button").attr("disabled",true);
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#imagemodalConfirm').modal('show');
                    }else{
                        var sub_text = '';
                        var text = '';
                        var flag = true;
                        for (var key in response) {
                            // check if the property/key is defined in the object itself, not in parent
                            if (response.hasOwnProperty(key)) {
                                if(flag){
                                    sub_text += "<tr><td>"+response[key]+"</td>";
                                    flag = false;
                                }else{
                                    if(action == "transfer"){
                                        sub_text += "<td> <input type='radio' value='' class='ml-5 "+pwg_id+"' name="+response[key]+" /> </td></tr>";
                                    }else if(action == "transfer_multiple_pwg"){
                                        sub_text += "<td> <input type='radio' value='' class='ml-5 "+pwg_id[0]+"' name="+response[key]+" /> </td></tr>";
                                    }else if(action == "authorize_multiple" || action == "share_multiple_pwg"){
                                        sub_text += "<td> <input type='checkbox' value='' class='ml-5 "+pwg_id[0]+"' name="+response[key]+" /> </td></tr>";
                                    }else{
                                        sub_text += "<td> <input type='checkbox' value='' class='ml-5 "+pwg_id+"' name="+response[key]+" /> </td></tr>";
                                    }
                                    flag = true;
                                }
                            }
                            if(flag){
                                text += sub_text;
                                sub_text = '';
                            }
                        }

                        $("#tester_modal").html('<div class="table-responsive"><table class="table"><thead><tr><th scope="col">My Users</th><th scope="col">Select</th></tr><tbody>'+text+'</tbody></table></div>');

                        if(action == "authorize"){
                            $("#confirm-modal-button").attr('onclick', 'assign('+pwg_id+')');
                        }else if(action == "share"){
                            $("#confirm-modal-button").attr('onclick', 'share('+pwg_id+')');
                        }else if(action == "transfer"){
                            $("#confirm-modal-button").attr('onclick', 'transfer('+pwg_id+')');
                        }else if(action == "authorize_multiple"){
                            $("#confirm-modal-button").attr('onclick', 'authorize_submit('+pwg_id[0]+')');
                        }else if(action == "share_multiple_pwg"){
                            $("#confirm-modal-button").attr('onclick', 'share_submit_pwg('+pwg_id[0]+')');
                        }else if(action == "transfer_multiple_pwg"){
                            $("#confirm-modal-button").attr('onclick', 'transfer_submit_pwg('+pwg_id[0]+')');
                        }
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#imagemodalConfirm').modal('show');

                        // event listener on click on checkboxes
                        if(action == "authorize" || action == "share"){
                            $('.'+pwg_id).click(function() {
                                if($(this).is(':checked')){
                                    var name = $(this).attr('name');
                                    $(this).val(name);
                                }else{
                                    $(this).val('');
                                }
                            });
                        }else if(action == "authorize_multiple" || action == "share_multiple_pwg"){
                            $('.'+pwg_id[0]).click(function() {
                                if($(this).is(':checked')){
                                    var name = $(this).attr('name');
                                    $(this).val(name);
                                }else{
                                    $(this).val('');
                                }
                            });
                        }else if(action == "transfer_multiple_pwg"){
                            $('.'+pwg_id[0]).click(function() {
                                names = $('.'+pwg_id);
                                    for(i=0;i<names.length;i++){
                                        value = names[i]['value'];
                                        if(value != ''){
                                            names[i]['value'] = '';
                                        }
                                    }
                                    if($(this).is(':checked')){
                                        var name = $(this).attr('name');
                                        $(this).val(name);
                                        $('input[type="radio"]').prop('checked', false);
                                        $(this).prop('checked', true);
                                    }
                            });
                        }else{
                            $('.'+pwg_id).click(function() {
                                names = $('.'+pwg_id);
                                    for(i=0;i<names.length;i++){
                                        value = names[i]['value'];
                                        if(value != ''){
                                            names[i]['value'] = '';
                                        }
                                    }
                                    if($(this).is(':checked')){
                                        var name = $(this).attr('name');
                                        $(this).val(name);
                                        $('input[type="radio"]').prop('checked', false);
                                        $(this).prop('checked', true);
                                    }
                            });
                        }
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

//to get system exclusive name
function get_name(accType){
        // GET AJAX request
        var nnn = $('#unique_name').val();
        $.ajax({
            type: 'GET',
            url: "unique_name",
            data: {"accType": accType, "nnn": nnn},
            success: function (response) {
                    if(response['msg'] == false){
                        $("#confirm-message").html("Something went wrong, Try again");
                        $("#confirm-message-color").css("color","red");
                    }else{
                        $("#unique_name_value").attr('value',response['msg']);
                    }

            },
            error: function (response) {
                console.log(response)
            }
        })

}

//to deauthorize the pwg from a user
function deauthorize(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "deauthorize",
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
                    }, 3000);

            },
            error: function (response) {
                console.log(response)
            }
        })

}

//to deauthorize the pwg from a user
function deshare(pk, accType){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "deshare",
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
                    }, 3000);

            },
            error: function (response) {
                console.log(response)
            }
        })

}

//to delete a user temporarily
function delete_temp_user(pk, accType){
      	$.ajax({
            type: 'GET',
            url: "delete_temp",
            data: {"pk": pk, "accType": accType},
            success: function (response) {
                    if(response['msg'] == false){
                        $("#confirm-message").html(response['msg']);
                        $("#confirm-message-color").css("color","red");
                    }else{
                        $("#confirm-message").html(response['msg']);
                        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                        $('#confirm').modal('show');
                    }
                    window.setTimeout(function(){
                        location.reload(true);
                    }, 6000);

            },
            error: function (response) {
                console.log(response)
            }
        })
      }
