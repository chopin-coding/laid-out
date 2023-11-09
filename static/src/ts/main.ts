import { createApp } from "vue";
import App from "./components/App.vue";
import vClickOutside from "click-outside-vue3"


const app = createApp(App);
app.use(vClickOutside)
app.mount("#app");

