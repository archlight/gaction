$(function(){

	var accessToken = "9616a33578ed439c9ff39d56fe739bf0";
	var baseUrl = "https://api.api.ai/v1/";

	var recognition;

	function startRecognition() {
		recognition = new webkitSpeechRecognition();
		recognition.onstart = function(event) {
			updateRec();
		};
		recognition.onresult = function(event) {
			var text = "";
		    for (var i = event.resultIndex; i < event.results.length; ++i) {
		    	text += event.results[i][0].transcript;
		    }
		    setInput(text);
			stopRecognition();
		};
		recognition.onend = function() {
			stopRecognition();
		};
		recognition.lang = "en-US";
		recognition.start();
	}

	function stopRecognition() {
		if (recognition) {
			recognition.stop();
			recognition = null;
		}
		updateRec();
	}

	function switchRecognition() {
		if (recognition) {
			stopRecognition();
		} else {
			startRecognition();
		}
	}

	function setInput(text) {
		$("#input").val(text);
		send();
	}

	function updateRec() {
		$("#rec").text(recognition ? "Stop" : "Speak");
	}

	function attach_message(text, isClient){
		var message = $('<div class="chat-message"></div>').addClass(isClient?'right':'left')
		message.append($('<img class="message-avatar" alt="">').attr('src', isClient?'img/client.jpg':'img/bot.jpg'))
		content = $('<div class="message"></div>')
		content.append($('<span class="message-content"></span>').text(text))
		message.append(content)
		message.appendTo($('.chat-discussion'))
	}

	function send() {
		var text = $("#input").val();

		attach_message(text, true)

		$.ajax({
			type: "POST",
			url: baseUrl + "query?v=20150910",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			headers: {
				"Authorization": "Bearer " + accessToken
			},
			data: JSON.stringify({ query: text, lang: "en", sessionId: "somerandomthing" }),

			success: function(data) {
				console.log(data)
				setResponse(data);
			},
			error: function() {
				setResponse("Internal Server Error");
			}
		});
	}

	function setResponse(data) {
		if (typeof(data) == 'string')
			attach_message(data, false)
        else
        	attach_message(data.result.fulfillment.displayText, false)

		//testWebhook()
	}

	function testWebhook(){
		console.log('testWebhook')

		$.post('webhook', 
			JSON.stringify({'result':{'parameters':{'source':'CNN', 'sort':''}}}),
			function(data){
				console.log(data)
				attach_message(data, false)
			})
	}

	$("#input").keypress(function(event) {
		if (event.which == 13) {
			event.preventDefault();
			send();
		}
	});
	$("#rec").click(function(event) {
		switchRecognition();
	});
	$("#webhook").click(function(event){
		$.post('webhook', 
			$("#request").val(),
			function(data){
				console.log(data)
				$("#response").val(JSON.stringify(data))
			})
	})

})