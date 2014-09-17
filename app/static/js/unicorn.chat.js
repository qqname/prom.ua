/**
 * Unicorn Admin Template
 * Version 2.2.0
 * Diablo9983 -> diablo9983@gmail.com
**/

$(document).ready(function(){
	namespace = '/chat'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!', nickname: 'Chat!'});
    });

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function(msg) {
        //$('#log').append('<br>Received #' + msg.count + ': ' + msg.data);
        add_message('test' ,'../static/img/demo/av1.jpg', msg.data, true)
    });

    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val(), nickname: ''});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#join').submit(function(event) {
        socket.emit('join', {room: $('#join_room').val()});
        return false;
    });
    $('form#leave').submit(function(event) {
        socket.emit('leave', {room: $('#leave_room').val()});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my room event', {room: $('#room_name').val(), data: $('#room_data').val()});
        return false;
    });
	var msg_template = '<p><span class="msg-block"><strong></strong><span class="time"></span><span class="msg"></span></span></p>';
	var widget_chat = $('.widget-chat');
	var messages = $('#chat-messages');
	var message_box = $('.chat-message');
	var message_box_input = $('.chat-message input[type="text"]');
	var messages_inner = $('#chat-messages-inner');


	
	messages.niceScroll({
		zindex: 1060
	});

	/*message_box_input.keypress(function(e){
    if($(this).val() != '') $('.input-box').removeClass('has-error');
		if(e.which == 13) {
			if($(this).val() != ''){
				add_message('You','../static/img/demo/av1.jpg',$(this).val(),true);
                socket.emit('my event', {data: $(this).val()});
			} else {
				$('.input-box').addClass('has-error');
			}
		}
	});*/
	

   	var i = 0;
	function add_message(name,img,msg,clear) {

		i = i + 1;
		
		var time = new Date();
		var hours = time.getHours();
		var minutes = time.getMinutes();
		if(hours < 10) hours = '0' + hours;
		if(minutes < 10) minutes = '0' + minutes;
		var id = 'msg-'+i;
        var idname = name.replace(' ','-').toLowerCase();
		messages_inner.append('<p id="'+id+'" class="user-'+idname+'"><img src="'+img+'" alt="" />'
										+'<span class="msg-block"><strong>'+name+'</strong> <span class="time">- '+hours+':'+minutes+'</span>'
										+'<span class="msg">'+msg+'</span></span></p>');
		$('#'+id).fadeOut(0).addClass('show');
		if(clear) {
			$('.input-box').removeClass('has-error');
			message_box_input.val('').focus();

		}
		messages.animate({ scrollTop: messages_inner.height() },1000);
		
		messages.getNiceScroll().resize();
	}
    function remove_user(userid,name) {
        i = i + 1;
        $('.contact-list li#user-'+userid).addClass('offline').delay(1000).slideUp(800,function(){
            $(this).remove();
        });
        var id = 'msg-'+i;
        messages_inner.append('<p class="offline al" id="'+id+'"><span>User <a href="#">@'+name+'</a> left the chat</span></p>');
        $('#'+id).fadeOut(0).addClass('show');
    }
});
