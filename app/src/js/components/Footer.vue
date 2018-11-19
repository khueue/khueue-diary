<script lang="js">
import pkg from '../../../package.json';

export default {
	data() {
		return {
			appVersion: pkg.version,
		};
	},
}
</script>

<template lang="pug">
.content.has-text-right
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
