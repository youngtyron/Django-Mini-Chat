<template>
    <div>

        <p>MessagesBlock</p>
    	<li v-for="message in messages">
    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
    		<p>{{message.text}}</p>
    		<p>{{message.time}}</p>
    		<p>{{message.date}}</p>
    	</li>
	    <input id="chat-message-input" v-model="text_input" type="text" size="100"/><br/>
    	<input id="chat-message-submit" type="button" @click="sendMessage" value="Send"/>
    </div>
</template>

<script>
    export default {
    	props: ['room_id'],
        data(){
            return  {
            	messages: [],
            	text_input: '',
            	chatSocket: null
            }
        },
        mounted() {
		    this.chatSocket = new WebSocket(
		        'ws://' + window.location.host +'/ws/chat/' + this.room_id + '/');
		    this.chatSocket.onopen = function(e) {
		    	console.log('chat socket opened')
		    };
		    this.chatSocket.onmessage = function(e) {
				console.log('chat socket message func')
				console.log(e.data)
				var data = JSON.parse(e.data);
        		var message = data['message'];
				console.log(message)
		    };
		    this.chatSocket.onclose = function(e) {
		        console.error('Chat socket closed unexpectedly');
		    };
        	this.loadMessages()
        },
        methods: {
		 		loadMessages: function(){
		            axios.get('/chat/api/messages/'+this.room_id).then((response)=> {
			            this.messages = response.data;
		            });
		 		},
		 		sendMessage: function(){
		 			console.log('message typed')
		 			var text_message = this.text_input
					this.chatSocket.send(JSON.stringify({
			            'message': text_message
			        }));
		 		}
            }      
        };
</script>

<style>
</style>
