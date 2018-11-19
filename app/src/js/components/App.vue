<script lang="js">
import firebase from '/js/firebase';
import db from '/js/firebase/db';

import Header from '/js/components/Header.vue';
import Footer from '/js/components/Footer.vue';
import DiaryPostList from '/js/components/DiaryPostList.vue';

export default {
	name: 'App',
	data() {
		return {
			user: null,
		};
	},
	components: {
		Header,
		Footer,
		DiaryPostList,
	},
	created() {
		const self = this;
		firebase.auth().onAuthStateChanged(function(user) {
			self.user = null;
			if (user) {
				console.log('guser', user);
				self.user = {
					uid: user.uid,
					email: user.email,
					photoUrl: user.photoURL,
				};
			}
			console.log(self.user);
		});
	},
	methods: {
		signInWithGoogle() {
			var provider = new firebase.auth.GoogleAuthProvider();
			firebase.auth().signInWithPopup(provider);
		},
		signOut() {
			firebase.auth().signOut();
		},
	},
}
</script>

<template lang="pug">
#app
	.hero.is-fullheight
		.hero-head
			.navbar.is-fixed-top.is-transparent
				.navbar-menu
					.navbar-end
						Header(
							:user="user"
							@sign-in-with-google="signInWithGoogle"
							@sign-out="signOut"
						)
		.hero-body
			.container
				.columns.is-centered
					.column.is-three-quarters
						transition(name="view-fade" mode="out-in")
							router-view(
								:user="user"
							)
		.hero-foot
			.container
				.columns.is-centered
					.column.is-three-quarters
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
