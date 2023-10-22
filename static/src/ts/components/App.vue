<script setup lang="ts">
import {ref, watch} from "vue";
import * as treeHelpers from "../treeHelpers";
import {useLocalStorage} from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TreeListComponent from "./TreeListComponent.vue";
import TransitionOutIn from "../transitions/TransitionOutIn.vue";

// TODO: loggedIn and userTrees error handling
const loggedIn: boolean = JSON.parse(
    document.getElementById("logged-in").textContent,
);

const localTreeStore = useLocalStorage("tree-store", {
  trees: [treeHelpers.defaultTree()],
});
let syncTimerBaseCount = 3000;

let tempTreeStore = ref([]);
let syncTimer = null;
let syncIndicator = ref("synced");
let selectedTreeIndex = ref(0);

initializeTrees();

function initializeTrees() {
  if (loggedIn) {
    tempTreeStore.value = JSON.parse(
        document.getElementById("user-trees").textContent,
    );

    initializeTreeWatchers();
  } else {
    // syncTimerBaseCount = 1000;
    // TODO: see if this could cause performance issues
    tempTreeStore.value = localTreeStore.value.trees;
  }
}

function treeWatcher(treeIndex: string) {
  watch(tempTreeStore.value[treeIndex], (newValue, oldValue) => {
    syncIndicator.value = "syncing";

    // reset the sync timer
    if (syncTimer) {
      clearTimeout(syncTimer);
    }

    // start the sync timer
    syncTimer = setTimeout(async () => {
      const updateStatus = await treeHelpers.updateTree(
          tempTreeStore.value[treeIndex],
          loggedIn,
      );

      if (updateStatus === 200) {
        syncIndicator.value = "synced";
      } else {
        syncIndicator.value = "failed";
      }
    }, syncTimerBaseCount);
  });
}

function initializeTreeWatchers() {
  for (const index in tempTreeStore.value) {
    treeWatcher(index);
  }
}

function addTreeWatcher(treeId: string) {
  const indexToWatch = tempTreeStore.value.findIndex(
      (tree) => tree.tree_id === treeId,
  );

  if (indexToWatch !== -1) {
    treeWatcher(indexToWatch.toString());
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
  <div class="flex flex-col w-full min-h-screen">

    <div class="flex flex-row h-full">
      <div class="w-max bg-backg border-r-2 border-accent">
        <component
            :is="TreeListComponent"
            :trees="tempTreeStore"
            :logged-in="loggedIn"
            @select-tree="(treeId: string) => selectTreeHandler(treeId)"
            @create-tree="(treeId: string) => addTreeWatcher(treeId)"
        />
      </div>
      <div>
        <span v-show="!loggedIn" class="text-textblackdim">
          <svg class="h-5 w-5 fill-textblackdim" viewBox="0 0 1920 1920" xmlns="http://www.w3.org/2000/svg"><path
              d="M960 0c530.193 0 960 429.807 960 960s-429.807 960-960 960S0 1490.193 0 960 429.807 0 960 0Zm-9.838 1342.685c-84.47 0-153.19 68.721-153.19 153.19 0 84.47 68.72 153.192 153.19 153.192s153.19-68.721 153.19-153.191-68.72-153.19-153.19-153.19ZM1153.658 320H746.667l99.118 898.623h208.755L1153.658 320Z"
              fill-rule="evenodd"/></svg>
        </span>

        <div class="text-textblackdim">
          <TransitionOutIn>
            <svg v-if="syncIndicator === 'syncing'"
                 class="animate-spin h-6 w-6" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M14.393 5.374c3.632 1.332 5.505 5.378 4.183 9.038a7.008 7.008 0 0 1-5.798 4.597m0 0 1.047-1.754m-1.047 1.754 1.71.991m-4.881-1.374c-3.632-1.332-5.505-5.378-4.183-9.038a7.008 7.008 0 0 1 5.798-4.597m0 0-1.047 1.754m1.047-1.754L9.512 4"
                  stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>

            <svg v-else-if="syncIndicator === 'synced'" class="h-6 w-6" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M16.5 5.385a8 8 0 0 1-5.707 14.525M13.16 4.083A8 8 0 0 0 7.405 18.55M13.16 4.083 12.5 3m.66 1.083L12.5 5m-1.707 14.91.963-.91m-.963.91L11.5 21M9 12l2 2 4-4"
                  stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else-if="syncIndicator === 'failed'" class="h-6 w-6" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M15.938 6.12A7.135 7.135 0 0 1 19 12c0 3.927-3.134 7.111-7 7.111-.359 0-.711-.027-1.056-.08m2.07-14.068A6.949 6.949 0 0 0 12 4.89c-3.866 0-7 3.184-7 7.111a7.136 7.136 0 0 0 2.979 5.822m5.036-12.859L12.437 4m.578.963-.578.815M10.944 19.03l.843-.809m-.843.809.618.969M12 9v3.5m0 2v.5"
                  stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </TransitionOutIn>
        </div>

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


  </div>
</template>