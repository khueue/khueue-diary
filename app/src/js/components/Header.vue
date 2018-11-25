<script lang="js">
import Vuex from 'vuex';

export default {
	name: 'Header',
	computed: {
		...Vuex.mapGetters([
			'user',
		]),
	},
	methods: {
		signInWithGoogle() {
			this.$emit('sign-in-with-google');
		},
		signOut() {
			this.$emit('sign-out');
		},
	},
};
</script>

<template lang="pug">
div.content.has-text-right
	transition(mode="out-in")
		div.buttons(v-if="!user")
			a.button.is-primary(@click="signInWithGoogle")
				span.icon
					i.fas.fa-sign-in-alt
				span Sign in
		div.buttons(v-else)
			a.button(@click="signOut")
				span.icon
					i.fas.fa-sign-out-alt
				span Sign out ({{ user.email }})
</template>

<style lang="scss" scoped></style>
