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
		    			<img class="message-img" :src="image" alt="Image">
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
    			<input type="text" id="message-input" v-model="text_input" class="form-control">
    		</div>

    		<div class="form-group col-md-6">
    			<i class="fas fa-camera-retro fa-2x avocado-icon" @click="activateImageLoadModal"></i>
    			<button type="submit" class="btn btn-avocado" @click="sendMessage">Send</button>
    		</div>
		</form>
		<div v-if="ImageLoadModal" class="modal-image-load-form text-center">
			<form enctype="multipart/form-data" id="images-form">
				<button type="button" class="btn btn-avocado btn-lg btn-block" @click="activateImagesInput">
					<h4>Add images to your message</h4>
					<i class="far fa-plus-square fa-2x" style="color: #FFFFFF;"></i>
				</button>
				<input type="file" id="images-input" name="images-input" v-on:change="changeImagesInput" class="form-control" multiple>
			</form>
			<div>
				<div v-for="i in 10" class="modal-img-div">
					<img class="modal-img-exmp-place" src="" alt="">		
				</div>
			</div>
		</div>
	

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
            	ImagesFormData: null,
            	ImageLoadModal: false,
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
		 			var id_list = false
		 			var ImagesFormData = this.ImagesFormData
		 			var commonRoomSocket = this.commonRoomSocket
		 			this.ImagesFormData = null
		 			this.text_input = ''
		 			if (text_message !='' && ImagesFormData != null){
					   	axios.post('/chat/send_message_images/' + this.room_id + '/', ImagesFormData, {
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
					    });

		 			}
		 			else if (ImagesFormData != null){
					   	axios.post('/chat/send_message_images/' + this.room_id + '/', ImagesFormData, {
					        headers: {
					          'Content-Type': 'multipart/form-data'
					        }
					    }).then(function(response){
					    	id_list = response.data['id_list']
						   	commonRoomSocket.send(JSON.stringify({
						            'message': null,
						            'images' : id_list,
						            'command': 'create_message'
						        }));
					    }).catch(function(error){
					    	console.error(error)
					    });		 				
		 			}
		 			else if (text_message != ''){
					   	commonRoomSocket.send(JSON.stringify({
					            'message': text_message,
					            'images' : id_list,
					            'command': 'create_message'
					        }));		 			
		 			}
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
		 			var inp = document.getElementById('images-input');
		 			var images = inp.files;
		 			if (images.length<=10){
		 				for (var i = 0; i < images.length; i++) {
			 				var reader = new FileReader();
			 			    reader.onload = function(e, i) {
			 			    	var place = $('.modal-img-exmp-place')[0];
			 			    	place.src = e.target.result;
			 			    	place.classList.remove("modal-img-exmp-place");
			 			    	place.classList.add("modal-img-exmp");
			 			    	place.style.maxWidth = '100%';
			 			    	place.style.minWidth = '100%';
						    }
							reader.readAsDataURL(inp.files[i], i);
						}
		 			}

		 		},
		 		activateImageLoadModal: function(){
		 			this.ImageLoadModal = true;
		 		},
		 		activateImagesInput: function(){
		 			document.getElementById('images-input').click();
		 		}
            }      
        };
</script>

<style>
</style>
