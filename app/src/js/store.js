import Vue from 'vue';
import Vuex from 'vuex';

import packageJson from '../../package.json';

Vue.use(Vuex);

const store = new Vuex.Store({
	// strict: process.env.NODE_ENV !== 'production',
	state: {
		packageJson: {
			version: packageJson.version,
		},
		user: null,
		posts: [],
	},
	getters: {
		user(state) {
			return state.user;
		},
		posts(state) {
			return state.posts;
		},
	},
	mutations: {
		setSignedInUser(state, payload) {
			state.user = payload.user;
		},
		clearSignedInUser(state) {
			state.user = null;
		},
		setPosts(state, payload) {
			state.posts = payload.posts;
		},
	},
	actions: {
	},
});

export default store;
