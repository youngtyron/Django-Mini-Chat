<template>
	<div class="row" style="margin-top: 10px;">	
        <div class="col-4">
            <ul class="list-group">
                <li class="list-group-item" v-for="added in added_users">
                    <p>
                        <div class="matched-users-avatar-div">
                            <img :src="added.avatar" alt="Avatar" class="matched-users-avatar-img">
                        </div>
                        {{added.first_name}} {{added.last_name}}
                        <i class="fas fa-times fa-2x cross-added-users" v-on:mouseover="emphasizeCross($event)"
                                                                        v-on:mouseout="hideCross($event)"
                                                                        @click='removeAdded(added)'></i>
                    </p>
                </li>
            </ul>
            <button v-if="added_users.length > 0" class="btn btn-black" @click='createChat' type="button">Create chat</button>
        </div>
		<div class='col-8'>
			<div class="user-search-div">
                <form action="">
                    <div class="form-group col-md-6">
                        <label for="userSearchInput">Type user name here</label>
                        <input type="text" id="userSearchInput" v-model="search_text" class="form-control" 
                                                              v-on:keypress='findOnTyping'>
                    </div>
                </form>
                <div>
                    <ul class="list-group">
                        <li class="list-group-item" v-for="matched in matched_users" @click='addUser(matched)'>
                            <p>
                                <div class="matched-users-avatar-div">
                                    <img :src="matched.avatar" alt="Avatar" class="matched-users-avatar-img">
                                </div>
                                {{matched.first_name}} {{matched.last_name}}
                            </p>
                        </li>
                    </ul>
                </div>
            </div>
		</div>
    </div>
</template>

<script>
    export default {
        data(){
            return  {
                search_text: '',
                matched_users: [],
                added_users: [],
            }
        },
        mounted() {
        },
        methods: {
                findOnTyping: function(){
                    var data = new URLSearchParams();
                    data.append('search', this.search_text);
                    axios.post('/chat/search_users/', data)
                        .then((response) => {
                            this.matched_users = response.data['matched_users']
                        });
                },
                addUser: function(choosen){
                    if (this.added_users.indexOf(choosen) != -1){
                        alert("You've added this user already")
                    }
                    else{
                        this.added_users.push(choosen)
                    }
                },
                emphasizeCross: function($event){
                    $event.target.style.opacity = '1';
                },
                hideCross: function($event){
                    $event.target.style.opacity = '0.3';
                },
                removeAdded: function(added){
                    this.added_users.splice(this.added_users.indexOf(added), 1);
                },
                createChat: function(){
                    var ids = new Array()
                    for (var i = 0; i < this.added_users.length; i++) {
                        ids.push(this.added_users[i].id)
                    }
                    this.added_users = []
                    var data = new URLSearchParams();
                    data.append('ids', ids);
                    axios.post('/chat/create_chat/', data)
                        .then((response) => {
                            var url = window.location.origin + '/chat/room/' + response.data['room_id'];
                            window.location.href= url;
                        });
                }
            }      
        };
</script>

<style>
</style>
