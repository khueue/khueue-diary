<script lang="js">
import firebase from '/js/firebase';
import db from '/js/firebase/db';

import DiaryPost from '/js/components/DiaryPost.vue';

export default {
	name: 'DiaryPostList',
	props: {
		user: {
			required: true,
		},
	},
	data() {
		return {
			currentUser: null,
			entries: [],
			unsubscriber: null,
			newEntry: null,
			isAuthoring: false,
		};
	},
	components: {
		DiaryPost,
	},
	watch: {
		user: {
			handler: function(newVal, oldVal) {
				console.log('watch:user', newVal);
				this.currentUser = newVal;
			},
		},
		currentUser: function(newVal, oldVal) {
			const self = this;
			console.log('old and new', oldVal, newVal);
			if (newVal) {
				console.log('GOING FOR IT');
				self.subscribeToFirestoreSnapshots();
			} else {
				self.unsubscribeToFirestoreSnapshots();
			}
		},
	},
	methods: {
		saveEntry(entry) {
			if (!entry.message) {
				this.deleteEntry(entry);
				return;
			}
			const self = this;
			const entriesColl = db.collection('diary').doc(self.currentUser.uid).collection('posts');
			if (entry.id) {
				entriesColl.doc(entry.id).set({
					message: entry.message,
					meta: entry.meta,
				}).then(function () {
					console.log('Set!');
				}).catch(function (error) {
					console.error(error);
				});
			} else {
				self.newEntry = null;
				entriesColl.add({
					message: entry.message,
					meta: entry.meta,
				}).then(function (doc) {
					console.log('Added!');
				}).catch(function (error) {
					console.error(error);
				});
			}
		},
		deleteEntry(entry) {
			if (!entry.id) {
				return;
			}
			const self = this;
			const entriesColl = db.collection('diary').doc(self.currentUser.uid).collection('posts');
			entriesColl.doc(entry.id).delete()
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
			console.log('currentUser', self.currentUser);
			const entriesColl = db.collection('diary').doc(self.currentUser.uid).collection('posts');
			self.unsubscriber = entriesColl.orderBy('meta.createdAt', 'asc').limit(100).onSnapshot(function(snapshot) {
				const entries = [];
				snapshot.forEach(function(snap) {
					const entry = self.newEntryFromSnapshot(snap);
					entries.push(entry);
				});
				self.entries = entries;
				console.log(self.entries.length);
			}, function (error) {
				console.log(error);
			});
		},
		unsubscribeToFirestoreSnapshots() {
			const self = this;
			if (self.unsubscriber) {
				self.unsubscriber();
			}
		},
		newEntryFromSnapshot(snap) {
			const entry = {};

			entry.id = snap.id;

			// Use auto-generated version timestamp to help Vue
			// decide whether to re-render.
			const version = snap._document.version.timestamp;
			entry.renderKey = `${snap.id}.${version.seconds}.${version.nanoseconds}`;

			entry.message = snap.data().message;

			entry.meta = snap.data().meta;

			return entry;
		},
	},
};
</script>

<template lang="pug">
.diary-post-list
	.wrapper(v-if="user")
		p(v-if="!entries.length") No entries!
		transition-group(v-else name="entry-list")
			DiaryPost(
				v-for="entry in entries"
				:key="entry.renderKey"
				:entry="entry"
				:user="currentUser"
				@save="saveEntry"
				@delete-entry="deleteEntry"
			)
	.p(v-else) Sign in!

	// .wrapper
	// 	DiaryPost(
	// 		v-show="isAuthoring"
	// 		:entry="newEntry"
	// 		@save="saveEntry"
	// 		@delete-entry="deleteEntry"
	// 		@cancel-post="cancelNewPost"
	// 	)
	// b-field(v-if="!isAuthoring")
	// 	button.button(@click="authorNewPost") New Post
</template>

<style lang="scss" scoped>
.entry-list-enter-active,
.entry-list-leave-active {
	transition: all 0.5s;
}
.entry-list-enter,
.entry-list-leave-to {
	opacity: 0;
	// transform: translateY(30px);
}
</style>
