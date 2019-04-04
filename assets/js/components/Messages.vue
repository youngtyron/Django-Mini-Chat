<template>
    <div>
        <ul class="list-group">
        	<i class="far fa-arrow-alt-circle-up arrow-up-avocado fa-4x" @click="olderMessagesUpload" 
        														@mouseover="olderMessagesUpload"></i>
	        <li class="list-group-item" v-for="message in messages">
	    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
	    		<p>{{message.text}}</p>
	    		<p>{{message.time}}</p>
	    		<p>{{message.date}}</p>
	    	</li>
        </ul>
    	<form action="">
    		<div class="form-group col-md-6">
    			<input type="text" id="message-input" v-model="text_input" required="required" class="form-control">
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
            	raw_messages: [],
            	text_input: '',
            	newMessageSocket: null,
            	portionMessagesSocket: null,
            	counter: 0,
            }
        },
        mounted() {
        	// this.loadMessages()
		    this.portionMessagesSocket = new WebSocket(
		        'ws://' + window.location.host +'/ws/chat/portion/' + this.room_id + '/');
		  	this.portionMessagesSocket.addEventListener("message", e =>{
		    	var data = JSON.parse(e.data);
        		var messages = data['messages']
        		var new_counter = data['counter']
        		this.raw_messages = messages
        		this.messages = this.raw_messages.reverse().concat(this.messages)
        		this.counter = new_counter
		  	});
		    this.portionMessagesSocket.onclose = function(e) {
		        console.error('Chat socket closed unexpectedly');
		    };
		    var counter = this.counter
		    this.portionMessagesSocket.onopen = function(e) {
			    this.send(JSON.stringify({
			        'counter': counter
			    }));
		    };
		    this.newMessageSocket = new WebSocket(
		        'ws://' + window.location.host +'/ws/chat/newmessages/' + this.room_id + '/');
		  	this.newMessageSocket.addEventListener("message", e =>{
		    	var data = JSON.parse(e.data);
        		var message = data['message'];
        		this.messages = this.messages.concat(message)
		  	});
		    this.newMessageSocket.onclose = function(e) {
		        console.error('Chat socket closed unexpectedly');
		    };
			window.addEventListener('keypress', this.keyListener);

        },
        methods: {
		 		// loadMessages: function(){
		   //          axios.get('/chat/api/messages/'+this.room_id).then((response)=> {
		   //          	this.raw_messages = response.data
			  //           this.messages = this.raw_messages.reverse();
			  //           this.raw_messages = []
		   //          });
		 		// },
		 		sendMessage: function(e){
		 			e.preventDefault()
		 			var text_message = this.text_input
		 			text_message = text_message.trim()
		 			if (text_message !=''){
			 			this.newMessageSocket.send(JSON.stringify({
				            'message': text_message
				        }));
		 			}
			  		this.text_input=''
		 		},
		 		keyListener: function(e){
		 			var key = e.keyCode
		 			if (key==13) {
					 	if (document.activeElement == document.getElementById('message-input')){
			              this.sendMessage(e)
			            }
		 			}
		 		},
		 		olderMessagesUpload: function(){
		 			this.portionMessagesSocket.send(JSON.stringify({
				        'counter': this.counter
				    }));
		 		}
            }      
        };
</script>

<style>
</style>
