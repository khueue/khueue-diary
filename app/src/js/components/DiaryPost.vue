<script lang="js">
import * as moment from 'moment';
import showdown from 'showdown';

const converter = new showdown.Converter();

export default {
	name: 'DiaryPost',
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
		messageAsHtml() {
			return converter.makeHtml(this.message);
		},
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
div.diary-post
	div.card
		div.card-content
			div.viewing(v-if="!isEditing" @dblclick="edit")
				div.markdown-to-html(v-html="messageAsHtml")
			div.editing(v-else)
				div.field
					div.control
						textarea.textarea(
							v-model="draftMessage"
							v-focus="true"
							@keyup.esc="cancelEdit"
							@keyup.ctrl.enter="save"
						) {{ draftMessage }}
				div.field
					div.control
						button.button.is-primary(@click="save") Save
						button.button(@click="cancelEdit") Cancel
						button.button.is-danger.is-pulled-right(v-if="hasDatabaseId" @click="deleteEntry") Delete
		div.card-footer.is-size-7
			div.card-footer-item
				div.media
					div.media-left
						figure.image.is-48x48
							img.is-rounded(:src="this.$store.state.user.photoURL")
			div.card-footer-item
				p {{ createdAtPretty }}
			div.card-footer-item(v-show="hasBeenEdited")
				p(:title="updatedAtPretty") (updated: {{ updatedAtRelative }})
</template>

<style lang="scss">
.diary-post {
	.markdown-to-html {
		h1,
		h2,
		h3,
		h4,
		h5,
		h6,
		ul,
		ol,
		p,
		pre {
			margin-bottom: 1rem;
		}
		h1 {
			font-size: x-large;
		}
	}
}
</style>

<style lang="scss" scoped>
.card {
	margin-bottom: 1.5rem;
}
.card-footer {
	margin-top: -1rem;
}
.textarea {
	height: 15rem;
}
</style>
