import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode:'history',
    routes: [
        {
            path: '/',
            component: () => import('./components/Home.vue')
        },
        {
            path: '/login',
            component: () => import('./components/Login.vue')
        },
        {
            path: '/registration',
            component: () => import('./components/Registration.vue')
        },
        {
            path: '/profile',
            component: () => import('./components/Profile.vue')
        }
    ]
})