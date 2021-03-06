import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode:'history',
    routes: [
        {
            path: '/',
            component: () => import('./components/Lectures.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              }
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
            component: () => import('./components/Profile.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              }
            
        },
        {
            path: '/chat/:id/',
            component: () => import('./components/Chat.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              },
            props: true
        },
        {
            path: '/chat',
            component: () => import('./components/Chat.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              },
        },
        {
            path: '/friends',
            component: () => import('./components/Friends.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              }
        },
        {
            path: '/lectures/:id/',
            component: () => import('./components/Lecture.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              }
        },
        {
            path: '/finance',
            component: () => import('./components/Finance.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              }
        },
        {
            path: '/diary',
            component: () => import('./components/Diary.vue'),
            beforeEnter: (to, from, next) => {
                status = localStorage.getItem('status')
                if(status != 'success')
                    next({ path: '/login' })
                else next()
              }
        },
    ]
})