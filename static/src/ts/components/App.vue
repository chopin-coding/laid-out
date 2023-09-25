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

// async function printTreeData() {
//   while (true) {
//     console.log(tempTreeStore.value[0].treeName);
//     await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second
//   }
// }

// printTreeData();

let selectedTreeIndex = ref(0);

function selectTreeHandler(frontendTreeId: string): void {
  const indexToSelect = tempTreeStore.value.findIndex(
    (tree) => tree.frontendTreeId === frontendTreeId,
  );

  if (indexToSelect !== -1) {
    selectedTreeIndex.value = indexToSelect;
  }
}
</script>

<template>
  <div>
    <div>
      <component
        v-if="tempTreeStore.length !== 0"
        :is="TreeComponent"
        :tree-nodes="tempTreeStore[selectedTreeIndex].treeData"
      />
      <div v-else>No trees to show</div>
    </div>

    <div>
      <component
        :is="TreeListComponent"
        :trees="tempTreeStore"
        @select-tree="(frontendTreeId) => selectTreeHandler(frontendTreeId)"
      />
    </div>
  </div>
</template>
