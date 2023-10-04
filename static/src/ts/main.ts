import { createApp } from "vue";
import App from "./components/App.vue";
import { axiosGetTrees } from "./treeHelpers"

const app = createApp(App);

app.mount("#app");

const receivedTrees = axiosGetTrees()
console.log(receivedTrees)

