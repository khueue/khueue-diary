<script lang="js">
import Vuex from 'vuex';

export default {
	name: 'Footer',
	computed: {
		...Vuex.mapGetters([
			'user',
		]),
		...Vuex.mapState({
			appVersion(state) {
				return state.packageJson.version;
			},
		}),
	},
};
</script>

<template lang="pug">
div.content
	p.version(v-if="user")
		a(href="https://github.com/khueue/khueue-diary") khueue-diary {{ appVersion }}
</template>

<style lang="scss" scoped>
.version {
	a {
		color: #ccc;
	}
}
</style>
