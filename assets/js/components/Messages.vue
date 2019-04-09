<template>
    <div>
        <ul class="list-group">
        	<i class="far fa-arrow-alt-circle-up arrow-up-avocado fa-4x" @click="olderMessagesUpload" 
        														@mouseover="olderMessagesUpload"></i>
	        <li class="list-group-item" v-bind:class="{not_read: message.not_read}" v-for="message in messages">
	        	<div v-if="message.need_update" v-on:mouseover="readMessages">
		    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
		    		<p>{{message.text}}</p>
		    		<p>{{message.time}}</p>
		    		<p>{{message.date}}</p>
	        	</div>
	        	<div v-else>
		    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
		    		<p>{{message.text}}</p>
		    		<p>{{message.time}}</p>
		    		<p>{{message.date}}</p>
	        	</div>
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
            	commonRoomSocket: null,
            	counter: 0,
            }
        },
        mounted() {
        	this.commonRoomSocket = new WebSocket(
		        'ws://' + window.location.host +'/ws/chat/common/' + this.room_id + '/');
		    var counter = this.counter
		    this.commonRoomSocket.onopen = function(e) {
			    this.send(JSON.stringify({
			        'counter': counter,
			        'command': 'get_messages'
			    }));
		    };
		  	this.commonRoomSocket.addEventListener("message", e =>{
		    	var data = JSON.parse(e.data);
		    	if (data['messages_portion']){
	        		var messages = data['messages_portion']
	        		var new_counter = data['counter']
	        		this.raw_messages = messages
	        		this.messages = this.raw_messages.reverse().concat(this.messages)
	        		this.counter = new_counter
		    	}
		    	else if (data['new_message']){
			    	var message = data['new_message'];
	        		this.messages = this.messages.concat(message)	
		    	}
		    	else if (data['updated_messages']){
			    	var updated = data['updated_messages'];
	        		for (var i = 0; i < updated.length; i++) {
	        			this.updateMessage(updated[i]);
	        		}
		    	}

		  	});
			window.addEventListener('keypress', this.keyListener);

        },
        methods: {
		 		sendMessage: function(e){
		 			e.preventDefault()
		 			var text_message = this.text_input
		 			text_message = text_message.trim()
		 			if (text_message !=''){
					   	this.commonRoomSocket.send(JSON.stringify({
					            'message': text_message,
					            'command': 'create_message'
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
		 			this.commonRoomSocket.send(JSON.stringify({
				        'counter': this.counter,
				        'command': 'get_messages'
				    }));
		 		},
		 		readMessages: function(){
	 				this.commonRoomSocket.send(JSON.stringify({
			            'counter': this.counter,
			   			'command': 'read_messages'
			        }));
		 		},
		 		updateMessage: function(arr){
	 				for (var i = 0; i < this.messages.length; i++) {
	 					if (this.messages[i].id == arr.id){
	 						this.messages[i].not_read = arr.not_read
	 						this.messages[i].need_update = arr.need_update
	 					}
	 				}
		 		}

            }      
        };
</script>

<style>
</style>
