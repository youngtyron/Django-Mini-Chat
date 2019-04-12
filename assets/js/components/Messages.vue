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
		    		<div class="message-flex-img-container">
 	   		    		<div class="message-flex-img-row">
		   		    		<div class="message-flex-img-col" v-for="image in message.images">
		    					<img :src="image" class="message-img" alt="Image">
		    				</div> 			
	    				</div> 		 		
		    		</div>
	        	</div>
	        	<div v-else>
		    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
		    		<p>{{message.text}}</p>
		    		<p>{{message.time}}</p>
		    		<p>{{message.date}}</p>
		    		<div class="message-flex-img-container">
 	   		    		<div class="message-flex-img-row">
		   		    		<div class="message-flex-img-col" v-for="image in message.images">
		    					<img :src="image" class="message-img" alt="Image">
		    				</div> 			
	    				</div> 		 		
		    		</div>
	        	</div>
	    	</li>
        </ul>
    	<form action="">
    		<div class="form-group col-md-6">
    			<input type="text" id="message-input" v-model="text_input" class="form-control">
    		</div>

    		<div class="form-group col-md-6">
    			<i class="fas fa-camera-retro fa-2x avocado-icon" @click="activateImagesInput"></i>
    			<button type="submit" class="btn btn-avocado" @click="sendMessage">Send</button>
    		</div>
		</form>
		<form enctype="multipart/form-data" id="images-form">
			<input type="file" id="images-input" name="images-input" v-on:change="postInputClick" class="form-control" multiple>
		</form>
		<div v-if="ImageLoadModal" class="modal-image-gallery-window text-center">
			<div class="modal-flex-img-container">
			  <div  v-for="i in 3" class="modal-flex-img-row">
				  <div v-for="i in 3" class="modal-flex-img-col">
				  	<img class="modal-img-exmp-place" src="" alt="">
				  </div>
			  </div>
			</div>
			<button id="attach-images-button" class="btn btn-avocado" type="button" @click="attachImages">Attach</button>
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
		 		preloadImagesGallery: function(images){
	 				for (var i = 0; i < images.length; i++) {
		 				var reader = new FileReader();
		 			    reader.onload = function(e, i) {
		 			    	var place = $('.modal-img-exmp-place')[0];
		 			    	place.src = e.target.result;
		 			    	place.classList.remove("modal-img-exmp-place");
		 			    	place.classList.add("modal-img-exmp");
		 			    	place.style.maxWidth = '80%';
		 			    	place.style.minWidth = '80%';
					    }
						reader.readAsDataURL(images[i], i);
					}
		 		},
		 		postInputClick: function(){
		 			var inp = document.getElementById('images-input');
		 			var images = inp.files;
		 			if (images.length>9){
		 				document.getElementById('images-input').files = null;
		 				alert("You can't attach more than 9 pictures");
		 			}
		 			else{
		 				console.log('click')
		 				this.ImageLoadModal = true;
		 				this.preloadImagesGallery(images);
		 			}
		 		},
		 		activateImagesInput: function(){
		 			document.getElementById('images-input').click();
		 		},
		 		attachImages: function(){
					this.ImagesFormData = new FormData(document.getElementById('images-form'))
					this.ImageLoadModal = false
		 		}
            }      
        };
</script>

<style>
</style>
