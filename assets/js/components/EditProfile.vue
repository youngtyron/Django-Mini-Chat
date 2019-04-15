<template>
	<div class="row">
		<p>EditProfileVue</p>
		<div class="col text-center">
			<div class="edit-profile-avatar-div">
				<img :src="avatar[0]" alt="Avatar" id="edit-profile-avatar-img">
			</div>
		</div>
    </div>
</template>

<script>
    export default {
    	props: ['user', 'avatar'],
        data(){
            return  {

            }
        },
        mounted() {

        },
        methods: {
 
            }      
        };
</script>

<style>
</style>
