<template>
	<div class="row">	
		<div class='col-8 chats-list-div'>
			<ul class="list-group">
				<li v-for="room in rooms" class="list-group-item">
					<a v-bind:href="'/chat/room/' + room.id"><p>{{room.title_name}}</p></a>
					<div class="not_read" v-if="room.last_message_title" 
										  v-bind:class="{not_read: room.last_message_title.not_read}">
						<p>
						<div class="chat-member-list-avatar-div">
							<img v-bind:src="room.last_message_title.author.avatar" alt="Avatar" class="chat-title-message-avatar-img">
						</div>
						{{room.last_message_title.author.first_name}} {{room.last_message_title.author.last_name}}
						</p>
						<p>{{room.last_message_title.title_text}}</p>						
					</div>
				  	<div v-else>
						<p>There is not any messages</p>
				  	</div>		
				</li>
			</ul>
		</div>
    </div>
</template>

<script>
    export default {
        data(){
            return  {
            	rooms: [],
            }
        },
        mounted() {
        	this.getRooms();
        },
        methods: {
        		getRooms: function(){
        			axios.get('/chat/get_rooms/').then((response) => {
 						this.rooms = response.data['rooms'];
                    });
        		}
            }      
        };
</script>

<style>
</style>
