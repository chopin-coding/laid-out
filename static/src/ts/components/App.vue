<script setup lang="ts">
import { ref } from "vue";
import * as treeHelpers from "../treeHelpers";
import { useStorage } from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TreeListComponent from "./TreeListComponent.vue";

const loggedIn = JSON.parse(document.getElementById("logged-in").textContent);
const userTrees = JSON.parse(document.getElementById("user-trees").textContent);

let tempTreeStore = ref([]);

if (loggedIn) {
  tempTreeStore.value.push.apply(tempTreeStore.value, userTrees)
} else {
  tempTreeStore.value.push(treeHelpers.defaultTree());
}

let selectedTreeIndex = ref(0);

function selectTreeHandler(treeId: string): void {
  const indexToSelect = tempTreeStore.value.findIndex(
    (tree) => tree.tree_id === treeId,
  );

  if (indexToSelect !== -1) {
    selectedTreeIndex.value = indexToSelect;
  }
}
</script>

<template>
  <div>
    <div>
      <div>
        <label for="selected-tree-name-input">Tree Name</label>
        <input
          id="selected-tree-name-input"
          v-model="tempTreeStore[selectedTreeIndex].tree_name"
        />
      </div>
      <component
        v-if="tempTreeStore.length !== 0"
        :is="TreeComponent"
        :tree-nodes="tempTreeStore[selectedTreeIndex].tree_data"
      />
      <div v-else>No trees to show</div>
    </div>

    <div>
      <component
        :is="TreeListComponent"
        :trees="tempTreeStore"
        @select-tree="(treeId: string) => selectTreeHandler(treeId)"
      />
    </div>
  </div>
</template>
