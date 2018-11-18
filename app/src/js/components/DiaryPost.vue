<script lang="js">
import * as moment from 'moment';

export default {
	props: {
		entry: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			...this.entry,
			isEditing: !this.entry.id,
			draftMessage: this.entry.message,
		};
	},
	computed: {
		hasDatabaseId() {
			return !!this.id;
		},
		hasBeenEdited() {
			return this.meta.createdAt !== this.meta.updatedAt;
		},
		updatedAtRelative() {
			return moment.utc(this.meta.updatedAt).fromNow();
		},
		updatedAtPretty() {
			return moment.utc(this.meta.updatedAt).format('YYYY-MM-DD HH:mm');
		},
		createdAtPretty() {
			return moment.utc(this.meta.createdAt).format('YYYY-MM-DD HH:mm');
		},
	},
	methods: {
		edit() {
			this.isEditing = true;
		},
		cancelEdit() {
			this.isEditing = false;
			this.$emit('cancel-post', this);
		},
		save() {
			this.isEditing = false;
			this.message = this.draftMessage.trim();
			const now = moment.utc().format();
			if (!this.meta.createdAt) {
				this.meta.createdAt = now;
			}
			this.meta.updatedAt = now;
			this.$emit('save', this);
		},
		deleteEntry() {
			this.$emit('delete-entry', this);
		},
	},
	directives: {
		focus: {
			inserted(el) {
				el.focus();
			}
		},
	},
};
</script>

<template lang="pug">
	.card
		.card-content
			.column(v-on:dblclick="edit")
				.viewing(v-if="!isEditing")
					p {{ message }}
				.editing(v-else)
					.field
						.control
							textarea.textarea(v-model="draftMessage" v-focus="true" @keyup.esc="cancelEdit") {{ draftMessage }}
					.field
						.control
							button.button.is-primary(@click="save") Save
							button.button(@click="cancelEdit") Cancel
							button.button.is-danger.is-pulled-right(v-if="hasDatabaseId" @click="deleteEntry") Delete
		.card-footer
			.card-footer-item
				p {{ createdAtPretty }}
			.card-footer-item(v-show="hasBeenEdited")
				p(v-show="hasBeenEdited" :title="updatedAtPretty") (updated: {{ updatedAtRelative }})
</template>

<style lang="scss" scoped>
.card {
	margin-bottom: 20px;
}
</style>
