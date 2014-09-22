/**
 * Unicorn Admin Template
 * Version 2.2.0
 * Diablo9983 -> diablo9983@gmail.com
**/

$(document).ready(function(){
            namespace = '/chat';

            var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
            socket.on('connect', function() {
                socket.emit('new user', {username: username});

            });

            socket.on('my response', function(msg) {
                add_message(msg.nickname, '../static/img/demo/av1.jpg', msg.data, true);
            });

            socket.on('refresh users', function(msg){
                add_user(msg.data, msg.data);
            });

            socket.on('leaver', function(msg){
                remove_user(msg.data, msg.data);
            });





            $('form#emit').submit(function(event) {
                socket.emit('send msg', {room: roomname, data: $('#emit_data').val()});
                $('.input-box').removeClass('has-error');
			    message_box_input.val('').focus();
                return false;
            });

	var msg_template = '<p><span class="msg-block"><strong></strong><span class="time"></span><span class="msg"></span></span></p>';
	var widget_chat = $('.widget-chat');
	var messages = $('#chat-messages');
	var message_box = $('.chat-message');
	var message_box_input = $('.chat-message input[type="text"]');
	var messages_inner = $('#chat-messages-inner');
    var user_list = $('ul.contact-list')


	
	messages.niceScroll({
		zindex: 1060
	});



   	var i = 0;
	function add_message(name,img,msg) {

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

		messages.animate({ scrollTop: messages_inner.height() },1000);
		
		messages.getNiceScroll().resize();
	}
    function remove_user(userid,name) {
        i = i + 1;
        $('.contact-list li#user-'+userid).addClass('offline').delay(1000).slideUp(800,function(){
            $(this).remove();
        });


    }
    function add_user(userid,name) {
        i = i + 1;
        user_list.append('<li id="user-'+userid+'" class="online"><a href="#"><img alt="" src="../static/img/demo/av1.jpg" /> <span>'+name+'</span></a></li>');



    }
});

