<script setup lang="ts">
import {ref, watch} from "vue";
import * as treeHelpers from "../treeHelpers";
import {useStorage} from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TreeListComponent from "./TreeListComponent.vue";

const loggedIn = JSON.parse(document.getElementById("logged-in").textContent);
const userTrees = JSON.parse(document.getElementById("user-trees").textContent);

const syncTimerBaseCount = 1 * 1000; // 5 seconds

let tempTreeStore = ref([]);
let syncTimer = null;
let syncIndicator = ref('synced')

if (loggedIn) {
  tempTreeStore.value.push.apply(tempTreeStore.value, userTrees);
} else {
  tempTreeStore.value.push(treeHelpers.defaultTree());
}

let selectedTreeIndex = ref(0);


function treeWatcher(treeIndex: string) {
  watch(tempTreeStore.value[treeIndex], (newValue, oldValue) => {
    syncIndicator.value = "syncing"

    // reset the sync timer
    if (syncTimer) {
      clearTimeout(syncTimer);
    }

    // start the sync timer
    syncTimer = setTimeout(async () => {
      const updateStatus = await treeHelpers.updateTree(tempTreeStore.value[treeIndex])

      if (updateStatus === 200) {
        syncIndicator.value = "synced"
      } else {
        syncIndicator.value = "failed"
      }

    }, syncTimerBaseCount);
  });
}

function initializeTreeWatchers() {
  for (const index in tempTreeStore.value) {
    treeWatcher(index)
  }
}

initializeTreeWatchers()

function addTreeWatcher(treeId: string) {
  const indexToWatch = tempTreeStore.value.findIndex(
      (tree) => tree.tree_id === treeId,
  );

  if (indexToWatch !== -1) {
    treeWatcher(indexToWatch.toString())
  }
}


function selectTreeHandler(treeId: string): void {
  const indexToSelect = tempTreeStore.value.findIndex(
      (tree) => tree.tree_id === treeId,
  );

  if (indexToSelect !== -1) {
    if (selectedTreeIndex.value != indexToSelect) {
      selectedTreeIndex.value = indexToSelect;
    }
  }
}
</script>

<template>
  <div>
    <div>
      <div>
        <span v-text="syncIndicator">

        </span>
      </div>
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
          @create-tree="(treeId: string) => addTreeWatcher(treeId)"
      />
    </div>
  </div>
</template>
