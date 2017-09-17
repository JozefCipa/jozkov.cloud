$(document).ready(function() {

	$('form').on('submit', function(e){ 
		e.preventDefault();

		var url = $(this).find('input[name="url"]').val();
		var name = $(this).find('input[name="name"]').val();
		var $url = $('#url');

		if (url.trim() != '') {
			$.ajax({
				url: '/add-url',
				method: 'POST',
				data: {url: url, name: name},
				success: function(res) {

					if (res.msg) {
						$url.css('visibility', 'hidden');
						notify(res.msg, 'ERROR')
					} else {
						$('div.notify').remove();
						$url
							.html(res.yourUrl)
							.css('visibility', 'visible');
					}
				},
				error: function(err) {
					notify('Something went wrong. Couldn\'t handle your request.', 'ERROR');
				}
			});
		}

	});
});

function notify(data, type) {
	$('div.notify').remove();
	var $msg = $('<div class="notify ' + type + '">' + data +'</div>');
	$('body').append($msg);
}