<template>
	<div class="row">
		<div class="col">
			<div class="left-block">
				<div v-for="user in visible_users">
					<p>
						<div class="chat-member-list-avatar-div">
							<img :src="user.avatar" alt="Avatar" class="chat-member-list-avatar-img">
						</div>
						{{user.first_name}} {{user.last_name}}
					</p>
				</div>
				<a href="" v-if="visible_users_start + 5 <= users.length" @click='showMoreUsers'>Show more</a>
				<a href="" v-else @click='backToFirst'>Back to first</a>
			</div>
		</div>
		<div class="col-7" style='display: flex; justify-content:center;  align-items:stretch;'>
			<div class="messages-block">
				<div class="one-message-block" 
						v-bind:class="{not_read: message.not_read}"
			        	v-for="message in messages">
					<div class="message-exemp-div" 
						v-bind:class="{my_message_block: message.mine, another_message_block: !message.mine}" v-if="message.need_update" v-on:mouseover="readMessages">
				    		<p>{{message.author.first_name}}</p>
				    		<p>{{message.text}}</p>
				    		<p>{{message.date}}</p>
				    		<div class="message-flex-img-container">
		 	   		    		<div class="message-flex-img-row">
				   		    		<div class="message-flex-img-col" v-for="image in message.images">
				    					<img :src="image" class="message-img" alt="Image" @click='openInGallery(image, message.images)'>
				    				</div> 			
			    				</div> 		 		
				    		</div>
			        </div>
			        <div class="message-exemp-div" v-bind:class="{my_message_block: message.mine, another_message_block: !message.mine}" v-else>
			    		<p>{{message.author.first_name}}</p>
			    		<p>{{message.text}}</p>
			    		<p>{{message.date}}</p>
			    		<div class="message-flex-img-container">
	 	   		    		<div class="message-flex-img-row">
			   		    		<div class="message-flex-img-col" v-for="image in message.images">
			    					<img :src="image" class="message-img" alt="Image"  @click='openInGallery(image, message.images)'>
			    				</div> 			
		    				</div> 		 		
			    		</div>
		        	</div>
				</div>
			</div>
	        <div class="form-div">
		        <form action="">
		    		<div class="form-group col-md-6 message-input-div">
		    			<input type="text" id="message-input" v-model="text_input" class="form-control text-center" 
		    												  v-on:keypress='translateTyping(); keyPressTracking(7000)'>
		    		</div>

		    		<div class="form-group col-md-6 send-and-add-picture">
		    			<i class="fas fa-camera-retro fa-2x" @click="activateImagesInput"></i>
		    			<button type="submit" id="send-message" class="btn btn-black" @click="sendMessage">Send</button>
		    		</div>
				</form>
				<form enctype="multipart/form-data" id="images-form">
					<input type="file" id="images-input" name="images-input" v-on:change="postInputClick" class="form-control" multiple>
				</form>
				<p v-model='typing_notif'>{{typing_notif}}</p>
	        </div>
	    	
			<div v-if="ImageLoadModal" class="modal-image-gallery-window text-center">
				<div class="modal-flex-img-container">
				  <div  v-for="i in 3" class="modal-flex-img-row">
					  <div v-for="i in 3" class="modal-flex-img-col">
					  	<img class="modal-img-exmp-place" src="" alt="">
					  </div>
				  </div>
				</div>
				<button id="attach-images-button" class="btn btn-black" type="button" @click="attachImages">Attach</button>
			</div>

			<div v-if="addMemberModal" class="modal-add-member-window text-center">
				<form action="" class="add-member-form">
                    <div class="form-group col-md-6 add-member-input">
                        <label for="userSearchInput">Type user name here</label>
                        <input type="text" id="memberSearchInput" v-model="search_member" class="form-control" 
                                                              v-on:keypress='findMemberOnTyping'>
                    </div>
                </form>
                <div  v-if='potential_members.length>0'>
                    <ul class="list-group">
                        <li class="list-group-item" v-for="potential in potential_members" @click='addMember(potential.id)'>
                            <p>
                                <div class="matched-users-avatar-div">
                                    <img :src="potential.avatar" alt="Avatar" class="matched-users-avatar-img">
                                </div>
                                {{potential.first_name}} {{potential.last_name}}
                            </p>
                        </li>
                    </ul>
                </div>
			</div>

			<div v-if="galleryModal" class="gallery-modal text-center">
				<div class="i-left-arrow">
					<i class="fas fa-arrow-circle-left fa-3x" @click="previousImage"></i>				
				</div>
				<div class="img-in-gallery">
					<div class="img-in-gallery-sub">
						<img :src="opened_img" alt="Image" class="opened-img">					
					</div>
				</div>
				<div class="i-right-arrow">
					<i class="fas fa-arrow-circle-right fa-3x" @click="nextImage"></i>					
				</div>
			</div>

		</div>
		<div class="col">
			<div class="right-block">
				<nav class="nav flex-column">
				  <a class="nav-link  above-chat-link" @click='leaveChat' href="#"><i class="fas fa-door-open fa-2x"></i>Leave chat</a>
				  <a class="nav-link  above-chat-link"  @click='openAddMember' href="#"><i class="fas fa-user-plus fa-2x"></i>Add user</a>
				</nav>
			</div>


		</div>
    </div>
