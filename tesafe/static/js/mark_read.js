		$('#bell_notif').on('click', function(){
			var user = '{{request.user}}';
			$.ajax({
				type: 'GET',
				url: 'mark_read',
				data: {'email': user},
				success: function(response){
					$('#notification_number').html('');
					window.setTimeout(function(){
                        $('.extra').addClass('read');
                    }, 8000);

				},
				error: function(response){
					console.log("error: "+response);
				}
			})
		});
