<script setup lang="ts">
import {ref, watch, computed, nextTick} from "vue";
import * as helpers from "../helpers";
import * as timeUtils from "../../timeUtils";
import {useLocalStorage} from "@vueuse/core";
import JournalComponent from "./JournalComponent.vue";
import TransitionOutInGrow from "../../transitions/TransitionOutInGrow.vue";
import TransitionBasic from "../../transitions/TransitionBasic.vue";
import TransitionSlide from "../../transitions/TransitionSlide.vue";
import JournalListItemComponent from "./JournalListItemComponent.vue";
import {config} from "../../config";

// TODO: loggedIn and userTrees error handling
const loggedIn: boolean = JSON.parse(
    document.getElementById("logged-in").textContent,
);

const localJournalStore = useLocalStorage("journal-store", {
  journals: [helpers.defaultJournal()],
});
let syncTimerBaseCount = config.SYNC_TIMER_DURATION_MS;

const tempJournalStore = ref([]);
let syncTimer = null;
const syncStatus = ref("synced");
const selectedJournalIndex = ref(0);
const syncWarningExpanded = ref(false);
const syncFailedExpanded = ref(false);
const newJournalLoading = ref(false);
const maxNumberOfJournals = 150;

initializeJournals();

function initializeJournals() {
  if (loggedIn) {
    tempJournalStore.value = JSON.parse(
        document.getElementById("user-journals").textContent,
    );

    initializeJournalWatchers();
  } else {
    // TODO: see if this causes performance issues
    tempJournalStore.value = localJournalStore.value.journals;
  }
}

const lastRemainingJournal = computed(() => {
  return tempJournalStore.value.length === 1;
});

const selectedJournalId = computed(() => {
  return tempJournalStore.value[selectedJournalIndex.value].journal_id;
});

const numberOfJournals = computed(() => {
  return tempJournalStore.value.length;
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

function journalWatcher(journalIndex: string) {
  const journalInQuestion = tempJournalStore.value[journalIndex];

  watch(journalInQuestion, (newValue, oldValue) => {
    syncStatus.value = "syncing";

    // reset the sync timer
    if (syncTimer) {
      clearTimeout(syncTimer);
    }

    // start the sync timer
    syncTimer = setTimeout(async () => {
      const updateStatus = await helpers.updateJournal(
          journalInQuestion,
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

function initializeJournalWatchers() {
  for (const index in tempJournalStore.value) {
    journalWatcher(index);
  }
}

function addJournalWatcher(journalId: string) {
  const indexToWatch = tempJournalStore.value.findIndex(
      (journal) => journal.journal_id === journalId,
  );

  if (indexToWatch !== -1) {
    journalWatcher(indexToWatch.toString());
  }
}

function selectJournalHandler(journalId: string): void {
  const indexToSelect = tempJournalStore.value.findIndex(
      (journal) => journal.journal_id === journalId,
  );

  if (indexToSelect !== -1) {
    if (selectedJournalIndex.value != indexToSelect) {
      selectedJournalIndex.value = indexToSelect;
    }
  }
}

async function newJournal(loggedIn: boolean) {
  if (numberOfJournals.value < maxNumberOfJournals) {
    newJournalLoading.value = loggedIn;
    const journalId = await helpers.createJournal(loggedIn);
    const newJournal = helpers.defaultJournal(journalId);

    tempJournalStore.value.splice(0, 0, newJournal);
    if (loggedIn) {
      addJournalWatcher(journalId);
    }
    newJournalLoading.value = false;
  }
}

async function deleteJournalHandler(journalId: string) {
  const indexToDelete = tempJournalStore.value.findIndex(
      (journal) => journal.journal_id === journalId,
  );

  if (indexToDelete !== -1) {
    if (selectedJournalIndex.value !== indexToDelete) {
      selectedJournalIndex.value = 0;
      tempJournalStore.value.splice(indexToDelete, 1);
    } else {
      selectedJournalIndex.value = 0;

      tempJournalStore.value.splice(indexToDelete, 1);
    }
  }
}


function unfocusInput(event) {
  event.target.blur();
}
</script>

<template v-cloak>
  <div class="mx-auto my-2 w-full overflow-x-hidden px-4">
    <div class="text-4xl text-center  font-semibold text-textblackdimmer mt-8">
      Journal
    </div>
    <div
        class="flex h-full w-full flex-col items-center gap-y-10 lg:flex-row lg:items-start lg:gap-x-5"
    >

      <!--  Journal List  -->
      <!-- Mobile journal list: on top, sm:on the left -->
      <div
          class="mt-8 w-full rounded-md bg-white px-3 py-2 shadow-lg sm:mb-10 ring-1 ring-opacity-5 ring-primarylight focus:outline-none lg:w-96"
      >
        <div class="divide-y divide-solid divide-primarylight">
          <div>
            <button
                class="my-2 rounded-md px-2 py-2 transition duration-100 ease-out text-textblackdimmer hover:bg-primarylight hover:text-black"
                v-on:click="newJournal(loggedIn)"
            >
              <TransitionOutInGrow duration="50">
                <!-- New Journal icon -->
                <div
                    v-if="!newJournalLoading && numberOfJournals < maxNumberOfJournals"
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
                    v-else-if="newJournalLoading"
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
                    v-else-if="numberOfJournals >= maxNumberOfJournals"

                >
                  <div class="text-danger">Maximum number of journals reached</div>
                  <div>
                    This limit is just to prevent spam. You're awesome for reaching this limit! Please do contact me if
                    you'd like to have more journals at once!
                  </div>
                </div>
              </TransitionOutInGrow>
            </button>
          </div>
          <ul class="max-h-80 list-none overflow-y-scroll sm:max-h-96">
            <component
                v-for="journal in tempJournalStore"
                :key="journal.journal_id"
                :is="JournalListItemComponent"
                :journal="journal"
                :selected-journal-id="selectedJournalId"
                :last-remaining-journal="lastRemainingJournal"
                :logged-in="loggedIn"
                @select-journal="(journalId: string) => selectJournalHandler(journalId)"
                @delete-journal="(journalId: string) => deleteJournalHandler(journalId)"
            />
          </ul>
        </div>
      </div>

      <!--   Info & Controls   -->
      <div
          class="mx-auto flex w-full flex-col gap-y-6 text-textblackdim lg:my-8 lg:px-6"
      >
        <div class="flex flex-col gap-y-3 sm:flex-row sm:justify-between">
          <!--   Journal Name   -->
          <div class="flex text-textblackdim">
            <input
                class="rounded px-5 py-2 shadow-lg ring-1 ring-opacity-5 transition duration-100 ease-out bg-backg ring-primarylight focus:outline-none"
                id="selected-tree-name-input"
                type="text"
                maxlength="22"
                v-model="tempJournalStore[selectedJournalIndex].journal_name"
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
                  >Couldn't save gratitude journal data to your account. If a refresh
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
                  class="relative flex cursor-pointer items-center text-textblackdim hover:text-gray-600"
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

        <!--   Journal   -->
        <div class="mb-40 w-full sm:mb-10 lg:mb:20">
          <component
              v-show="tempJournalStore.length !== 0 && tempJournalStore[selectedJournalIndex]"
              :is="JournalComponent"
              :journal="tempJournalStore[selectedJournalIndex]"
              :logged-in="loggedIn"
          />
        </div>
      </div>
    </div>
  </div>
</template>
