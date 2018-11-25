import Vue from 'vue';
import VueRouter from 'vue-router';

import DiaryView from '/js/components/DiaryView.vue';

Vue.use(VueRouter);

const router = new VueRouter({
	mode: 'history',
	routes: [
		{
			path: '/',
			component: DiaryView,
		},
		{
			path: '*',
			redirect: '/',
		},
	],
});

export default router;
