<script lang="js">
import Vuex from 'vuex';

import firebase from '/js/firebase';
import db from '/js/firebase/db';

import DiaryPost from '/js/components/DiaryPost.vue';

export default {
	name: 'DiaryPostList',
	components: {
		DiaryPost,
	},
	data() {
		return {
			unsubscriber: null,
			newEntry: null,
			isAuthoring: false,
			postsCollection: null,
		};
	},
	created() {
		this.subscribeToFirestoreSnapshots();
	},
	beforeDestroy() {
		this.unsubscribeToFirestoreSnapshots();
	},
	computed: {
		...Vuex.mapGetters([
			'user',
			'posts',
		]),
	},
	methods: {
		savePost(entry) {
			if (!entry.message) {
				this.deletePost(entry);
				return;
			}
			const self = this;
			if (entry.id) {
				self.postsCollection
				.doc(entry.id)
				.set({
					message: entry.message,
					meta: entry.meta,
				}).then(function () {
					console.log('Set!');
				}).catch(function (error) {
					console.error(error);
				});
			} else {
				self.newEntry = null;
				self.postsCollection
				.add({
					message: entry.message,
					meta: entry.meta,
				}).then(function (doc) {
					console.log('Added!');
				}).catch(function (error) {
					console.error(error);
				});
			}
		},
		deletePost(entry) {
			if (!entry.id) {
				return;
			}
			const self = this;
			self.postsCollection
			.doc(entry.id)
			.delete()
			.then(function () {
				console.log('Deleted!');
			}).catch(function (error) {
				console.error(error);
			});
		},
		cancelNewPost(entry) {
			const self = this;
			self.isAuthoring = false;
		},
		authorNewPost() {
			const self = this;
			self.isAuthoring = true;
			if (!self.newEntry) {
				self.newEntry = {
					meta: {},
					isEditing: true,
					message: null,
				};
			}
		},
		subscribeToFirestoreSnapshots() {
			const self = this;
			self.postsCollection = db.collection('diary').doc(self.user.uid).collection('posts');
			self.unsubscriber = self.postsCollection
			.orderBy('meta.createdAt', 'desc')
			.limit(20)
			.onSnapshot(function(snapshot) {
				const newPosts = [];
				snapshot.forEach(function(snap) {
					const newPost = self.newPostFromSnapshot(snap);
					newPosts.push(newPost);
				});
				console.log(newPosts);
				self.$store.commit({
					type: 'setPosts',
					posts: newPosts,
				});
			}, function (error) {
				console.error(error);
			});
		},
		unsubscribeToFirestoreSnapshots() {
			const self = this;
			if (self.unsubscriber) {
				self.unsubscriber();
				self.postsCollection = null;
			}
		},
		newPostFromSnapshot(snap) {
			const post = {};

			post.id = snap.id;

			// Use auto-generated version timestamp to help Vue
			// decide whether to re-render.
			const version = snap._document.version.timestamp;
			post.renderKey = `${snap.id}.${version.seconds}.${version.nanoseconds}`;

			post.message = snap.data().message;

			post.meta = snap.data().meta;

			return post;
		},
	},
};
</script>

<template lang="pug">
div.diary-post-list
		p(v-if="!posts.length") No entries!
		transition-group(v-else name="entry-list")
			DiaryPost(
				v-for="post in posts"
				:key="post.renderKey"
				:entry="post"
				@save="savePost"
				@delete-entry="deletePost"
			)
</template>

<style lang="scss" scoped>
.entry-list-enter-active,
.entry-list-leave-active {
	transition: all 0.5s;
}
.entry-list-enter,
.entry-list-leave-to {
	opacity: 0;
}
</style>
