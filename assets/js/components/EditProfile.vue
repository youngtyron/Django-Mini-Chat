<template>
	<div class="row">
		<div class="col text-center">
			<p class="subtitle">{{firstname}} {{lastname}}</p>
			<ul class="list-group">
				<li class="list-group-item" @click='avatarInput'>
					<div class="edit-profile-avatar-div">
						<img :src="avatar[0]" alt="Avatar" id="edit-profile-avatar-img">
					</div>
				</li>
				<li class="list-group-item" v-if='clungPhoto' @click='sendNewAvatar'>
					<p style='font-weight: bold; color: #000066;'>Update</p>
				</li>
				<li class="list-group-item" v-else @click='avatarInput'>
					<p style='font-weight: bold; color: #000066;'>New Profile Photo</p>
				</li>
				<li class="list-group-item" @click=''>
					<p style='font-weight: bold; color: #000066;'>{{city}}</p>
				</li>
				<li class="list-group-item" @click=''>
					<p style='font-weight: bold; color: #000066;'>{{birthday}}</p>
				</li>
				<li class="list-group-item" @click='deleteAccount'>
					<p style='font-weight: bold; color: #000066;'>You can delete your account</p>
				</li>
			</ul>
			<form enctype="multipart/form-data" id="avatar-form">
				<input type="file" id="avatar-input" name="avatar-input" v-on:change="postInputFunc" class="form-control">
			</form>
		</div>
    </div>
</template>

<script>
    export default {
    	props: ['firstname', 'lastname', 'avatar', 'city', 'birthday'],
        data(){
            return  {
            	AvatarFormData: null,
            	clungPhoto: false,
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
	 							this.clungPhoto = false;		
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
					this.clungPhoto = true;				
 				},
 				avatarInput: function(){
 					document.getElementById('avatar-input').click();
 				},
 				deleteAccount: function(){
 					if (confirm("Are you sure? You wouldn't be able to cancel it.")){
 						axios.post('/delete_account/').then((response) => {
	 							if (response.data['success'] == true){
	 								window.location.href = window.location.origin;
	 							}
	                    	});
 					}
 				}
            }      
        };
</script>

<style>
</style>
