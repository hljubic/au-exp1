import {createRouter, createWebHistory} from 'vue-router'

import Home from './views/Home.vue'
import Charts from './views/Charts.vue'
import Predict from './views/Predict.vue'

const routes = [
    {path: '/', component: Home},
    {path: '/charts', component: Charts},
    {path: '/predict', component: Predict}
]

const router = createRouter({history: createWebHistory(), routes})

export default router
