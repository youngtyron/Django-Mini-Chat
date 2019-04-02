<template>
    <div>

        <p>MessagesBlock</p>
    	<li v-for="message in messages">
    		<p>{{message.author.first_name}} {{message.author.last_name}}</p>
    		<p>{{message.text}}</p>
    		<p>{{message.date}}</p>
    	</li>
    </div>
</template>

<script>
    export default {
    	props: ['room_id'],
        data(){
            return  {
            	messages: '',
            }
        },
        mounted() {
        	this.loadMessages()
        },
        methods: {
		 		loadMessages: function(){
		            axios.get('/chat/api/messages/'+this.room_id).then((response)=> {
			            this.messages = response.data;
		            });
		 		}
            }      
        };
</script>

<style>
</style>
