<script setup lang="ts">
import {ref, watch} from "vue";
import * as treeHelpers from "../treeHelpers";
import {useLocalStorage} from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TreeListComponent from "./TreeListComponent.vue";


// FIXME: loggedIn and userTrees error handling
const loggedIn: boolean = JSON.parse(document.getElementById("logged-in").textContent);


const localTreeStore = useLocalStorage('tree-store', {trees: [treeHelpers.defaultTree()]})
let syncTimerBaseCount = 3000

let tempTreeStore = ref([]);
let syncTimer = null;
let syncIndicator = ref('synced')
let selectedTreeIndex = ref(0);

initializeTrees()

function initializeTrees() {
  if (loggedIn) {
    tempTreeStore.value = JSON.parse(document.getElementById("user-trees").textContent)

    initializeTreeWatchers()
  } else {
    // TODO: see if this causes performance issues
    tempTreeStore.value = localTreeStore.value.trees
  }
}


function treeWatcher(treeIndex: string) {
  watch(tempTreeStore.value[treeIndex], (newValue, oldValue) => {
    syncIndicator.value = "syncing"

    // reset the sync timer
    if (syncTimer) {
      clearTimeout(syncTimer);
    }

    // start the sync timer
    syncTimer = setTimeout(async () => {
      const updateStatus = await treeHelpers.updateTree(tempTreeStore.value[treeIndex], loggedIn)

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
  <div class="text-3xl font-bold underline">
    tailwind test
  </div>
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
          :logged-in="loggedIn"
      />
      <div v-else>No trees to show</div>
    </div>

    <div>
      <component
          :is="TreeListComponent"
          :trees="tempTreeStore"
          :logged-in="loggedIn"
          @select-tree="(treeId: string) => selectTreeHandler(treeId)"
          @create-tree="(treeId: string) => addTreeWatcher(treeId)"
      />
    </div>
  </div>
</template>
