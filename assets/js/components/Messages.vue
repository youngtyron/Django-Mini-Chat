<template>
    <div>
        <ul class="list-group">
        	<i class="far fa-arrow-alt-circle-up arrow-up-avocado fa-4x" @click="olderMessagesUpload" 
        														@mouseover="olderMessagesUpload"></i>
	        <li class="list-group-item" 
	        	v-bind:class="{not_read: message.not_read, my_message_block: message.mine, anothers_message_block: !message.mine}"
	        	v-for="message in messages">
	        	<div v-if="message.need_update" v-on:mouseover="readMessages">
		    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
		    		<p>{{message.text}}</p>
		    		<p>{{message.time}}</p>
		    		<p>{{message.date}}</p>
		    		<div v-for="image in message.images">
		    			<img :src="image" alt="Image">
		    		</div>
	        	</div>
	        	<div v-else>
		    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
		    		<p>{{message.text}}</p>
		    		<p>{{message.time}}</p>
		    		<p>{{message.date}}</p>
		    		<div v-for="image in message.images">
		    			<img :src="image" alt="Image">
		    		</div>
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
		<form enctype="multipart/form-data" id="images-form">
		   	<input type="file" id="images-input" name="images-input" v-on:change="changeImagesInput" class="form-control" multiple>
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
            	images_input: '',
            	commonRoomSocket: null,
            	counter: 0,
            	ImagesFormData: null
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
		    	console.log(data)
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
		 			var id_list = false
		 			var commonRoomSocket = this.commonRoomSocket
		 			if (text_message !=''){
					   	axios.post('/chat/send_message_images/' + this.room_id + '/', this.ImagesFormData, {
					        headers: {
					          'Content-Type': 'multipart/form-data'
					        }
					    }).then(function(response){
					    	id_list = response.data['id_list']
						   	commonRoomSocket.send(JSON.stringify({
						            'message': text_message,
						            'images' : id_list,
						            'command': 'create_message'
						        }));
					    }).catch(function(error){
					    	console.error(error)
					  		this.text_input=''
					  		this.ImagesFormData == null
					    });

		 			}
			  		this.text_input=''
			  		this.ImagesFormData == null
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
		 		},
		 		changeImagesInput: function(){
		 			this.ImagesFormData = new FormData(document.getElementById('images-form'))
		 		}

            }      
        };
</script>

<style>
</style>
