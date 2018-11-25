<script lang="js">
import Vuex from 'vuex';

import DiaryPostList from '/js/components/DiaryPostList.vue';

export default {
	name: 'DiaryView',
	components: {
		DiaryPostList,
	},
	computed: {
		...Vuex.mapGetters([
			'user',
		]),
	},
};
</script>

<template lang="pug">
div.diary-view
	DiaryPostList(v-if="user")
	div.has-text-centered(v-else)
		p You are currently signed out!
</template>

<style lang="scss" scoped></style>
