<template>
	<div class="row" style="margin-top: 10px;">	
		<div class='col-6'>
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
                        <li class="list-group-item" v-for="matched in matched_users">
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
        <div class="col-6">
            
        </div>
    </div>
</template>

<script>
    export default {
        data(){
            return  {
                search_text: '',
                matched_users: [],
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
                            console.log(response.data)
                        }).catch((error)=>{
                            console.log(error)
                        });
                }
            }      
        };
</script>

<style>
</style>
