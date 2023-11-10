<script setup lang="ts">
import { ref, watch, computed, nextTick } from "vue";
import * as treeHelpers from "../treeHelpers";
import * as timeUtils from "../timeUtils";
import { useLocalStorage } from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TransitionOutInGrow from "../transitions/TransitionOutInGrow.vue";
import TransitionBasic from "../transitions/TransitionBasic.vue";
import TransitionSlide from "../transitions/TransitionSlide.vue";
import TreeListItemComponent from "./TreeListItemComponent.vue";

// TODO: loggedIn and userTrees error handling
const loggedIn: boolean = JSON.parse(
  document.getElementById("logged-in").textContent,
);

const localTreeStore = useLocalStorage("tree-store", {
  trees: [treeHelpers.defaultTree()],
});
let syncTimerBaseCount = 2000;

const tempTreeStore = ref([]);
let syncTimer = null;
const syncIndicator = ref("synced");
const selectedTreeIndex = ref(0);
const hideUncontrollable = ref(false);
const syncWarningExpanded = ref(false);
const newTreeLoading = ref(false);

initializeTrees();

function initializeTrees() {
  if (loggedIn) {
    tempTreeStore.value = JSON.parse(
      document.getElementById("user-trees").textContent,
    );

    initializeTreeWatchers();
  } else {
    // TODO: see if this causes performance issues
    tempTreeStore.value = localTreeStore.value.trees;
  }
}

const lastRemainingTree = computed(() => {
  return tempTreeStore.value.length === 1;
});

const selectedTreeId = computed(() => {
  return tempTreeStore.value[selectedTreeIndex.value].tree_id;
});

