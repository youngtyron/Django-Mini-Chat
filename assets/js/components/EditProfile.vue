<template>
	<div class="row">
		<div class="col text-center">
			<ul class="list-group" style='margin-top: 15%;'>
				<p class="subtitle">{{firstname}} {{lastname}}</p>
				<li v-if='clungPhoto' class="list-group-item" @click='avatarInput'>
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
				<li class="list-group-item">
					<div v-if="edit_city_open">
						<form action="">
							<div class="form-group col-md-6" style="margin: 0 auto; width: 100%">
			                    <input type="text" id="editCityInput" v-model="edited_city" class="form-control" style='width:70%; float: left; margin-right: 10px;'>
			                    <button class="btn btn-white" @click='updateCity' style='width:20%; float: right; margin-left: 10px;'>Update</button>						
			                </div>
			            </form>	
					</div>
					<div v-else>
						<p style='font-weight: bold; color: #000066;'>{{city}}
						<button class="btn btn-white"  @click='openEditCity'>Edit</button></p>
					</div>
				</li>
				<li class="list-group-item">
					<div v-if="edit_birthday_open">
						<form action="">
							<div class="form-group col-md-6 text-center" style="margin: 0 auto; width: 100%">
			                    <input type="date" id="editBirthdayInput" v-model="edited_birthday" class="form-control" style='width:70%; float: left; margin-right: 10px;'>
			                    <button class="btn btn-white" @click='updateBirthday' style='width:20%; float: right; margin-left: 10px;'>Update</button>						
			                </div>
			            </form>	
					</div>
					<div v-else>
						<p style='font-weight: bold; color: #000066;'>{{birthday}}
						<button class="btn btn-white"  @click='openEditBirthDay'>Edit</button></p>				
					</div>
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
            	edit_city_open: false,
            	edited_city: '',
            	edit_birthday_open: false,
            	edited_birthday: '',
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
 				},
 				openEditCity: function(){
 					this.edit_city_open = true;
 				},
 				updateCity: function(e){
 					e.preventDefault();
 					var data = new URLSearchParams();
                    data.append('city', this.edited_city);
					axios.post('/update_city/', data).then((response) => {
 							this.city = response.data['city'];
 							this.edit_city_open = false;		
 							this.edited_city = '';
                    	});
 				},
 				openEditBirthDay: function(){
 					this.edit_birthday_open = true;
 				},
 				updateBirthday: function(e){
 					e.preventDefault();
 					var data = new URLSearchParams();
 					data.append('birthday', this.edited_birthday);
					axios.post('/update_birthday/', data).then((response) => {
						this.birthday = response.data['birthday'];
						this.edit_birthday_open = false;		
						this.edited_birthday = '';
        			});			
 				},
            }      
        };
</script>

<style>
</style>