</template>

<script>
    export default {
    	props: ['room_id'],
        data(){
            return  {
            	visible_users: [],
            	visible_users_start: null,
            	users: [],
            	messages: [],
            	raw_messages: [],
            	text_input: '',
            	images_input: '',
            	commonRoomSocket: null,
            	counter: 0,
            	ImagesFormData: null,
            	ImageLoadModal: false,
            	typers: [],
            	typing_notif: '',
            	addMemberModal: false,
            	potential_members: [],
            	search_member: '',
            	galleryModal: false,
            	opened_img: null,
            	gallery_images: [],
            }
        },
        mounted() {
        	this.getUsers();
        	this.commonRoomSocket = new WebSocket(
		        'ws://' + window.location.host +'/ws/chat/' + this.room_id + '/');
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
		    	else if (data['user_is_typing']){
			    	var user_name = data['user_is_typing'];
			    	if(this.typers.indexOf(user_name)==-1){
			    		this.typers.push(user_name);
			    		this.typing_notif =  '';
				    	for (var i = 0; i < this.typers.length; i++) {
				    		if (i!= this.typers.length-1){
				    			this.typing_notif = this.typing_notif + this.typers[i] + ', '
				    		}
				    		else{
				    			this.typing_notif = this.typing_notif + this.typers[i]
				    		}
				    	}
				    	if (this.typers.length == 1){
				    		this.typing_notif = this.typing_notif + ' types a message...'
				    	}
				    	else if (this.typers.length>1){
				    		this.typing_notif = this.typing_notif + ' type a message...'
				    	}			    		
			    	}
		    	}
		    	else if (data['user_stopped_typing']){
			    	var user_name = data['user_stopped_typing'];
			    	this.typers.splice(this.typers.indexOf(user_name), 1);
	    			this.typing_notif =  '';
				    for (var i = 0; i < this.typers.length; i++) {
			    		if (i!= this.typers.length-1){
			    			this.typing_notif = this.typing_notif + this.typers[i] + ', '
			    		}
			    		else{
			    			this.typing_notif = this.typing_notif + this.typers[i]
			    		}
				    }
			    	if (this.typers.length == 1){
			    		this.typing_notif = this.typing_notif + ' types a message...'
			    	}
			    	else if (this.typers.length>1){
			    		this.typing_notif = this.typing_notif + ' type a message...'
			    	}	
		    	}
		    	else if (data['new_member']){
					this.users.push(data['new_member']);
		    	}
		    	else if (data['leave_chat']){
		    		for (var i = 0; i < this.users.length; i++) {
		    			if (this.users[i].id == data['leave_chat'].id){
		    				this.users.splice(i, 1);
		    				break;
		    			}
		    		}
					alert(data['leave_chat'].first_name + ' ' + data['leave_chat'].last_name + ' left this chat');
		    	}
		  	});
			window.addEventListener('keydown', this.keyListener);
			window.addEventListener('scroll', this.scrollMessages);
			window.addEventListener('click', (e)=> {
				if (this.galleryModal==true){
					var img = document.getElementsByClassName('opened-img')[0]
					if(e.target!=img && e.target.className!='fas fa-arrow-circle-left fa-3x' 
						&& e.target.className!='fas fa-arrow-circle-right fa-3x' && e.target.className!='message-img'){
						this.galleryModal = false;
						this.opened_img = null;
						this.gallery_images = [];	
					}
				}
			});			
		},
        methods: {
        		getUsers: function(){
				   	axios.get('/chat/get_users/' + this.room_id + '/').then((response) => {
 						this.users = response.data['users'];
 						this.visible_users = this.users.slice(0, 5);
 						this.visible_users_start = 0;
                    });
        		},
        		showMoreUsers: function(e){
        			e.preventDefault();
        			this.visible_users_start = this.visible_users_start + 5;
        			var end = this.visible_users_start + 5;
        			this.visible_users = this.users.slice(this.visible_users_start, end);
        		},
        		backToFirst: function(e){
        			e.preventDefault();
					this.visible_users = this.users.slice(0, 5);
					this.visible_users_start = 0;       			
        		},
        		scrollMessages: function(){
        			var sctop =  document.documentElement.scrollTop;
        			if (sctop == 0){
	        			this.commonRoomSocket.send(JSON.stringify({
					        'counter': this.counter,
					        'command': 'get_messages'
					    }));
        			}
        		},
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
		 			else if (key==27 && this.galleryModal==true){
		 				this.galleryModal = false;
						this.opened_img = null;
						this.gallery_images = [];			
		 			}
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
		 		},
		 		stopTypeTracking: function(){
	 				this.commonRoomSocket.send(JSON.stringify({
			   			'command': 'stoptyping'
			        }));
		 		},
		 		keyPressTracking: function(timer){
					var text_area = document.getElementById('message-input');
		 			window.clearTimeout(timer);
					timer = setTimeout(this.stopTypeTracking, 7000);
		 		},
		 		translateTyping: function(){
	 				this.commonRoomSocket.send(JSON.stringify({
			   			'command': 'typing'
			        }));
		 		},
		 		leaveChat: function(){
   					this.commonRoomSocket.send(JSON.stringify({
			            'command': 'leave_chat'
			        }));	
                    window.location.href= window.location.origin;
		 		},
		 		openAddMember: function(){
		 			this.addMemberModal = true;
		 		},
		 		findMemberOnTyping: function(){
		 			var data = new URLSearchParams();
                    data.append('search', this.search_member);
                    axios.post('/chat/potential_members/' + this.room_id + '/', data)
                        .then((response) => {
	 						this.potential_members = response.data['potential_members'];
                        });
		 		},
		 		addMember: function(potential_id){
					this.commonRoomSocket.send(JSON.stringify({
			            'potential_id': potential_id,
			            'command': 'new_member'
			        }));	
			        this.addMemberModal = false
		 		},
		 		openInGallery: function(this_image, images){
		 			this.opened_img = this_image;
		 			this.gallery_images = images
		 			this.galleryModal = true;
		 		},
		 		nextImage: function(){
		 			var index = this.gallery_images.indexOf(this.opened_img);
		 			if (index + 1 == this.gallery_images.length){
		 				var new_index = 0;
		 			}
		 			else{
		 				var new_index = index + 1;
		 			}
		 			this.opened_img = this.gallery_images[new_index];
		 		},
		 		previousImage: function(){
		 			var index = this.gallery_images.indexOf(this.opened_img);
		 			if (index == 0){
		 				var new_index = this.gallery_images.length - 1;
		 			}
		 			else{
		 				var new_index = index - 1;
		 			}
		 			this.opened_img = this.gallery_images[new_index];
		 		},	 			 		
            }      
        };
</script>

<style>
</style>
