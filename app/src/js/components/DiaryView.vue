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
		h1.title.is-1 khueue.com
</template>

<style lang="scss" scoped></style>
