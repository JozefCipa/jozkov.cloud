$(document).ready(function() {

	$('form').on('submit', function(e){ 
		e.preventDefault();

		var url = $(this).find('input[name="url"]').val();
		var name = $(this).find('input[name="name"]').val();

		var $msg = $('#msg');
		var $url = $('#url');

		if (url.trim() != '') {
			$.ajax({
				url: '/add-url',
				method: 'POST',
				data: {url: url, name: name},
				success: function(res) {

					if (res.msg) {
						$url.css('visibility', 'hidden');
						$msg
							.html(res.msg)
							.css('visibility', 'visible');
					} else {
						$msg.css('visibility', 'hidden');
						$url
							.html(res.yourUrl)
							.css('visibility', 'visible');
					}
				},
				error: function(err) {
					$msg.html('Something went wrong. Couldn\'t handle your request.');
				}
			});
		}

	});
});