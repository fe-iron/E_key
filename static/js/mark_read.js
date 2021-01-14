		$('#bell_notif').on('click', function(){
		user_data = $('#bell_notif').attr('aria-valuenow');

			$.ajax({
				type: 'GET',
				url: 'mark_read',
				data: {'email': user_data},
				success: function(response){
					$('#notification_number').html('');
					window.setTimeout(function(){
                        $('.extra').addClass('read');
                    }, 2000);
				},
				error: function(response){
					console.log("error: "+response);
				}
			})
		});