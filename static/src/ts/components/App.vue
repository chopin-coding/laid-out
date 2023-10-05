<script setup lang="ts">
import { ref, watch } from "vue";
import * as treeHelpers from "../treeHelpers";
import { useStorage } from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TreeListComponent from "./TreeListComponent.vue";

const loggedIn = JSON.parse(document.getElementById("logged-in").textContent);
const userTrees = JSON.parse(document.getElementById("user-trees").textContent);

const syncTimerBaseCount = 1 * 1000; // 5 seconds

let tempTreeStore = ref([]);
let syncTimer = null;

if (loggedIn) {
  tempTreeStore.value.push.apply(tempTreeStore.value, userTrees);
} else {
  tempTreeStore.value.push(treeHelpers.defaultTree());
}

let selectedTreeIndex = ref(0);

watch(tempTreeStore.value[0], (newValue, oldValue) => {
  console.log(`The first tree has been changed"`);

  // reset the sync timer
  if (syncTimer) {
    clearTimeout(syncTimer);
  }

  // start the sync timer
  syncTimer = setTimeout(async () => {
    const updateStatus = await treeHelpers.updateTree(tempTreeStore.value[0])

    console.log(`updateStatus: ${updateStatus}`)
  }, syncTimerBaseCount);
});

// 3 reactive states: syncing, synced, failed that

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
