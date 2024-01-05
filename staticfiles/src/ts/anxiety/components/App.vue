<script setup lang="ts">
import {ref, watch, computed, nextTick} from "vue";
import * as helpers from "../helpers";
import * as timeUtils from "../../timeUtils";
import {useLocalStorage} from "@vueuse/core";
import TreeComponent from "./TreeComponent.vue";
import TransitionOutInGrow from "../../transitions/TransitionOutInGrow.vue";
import TransitionBasic from "../../transitions/TransitionBasic.vue";
import TransitionSlide from "../../transitions/TransitionSlide.vue";
import TreeListItemComponent from "./TreeListItemComponent.vue";
import {config} from "../../config";
import CharacterAnimation from "../../animations/CharacterAnimation.vue";

// TODO: loggedIn and userTrees error handling
const loggedIn: boolean = JSON.parse(
    document.getElementById("logged-in").textContent,
);

const localTreeStore = useLocalStorage("tree-store", {
  trees: [helpers.defaultTree()],
});
let syncTimerBaseCount = config.SYNC_TIMER_DURATION_MS;

const tempTreeStore = ref([]);
let syncTimer = null;
const syncStatus = ref("synced");
const selectedTreeIndex = ref(0);
const hideUncontrollable = ref(false);
const syncWarningExpanded = ref(false);
const syncFailedExpanded = ref(false);
const newTreeLoading = ref(false);
const maxNumberOfTrees = 150; // the browser may shit itself before 150 trees:D

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

const numberOfTrees = computed(() => {
  return tempTreeStore.value.length;
});

window.addEventListener("beforeunload", function (e) {
  if (loggedIn && syncStatus.value === "syncing") {
    const confirmationMessage =
        "You have unsaved changes. Are you sure you want to leave?";

    // Standard for most browsers
    e.returnValue = confirmationMessage;

    // For some older browsers
    return confirmationMessage;
  }
});

