<template>
	<div class="row">
		<div class="col text-center">
			<div class="edit-profile-avatar-div">
				<img :src="avatar[0]" alt="Avatar" id="edit-profile-avatar-img">
			</div>
			<p>{{firstname}}</p>
			<p>{{lastname}}</p>
			<button class="btn btn-avocado" @click='avatarInput'>Choice picture</button>
			<button class="btn btn-avocado" @click='sendNewAvatar'>Send picture</button>
			<form enctype="multipart/form-data" id="avatar-form">
				<input type="file" id="avatar-input" name="avatar-input" v-on:change="postInputFunc" class="form-control">
			</form>
		</div>
    </div>
</template>

<script>
    export default {
    	props: ['firstname', 'lastname', 'avatar'],
        data(){
            return  {
            	AvatarFormData: null,
            }
        },
        mounted() {

        },
        methods: {
        		sendNewAvatar: function(){
        			if (document.getElementById('avatar-input').files.length > 0){
        				this.AvatarFormData = new FormData(document.getElementById('avatar-form'));
						axios.post('/new_avatar/', this.AvatarFormData, {
					        headers: {
					          'Content-Type': 'multipart/form-data'
					        }}).then((response) => {
	 							document.getElementById('edit-profile-avatar-img').src = response.data['avatar_url'];
	                    	});
        			}
        		},
 				postInputFunc: function(){
		 			var inp = document.getElementById('avatar-input');
		 			var new_avatar = inp.files[0];
 					var reader = new FileReader();
	 			    reader.onload = function(e) {
	 			    	var place = document.getElementById('edit-profile-avatar-img');
	 			    	place.src = e.target.result;
				    }
					reader.readAsDataURL(new_avatar); 					
 				},
 				avatarInput: function(){
 					document.getElementById('avatar-input').click();
 				}
            }      
        };
</script>

<style>
</style>
