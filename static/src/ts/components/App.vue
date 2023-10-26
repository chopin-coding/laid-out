<script setup lang="ts">
import { ref, watch, computed } from "vue";
import * as treeHelpers from "../treeHelpers";
import { useLocalStorage } from "@vueuse/core";
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
let showTreeList = ref(false);
let visibilityToggle = ref(false);

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
  <div class="mx-auto px-1 sm:px-6">
    <div class="flex flex-col h-full items-center sm:flex-row gap-y-6">
      <!--  Tree List  -->
      <!-- Mobile tree list: on top, sm:on the left -->
      <div
        class="sm:w-44 w-60 px-3 py-2 mt-8 rounded-md shadow-lg ring-1 ring-primary ring-opacity-5 focus:outline-none"
      >
        <component
          :is="TreeListComponent"
          :trees="tempTreeStore"
          :logged-in="loggedIn"
          @select-tree="(treeId: string) => selectTreeHandler(treeId)"
          @create-tree="(treeId: string) => addTreeWatcher(treeId)"
        />
      </div>

      <!--   Info & Controls   -->
      <div class="flex flex-col w-60 mx-auto sm:px-6 gap-y-2">
        <div class="flex justify-between">
          <div>
            <div class="text-xl text-center py-1">Tree Name</div>
          </div>

          <div class="flex items-center gap-x-1">
            <!--     Sync status     -->
            <div class="text-textblackdim">
              <TransitionOutIn>
                <svg
                  v-if="syncIndicator === 'syncing'"
                  class="h-7 w-7 animate-spin"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M14.393 5.374c3.632 1.332 5.505 5.378 4.183 9.038a7.008 7.008 0 0 1-5.798 4.597m0 0 1.047-1.754m-1.047 1.754 1.71.991m-4.881-1.374c-3.632-1.332-5.505-5.378-4.183-9.038a7.008 7.008 0 0 1 5.798-4.597m0 0-1.047 1.754m1.047-1.754L9.512 4"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>

                <svg
                  v-else-if="syncIndicator === 'synced'"
                  class="h-7 w-7"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M16.5 5.385a8 8 0 0 1-5.707 14.525M13.16 4.083A8 8 0 0 0 7.405 18.55M13.16 4.083 12.5 3m.66 1.083L12.5 5m-1.707 14.91.963-.91m-.963.91L11.5 21M9 12l2 2 4-4"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
                <svg
                  v-else-if="syncIndicator === 'failed'"
                  class="h-7 w-7"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M15.938 6.12A7.135 7.135 0 0 1 19 12c0 3.927-3.134 7.111-7 7.111-.359 0-.711-.027-1.056-.08m2.07-14.068A6.949 6.949 0 0 0 12 4.89c-3.866 0-7 3.184-7 7.111a7.136 7.136 0 0 0 2.979 5.822m5.036-12.859L12.437 4m.578.963-.578.815M10.944 19.03l.843-.809m-.843.809.618.969M12 9v3.5m0 2v.5"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </TransitionOutIn>
            </div>

            <!--     Not logged in sync warning     -->
            <div class="text-textblackdim">
              <span v-show="!loggedIn">
                <svg
                  class="h-5 w-5 fill-warning shadow-md rounded-full"
                  viewBox="0 0 1920 1920"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M960 0c530.193 0 960 429.807 960 960s-429.807 960-960 960S0 1490.193 0 960 429.807 0 960 0Zm-9.838 1342.685c-84.47 0-153.19 68.721-153.19 153.19 0 84.47 68.72 153.192 153.19 153.192s153.19-68.721 153.19-153.191-68.72-153.19-153.19-153.19ZM1153.658 320H746.667l99.118 898.623h208.755L1153.658 320Z"
                    fill-rule="evenodd"
                  />
                </svg>
              </span>
            </div>
          </div>
        </div>

        <div class="flex">
          <!--   Tree Name   -->
          <div class="text-textblackdim">
            <input
              class="w-32 rounded shadow-lg ring-1 ring-primary ring-opacity-5 focus:outline-none"
              id="selected-tree-name-input"
              type="text"
              maxlength="20"
              v-model="tempTreeStore[selectedTreeIndex].tree_name"
            />
          </div>
        </div>

        <div class="flex gap-x-2">
          <label for="uncontrollable-visibility toggle">Controllable</label>
          <button class="text-textblackdim" v-on:click="visibilityToggle = !visibilityToggle">
            <!-- Not visible -->
            <svg
              v-show="visibilityToggle"
              class="h-5 w-5"
              viewBox="0 0 32 32"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="m30.89 16.46.24-.46-.24-.46A17 17 0 0 0 16 6a15.7 15.7 0 0 0-6.91 1.63L4.73 3.27 3.31 4.69l4 4 2.43 2.43L12.58 14l1.5 1.51 2.46 2.46 1.51 1.5 2.87 2.87 2 2.05 4.34 4.35 1.42-1.42-4-4a18.34 18.34 0 0 0 6.21-6.86Zm-12.95 0-2.42-2.42A2.42 2.42 0 0 1 16 14a2 2 0 0 1 2 2 2.42 2.42 0 0 1-.06.48Zm4.39 4.39L19.45 18A4 4 0 0 0 14 12.55l-2.87-2.88a8 8 0 0 1 11.2 11.2Zm2.39 0a10 10 0 0 0 0-9.78A16.47 16.47 0 0 1 28.86 16a16.47 16.47 0 0 1-4.14 4.89ZM19.15 23.35a8 8 0 0 1-10.5-10.5l-1.49-1.49a9.92 9.92 0 0 0 .12 9.53A16.47 16.47 0 0 1 3.14 16a16.23 16.23 0 0 1 4-4.71L5.66 9.86a18.5 18.5 0 0 0-4.55 5.68L.87 16l.24.46A17 17 0 0 0 16 26a15.42 15.42 0 0 0 5-.84Z"
              />
            </svg>

            <!-- Visible -->
            <svg
              v-show="!visibilityToggle"
              class="h-5 w-5"
              viewBox="0 0 32 32"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M30.89 15.54A17 17 0 0 0 16 6a17 17 0 0 0-14.89 9.54L.87 16l.24.46A17 17 0 0 0 16 26a17 17 0 0 0 14.89-9.54l.24-.46ZM24 16a8 8 0 1 1-8-8 8 8 0 0 1 8 8ZM3.14 16a16.47 16.47 0 0 1 4.14-4.89 10 10 0 0 0 0 9.78A16.47 16.47 0 0 1 3.14 16Zm21.58 4.89a10 10 0 0 0 0-9.78A16.47 16.47 0 0 1 28.86 16a16.47 16.47 0 0 1-4.14 4.89Z"
              />
              <path
                d="M16 20a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0-6a2 2 0 1 1-2 2 2 2 0 0 1 2-2Z"
              />
            </svg>
          </button>
        </div>
      </div>
      <!--   Tree   -->
      <div class="sm:w-44 w-60 mb-10">
        <component
          v-if="tempTreeStore.length !== 0"
          :is="TreeComponent"
          :tree-nodes="tempTreeStore[selectedTreeIndex].tree_data"
          :logged-in="loggedIn"
          :hide-uncontrollable="visibilityToggle"
        />
        <div v-else>No trees to show</div>
      </div>
    </div>
  </div>
</template>