function treeWatcher(treeIndex: string) {
  const treeInQuestion = tempTreeStore.value[treeIndex];

  watch(treeInQuestion, (newValue, oldValue) => {
    syncStatus.value = "syncing";

    // reset the sync timer
    if (syncTimer) {
      clearTimeout(syncTimer);
    }

    // start the sync timer
    syncTimer = setTimeout(async () => {
      const updateStatus = await helpers.updateTree(
          treeInQuestion,
          loggedIn,
      );

      if (updateStatus === 200) {
        syncStatus.value = "synced";
      } else {
        syncStatus.value = "failed";
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

async function newTree(loggedIn: boolean) {
  if (numberOfTrees.value < maxNumberOfTrees) {
    newTreeLoading.value = loggedIn;
    const treeId = await helpers.createTree(loggedIn);
    const newTree = helpers.defaultTree(treeId);

    tempTreeStore.value.splice(0, 0, newTree);
    await nextTick();
    selectedTreeIndex.value += 1

    if (loggedIn) {
      addTreeWatcher(treeId);
    }
    newTreeLoading.value = false;
  }
}

async function deleteTreeHandler(treeId: string) {
  const indexToDelete = tempTreeStore.value.findIndex(
      (tree) => tree.tree_id === treeId,
  );

  if (indexToDelete === -1) {
    console.log("The tree trying to be deleted does not exist in tempTreeStore")
    return;
  }

  if (indexToDelete !== tempTreeStore.value.length - 1) {
    tempTreeStore.value.splice(indexToDelete, 1);
  } else if (indexToDelete === tempTreeStore.value.length - 1) {
    selectedTreeIndex.value -= 1
    tempTreeStore.value.splice(indexToDelete, 1);
  }

}

function unfocusInput(event) {
  event.target.blur();
}

</script>

<template v-cloak>
  <div class="mx-auto my-2 w-full overflow-x-hidden px-4">
    <div class="text-4xl text-center  font-semibold text-textblackdimmer mt-8">
      Anxiety
    </div>

    <CharacterAnimation
        class="-mb-5 z-50"
        character="cat"
        :action="{
      name: 'idle',
      numberOfFrames: 2,
      ticksPerFrame: 300,
      loop: true
        }"
    />
    <div
        class="flex h-full w-full flex-col gap-y-10 items-center lg:flex-row lg:items-start lg:gap-x-5"
    >

      <!--  Tree List  -->
      <!-- Mobile tree list: on top, sm:on the left -->


      <div
          class="w-full rounded-md bg-white px-3 py-2 shadow-lg sm:mb-10 ring-1 ring-opacity-5 ring-primarylight focus:outline-none lg:w-96"
      >
        <div class="divide-y divide-solid divide-primarylight">
          <div>
            <button
                class="my-2 rounded-md px-2 py-2 transition duration-100 ease-out text-textblackdimmer hover:bg-primarylight hover:text-black"
                v-on:click="newTree(loggedIn)"
            >
              <TransitionOutInGrow duration="50">
                <!-- New Tree icon -->
                <div
                    v-if="!newTreeLoading && numberOfTrees < maxNumberOfTrees"
                    class="flex gap-x-3"
                >
                  <svg
                      class="h-6 w-6"
                      viewBox="0 0 32 32"
                      xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                        d="M30 28c0 1.1-.896 2-2 2H4c-1.104 0-2-.9-2-2V4c0-1.1.896-2 2-2h24c1.104 0 2 .9 2 2v24ZM28 0H4a4 4 0 0 0-4 4v24a4 4 0 0 0 4 4h24a4 4 0 0 0 4-4V4a4 4 0 0 0-4-4Zm-6 15h-5v-5c0-.55-.448-1-1-1s-1 .45-1 1v5h-5c-.552 0-1 .45-1 1s.448 1 1 1h5v5c0 .55.448 1 1 1s1-.45 1-1v-5h5c.552 0 1-.45 1-1s-.448-1-1-1Z"
                        fill="currentColor"
                        fill-rule="evenodd"
                    />
                  </svg>
                  <span> Create new </span>
                </div>

                <!-- Loading icon -->
                <svg
                    v-else-if="newTreeLoading"
                    class="h-6 w-6animate-spin"
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

                <div
                    v-else-if="numberOfTrees >= maxNumberOfTrees"

                >
                  <div class="text-danger">Maximum number of trees reached</div>
                  <div>
                    This limit is just to prevent spam. You're awesome for reaching this limit! Please do contact me if
                    you'd like to have more trees at once!
                  </div>
                </div>
              </TransitionOutInGrow>
            </button>
          </div>
          <ul class="max-h-80 list-none overflow-y-scroll sm:max-h-96">
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
        <div class="flex flex-col gap-y-3 sm:flex-row sm:justify-between">
          <!--   Tree Name   -->
          <div class="flex text-textblackdim">
            <input
                class="rounded px-5 py-2 shadow-lg ring-1 ring-opacity-5 transition duration-100 ease-out bg-backg ring-primarylight focus:outline-none"
                id="selected-tree-name-input"
                type="text"
                maxlength="22"
                v-model="tempTreeStore[selectedTreeIndex].tree_name"
                @keydown.enter.exact.prevent.stop="unfocusInput($event)"
            />
          </div>

          <div class="mx-1 flex items-center gap-x-1 sm:mx-4">
            <!--     Sync status     -->
            <div class="relative text-textblackdimmer" title="Sync status">
              <TransitionOutInGrow>
                <svg
                    v-if="syncStatus === 'syncing'"
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
                    v-else-if="syncStatus === 'synced'"
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
                    @mouseover="syncFailedExpanded = true"
                    @mouseleave="syncFailedExpanded = false"
                    v-else-if="syncStatus === 'failed'"
                    class="h-8 w-8 text-danger"
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
              <TransitionBasic duration="150">
                <div
                    v-show="syncStatus === 'failed' && syncFailedExpanded"
                    class="absolute top-0 right-0 mt-14 -ml-32 inline-block w-60 rounded-lg bg-white px-4 py-3 ring-1 ring-opacity-5 text-textblackdim ring-danger focus:outline-none"
                >
                  <span class="inline-block text-sm leading-tight"
                  >Couldn't save tree data to your account. If a refresh
                    doesn't solve the issue, please contact the admin.</span
                  >
                </div>
              </TransitionBasic>
            </div>

            <!--     Not logged in sync warning     -->
            <div
                class="text-textblackdim"
                v-show="!loggedIn"
                @mouseover="syncWarningExpanded = true"
                @mouseleave="syncWarningExpanded = false"
            >
              <div
                  class="relative flex items-center text-textblackdim"
              >
                <TransitionBasic duration="150">
                  <div
                      v-show="syncWarningExpanded"
                      class="absolute top-0 right-0 mt-14 -ml-32 inline-block w-60 rounded-lg bg-white px-4 py-3 ring-1 ring-opacity-5 text-textblackdim ring-warning focus:outline-none"
                  >
                    <span class="inline-block text-sm leading-tight"
                    >Your data has been saved to this device only. Log in to
                      save and access your data from any device.</span
                    >
                  </div>
                </TransitionBasic>

                <button>
                  <!-- Warning icon -->
                  <svg
                      class="h-8 w-8 fill-warning"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M19.5 12a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Zm1.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9.75 1.5V8.25h1.5v5.25h-1.5Zm0 2.25v-1.5h1.5v1.5h-1.5Z"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-x-3 text-textblackdim">
          <div>
            <span class="text-lg text-textblackdim">Uncontrollable</span>
          </div>

          <button
              class="transition duration-100 ease-out fill-textblackdimmer hover:fill-black"
              v-on:click="hideUncontrollable = !hideUncontrollable"
              title="Toggle uncontrollable items visibility"
          >
            <TransitionBasic>
              <!-- Not visible -->
              <svg
                  v-if="hideUncontrollable"
                  class="h-7 w-7"
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
                  class="h-7 w-7"
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
        <div class="mb-40 w-full sm:mb-10 lg:mb:20">
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

<style scoped>

</style>

