<script lang="js">
import Vuex from 'vuex';

export default {
	name: 'Footer',
	computed: {
		...Vuex.mapState({
			appVersion(state) {
				return state.packageJson.version;
			},
		}),
	},
};
</script>

<template lang="pug">
div.content.has-text-right
	p.version
		a(href="https://github.com/khueue/khueue-diary") khueue-diary {{ appVersion }}
</template>

<style lang="scss" scoped>
.version {
	a {
		color: #ccc;
	}
}
</style>
