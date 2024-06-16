import 'ant-design-vue/dist/reset.css'
import './assets/scss/main.scss'

import { createApp } from 'vue'

import App from './App.vue'

// ant-design
import Antd from 'ant-design-vue'

const app = createApp(App)

app.use(Antd)

app.mount('#app')
