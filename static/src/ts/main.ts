import * as tree from './tree'
import { createApp } from 'vue';
import App from './components/App.vue';

tree.initTreePage()




const app = createApp(App)

app.mount("#app")


