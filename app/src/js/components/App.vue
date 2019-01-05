<script lang="js">
import Vuex from 'vuex';

import firebase from '/js/firebase';
import db from '/js/firebase/db';

import Header from '/js/components/Header.vue';
import Footer from '/js/components/Footer.vue';

export default {
	name: 'App',
	components: {
		Header,
		Footer,
	},
	computed: {
		...Vuex.mapGetters([
			'user',
		]),
	},
	created() {
		const self = this;
		firebase.auth().onAuthStateChanged(function(user) {
			if (user) {
				self.$store.commit({
					type: 'setSignedInUser',
					user: user,
				});
			} else {
				self.$store.commit({
					type: 'clearSignedInUser',
				});
			}
			console.log(self.user);
		});
	},
	methods: {
		signInWithGoogle() {
			const provider = new firebase.auth.GoogleAuthProvider();
			firebase.auth().signInWithPopup(provider);
		},
		signOut() {
			firebase.auth().signOut();
		},
	},
}
</script>

<template lang="pug">
div#app
	div.hero.is-fullheight
		div.hero-head
			div.navbar.is-fixed-top.is-transparent
				div.navbar-menu
					div.navbar-end
						Header(
							@sign-in-with-google="signInWithGoogle"
							@sign-out="signOut"
						)
		div.hero-body
			div.container
				div.columns.is-centered
					div.column.is-three-quarters
						transition(name="view-fade" mode="out-in")
							router-view
		div.hero-foot
			div.container
				div.columns.is-centered
					div.column.has-text-centered
						Footer
</template>

<style lang="scss" scoped>
.hero {
	.navbar {
		padding: 1rem;
	}
}

.view-fade-enter-active,
.view-fade-leave-active {
	transition: opacity 0.15s ease;
}
.view-fade-enter,
.view-fade-leave-to {
	opacity: 0;
}
</style>
