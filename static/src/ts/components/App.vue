<script setup lang="ts">
import { ref, reactive } from "vue";
import * as treeHelpers from "../treeHelpers";
import { useStorage } from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TreeListComponent from "./TreeListComponent.vue";

const loggedIn = false;

let tempTreeStore = ref([]);

if (loggedIn) {
  // some stuff
} else {
  tempTreeStore.value.push(treeHelpers.defaultTree());
}
</script>

<template>
  <div>
    <div>
      <component
        :is="TreeComponent"
        :treeNodes="tempTreeStore[0].treeData"
      />
    </div>

    <div>
      <component :is="TreeListComponent" :trees="tempTreeStore" />
    </div>
  </div>
</template>