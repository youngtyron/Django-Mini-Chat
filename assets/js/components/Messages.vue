<template>
    <div>
        <ul class="list-group">
	        <li class="list-group-item" v-for="message in messages">
	    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
	    		<p>{{message.text}}</p>
	    		<p>{{message.time}}</p>
	    		<p>{{message.date}}</p>
	    	</li>
        </ul>
    	<form action="">
    		<div class="form-group col-md-6">
    			<input type="text" v-model="text_input" required="required" class="form-control">
    		</div>
    		<div class="form-group col-md-6">
    			<button type="submit" class="btn btn-avocado" @click="sendMessage">Send</button>
    		</div>
		</form>
    </div>
</template>

<script>
    export default {
    	props: ['room_id'],
        data(){
            return  {
            	messages: [],
            	text_input: '',
            	chatSocket: null,
            }
        },
        mounted() {
        	this.loadMessages()
		    this.chatSocket = new WebSocket(
		        'ws://' + window.location.host +'/ws/chat/' + this.room_id + '/');

		  	this.chatSocket.addEventListener("message", e =>{
		    	var data = JSON.parse(e.data);
        		var message = data['message'];
        		this.messages = this.messages.concat(message)
		  	});

		    this.chatSocket.onclose = function(e) {
		        console.error('Chat socket closed unexpectedly');
		    };
        },
        methods: {
		 		loadMessages: function(){
		            axios.get('/chat/api/messages/'+this.room_id).then((response)=> {
			            this.messages = response.data;
		            });
		 		},
		 		sendMessage: function(e){
		 			e.preventDefault()
		 			var text_message = this.text_input
					this.chatSocket.send(JSON.stringify({
			            'message': text_message
			        }));

		 		},
            }      
        };
</script>

<style>
</style>