function treeWatcher(treeIndex: string) {
  const treeInQuestion = tempTreeStore.value[treeIndex];

  watch(treeInQuestion, (newValue, oldValue) => {
    syncIndicator.value = "syncing";

    // reset the sync timer
    if (syncTimer) {
      clearTimeout(syncTimer);
    }

    // start the sync timer
    syncTimer = setTimeout(async () => {
      const updateStatus = await treeHelpers.updateTree(
        treeInQuestion,
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

function warningClickOutsideHandler(): void {
  syncWarningExpanded.value = false;
}

async function newTree(loggedIn: boolean) {
  newTreeLoading.value = loggedIn;
  const treeId = await treeHelpers.createTree(loggedIn);
  const newTree = treeHelpers.defaultTree(treeId);

  tempTreeStore.value.splice(0, 0, newTree);
  if (loggedIn) {
    addTreeWatcher(treeId);
  }
  newTreeLoading.value = false;
}

async function deleteTreeHandler(treeId: string) {
  const indexToDelete = tempTreeStore.value.findIndex(
    (tree) => tree.tree_id === treeId,
  );

  if (indexToDelete !== -1) {
    if (selectedTreeIndex.value !== indexToDelete) {
      selectedTreeIndex.value = 0;
      tempTreeStore.value.splice(indexToDelete, 1);
    } else {
      selectedTreeIndex.value = 0;
      // await nextTick()
      tempTreeStore.value.splice(indexToDelete, 1);
    }
  }
}

function unfocusInput(event) {
  event.target.blur();
}
</script>

<template v-cloak>
  <div class="mx-auto my-2 w-full overflow-x-hidden px-4">
    <div
      class="flex h-full w-full flex-col items-center gap-y-10 lg:flex-row lg:items-start lg:gap-x-5"
    >
      <!--  Tree List  -->
      <!-- Mobile tree list: on top, sm:on the left -->
      <div
        class="mt-8 w-full rounded-md bg-white px-3 py-2 shadow-lg ring-1 ring-opacity-5 ring-primarylight focus:outline-none lg:w-96"
      >
        <div class="divide-y divide-solid divide-primarylight">
          <div class="my-1 py-2 text-center text-xl text-textblackdim">
            Trees
          </div>
          <div>
            <button
              class="my-2 rounded-md px-1 py-2 transition duration-100 ease-out hover:bg-primarylight hover:text-black"
              @click="newTree(loggedIn)"
            >
              <TransitionOutInGrow duration="50">
                <!-- New Tree icon -->
                <svg
                  v-if="!newTreeLoading"
                  class="h-7 w-7 text-textblackdim"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-label="Add Tree"
                >
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M10 1a1 1 0 0 0-.707.293l-6 6A1 1 0 0 0 3 8v12a3 3 0 0 0 3 3h8a1 1 0 1 0 0-2H6a1 1 0 0 1-1-1V9h5a1 1 0 0 0 1-1V3h7a1 1 0 0 1 1 1v4a1 1 0 1 0 2 0V4a3 3 0 0 0-3-3h-8ZM9 7H6.414L9 4.414V7Zm11 5a1 1 0 1 0-2 0v3h-3a1 1 0 1 0 0 2h3v3a1 1 0 1 0 2 0v-3h3a1 1 0 1 0 0-2h-3v-3Z"
                    fill="currentColor"
                  />
                </svg>
                <!-- Loading icon -->
                <svg
                  v-else-if="newTreeLoading"
                  class="h-7 w-7 animate-spin"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M20 12a8 8 0 0 1-11.76 7.061"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                  />
                </svg>
              </TransitionOutInGrow>
            </button>
          </div>
          <ul class="list-none">
            <component
              v-for="tree in tempTreeStore"
              :key="tree.tree_id"
              :is="TreeListItemComponent"
              :tree="tree"
              :selected-tree-id="selectedTreeId"
              :last-remaining-tree="lastRemainingTree"
              :logged-in="loggedIn"
              @select-tree="(treeId: string) => selectTreeHandler(treeId)"
              @delete-tree="(treeId: string) => deleteTreeHandler(treeId)"
            />
          </ul>
        </div>
      </div>

      <!--   Info & Controls   -->
      <div
        class="mx-auto flex w-full flex-col gap-y-6 text-textblackdim lg:my-8 lg:px-6"
      >
        <div class="flex justify-between">
          <div class="flex">
            <!--   Tree Name   -->
            <div class="text-textblackdim">
              <input
                class="w-full rounded bg-white px-5 py-2 shadow-lg ring-1 ring-opacity-5 ring-primarylight focus:outline-none"
                id="selected-tree-name-input"
                type="text"
                maxlength="22"
                v-model="tempTreeStore[selectedTreeIndex].tree_name"
                @keydown.enter.exact.prevent.stop="unfocusInput($event)"
              />
            </div>
          </div>

          <div class="mx-4 flex items-center gap-x-4">
            <!--     Sync status     -->
            <div class="text-textblackdim">
              <TransitionOutInGrow>
                <svg
                  v-if="syncIndicator === 'syncing'"
                  class="h-8 w-8 animate-spin"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M14.393 5.374c3.632 1.332 5.505 5.378 4.183 9.038a7.008 7.008 0 0 1-5.798 4.597m0 0 1.047-1.754m-1.047 1.754 1.71.991m-4.881-1.374c-3.632-1.332-5.505-5.378-4.183-9.038a7.008 7.008 0 0 1 5.798-4.597m0 0-1.047 1.754m1.047-1.754L9.512 4"
                    stroke-width="1.5"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>

                <svg
                  v-else-if="syncIndicator === 'synced'"
                  class="h-8 w-8"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M16.5 5.385a8 8 0 0 1-5.707 14.525M13.16 4.083A8 8 0 0 0 7.405 18.55M13.16 4.083 12.5 3m.66 1.083L12.5 5m-1.707 14.91.963-.91m-.963.91L11.5 21M9 12l2 2 4-4"
                    stroke-width="1.5"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
                <svg
                  v-else-if="syncIndicator === 'failed'"
                  class="h-8 w-8"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M15.938 6.12A7.135 7.135 0 0 1 19 12c0 3.927-3.134 7.111-7 7.111-.359 0-.711-.027-1.056-.08m2.07-14.068A6.949 6.949 0 0 0 12 4.89c-3.866 0-7 3.184-7 7.111a7.136 7.136 0 0 0 2.979 5.822m5.036-12.859L12.437 4m.578.963-.578.815M10.944 19.03l.843-.809m-.843.809.618.969M12 9v3.5m0 2v.5"
                    stroke-width="1.5"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </TransitionOutInGrow>
            </div>

            <!--     Not logged in sync warning     -->
            <div
              class="text-textblackdim"
              v-show="!loggedIn"
              @mouseover="syncWarningExpanded = true"
              @mouseleave="syncWarningExpanded = false"
            >
              <div
                class="relative flex cursor-pointer items-center text-textblackdim hover:text-gray-600"
              >
                <TransitionBasic duration="100">
                  <div
                    v-show="syncWarningExpanded"
                    class="absolute top-0 right-0 mt-14 -ml-32 inline-block w-60 rounded-lg bg-white px-4 py-3 ring-1 ring-opacity-5 text-textblackdim ring-warning focus:outline-none"
                  >
                    <span class="inline-block leading-tight"
                      >Your data has been saved to this device only. Log in to
                      save and access your data from any device.</span
                    >
                  </div>
                </TransitionBasic>

                <button
                  v-on:click="syncWarningExpanded = !syncWarningExpanded"
                  v-click-outside="warningClickOutsideHandler"
                >
                  <span>
                    <svg
                      class="h-6 w-6 rounded-full drop-shadow-md fill-warning"
                      viewBox="0 0 1920 1920"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M960 0c530.193 0 960 429.807 960 960s-429.807 960-960 960S0 1490.193 0 960 429.807 0 960 0Zm-9.838 1342.685c-84.47 0-153.19 68.721-153.19 153.19 0 84.47 68.72 153.192 153.19 153.192s153.19-68.721 153.19-153.191-68.72-153.19-153.19-153.19ZM1153.658 320H746.667l99.118 898.623h208.755L1153.658 320Z"
                        fill-rule="evenodd"
                      />
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-x-3 text-textblackdim">
          <div>
            <span class="text-xl text-textblackdim">Uncontrollable</span>
          </div>

          <button
            class="text-textblackdim"
            v-on:click="hideUncontrollable = !hideUncontrollable"
          >
            <TransitionBasic>
              <!-- Not visible -->
              <svg
                v-if="hideUncontrollable"
                class="h-7 w-7 text-textblackdim fill-textblackdim"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4.495 7.44c-.948.678-1.717 1.402-2.306 2.04a3.679 3.679 0 0 0 0 5.04C3.917 16.391 7.19 19 12 19c1.296 0 2.48-.19 3.552-.502l-1.662-1.663A10.77 10.77 0 0 1 12 17c-4.033 0-6.812-2.18-8.341-3.837a1.68 1.68 0 0 1 0-2.326 12.972 12.972 0 0 1 2.273-1.96L4.495 7.442Z"
                />
                <path
                  d="M8.533 11.478a3.5 3.5 0 0 0 3.983 3.983l-3.983-3.983ZM15.466 12.447l-3.919-3.919a3.5 3.5 0 0 1 3.919 3.919Z"
                />
                <path
                  d="M18.112 15.093a12.99 12.99 0 0 0 2.23-1.93 1.68 1.68 0 0 0 0-2.326C18.811 9.18 16.032 7 12 7c-.64 0-1.25.055-1.827.154L8.505 5.486A12.623 12.623 0 0 1 12 5c4.811 0 8.083 2.609 9.81 4.48a3.679 3.679 0 0 1 0 5.04c-.58.629-1.334 1.34-2.263 2.008l-1.435-1.435ZM2.008 3.422a1 1 0 1 1 1.414-1.414L22 20.586A1 1 0 1 1 20.586 22L2.008 3.422Z"
                />
              </svg>
              <!-- Visible -->
              <svg
                v-else-if="!hideUncontrollable"
                class="h-7 w-7 text-textblackdim fill-textblackdim"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M11.994 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Zm0-2.006a1.494 1.494 0 1 1 0-2.988 1.494 1.494 0 0 1 0 2.988Z"
                />
                <path
                  d="M12 5C7.189 5 3.917 7.609 2.19 9.48a3.679 3.679 0 0 0 0 5.04C3.916 16.391 7.188 19 12 19c4.811 0 8.083-2.609 9.81-4.48a3.679 3.679 0 0 0 0-5.04C20.084 7.609 16.812 5 12 5Zm-8.341 5.837C5.189 9.18 7.967 7 12 7c4.033 0 6.812 2.18 8.341 3.837a1.68 1.68 0 0 1 0 2.326C18.811 14.82 16.033 17 12 17c-4.033 0-6.812-2.18-8.341-3.837a1.68 1.68 0 0 1 0-2.326Z"
                />
              </svg>
            </TransitionBasic>
          </button>
        </div>

        <!--   Tree   -->
        <div class="mb-40 w-full lg:mb:0">
          <component
            v-show="
              tempTreeStore.length !== 0 && tempTreeStore[selectedTreeIndex]
            "
            :is="TreeComponent"
            :nodes="tempTreeStore[selectedTreeIndex].tree_data"
            :logged-in="loggedIn"
            :hide-uncontrollable="hideUncontrollable"
            :node-type="'root'"
            :parent-node-id="'root'"
          />
        </div>
      </div>
    </div>
  </div>
</template>
