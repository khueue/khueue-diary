<script lang="js">
export default {
	name: 'Header',
	props: {
		user: {
			required: true,
		},
	},
	data() {
		return {};
	},
	methods: {
		signInWithGoogle() {
			this.$emit('sign-in-with-google');
		},
		signOut() {
			this.$emit('sign-out');
		},
	},
}
</script>

<template lang="pug">
.content.has-text-right
	transition(mode="out-in")
		button.button.is-primary(v-if="!user" @click="signInWithGoogle") Sign in
		button.button.is-primary(v-else @click="signOut") Sign out ({{ user.email }})
</template>

<style lang="scss" scoped></style>
