import { createApp } from "vue";
import App from "./components/App.vue";
import { getTrees } from "./treeHelpers"

const app = createApp(App);

app.mount("#app");

