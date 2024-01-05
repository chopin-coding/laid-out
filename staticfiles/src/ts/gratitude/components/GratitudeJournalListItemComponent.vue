<script setup lang="ts">
import { ref, computed } from "vue";
import * as helpers from "../helpers";
import * as timeUtils from "../../timeUtils";
import { GratitudeJournal } from "../models";
import TransitionSlide from "../../transitions/TransitionSlide.vue";
import TransitionOutInGrow from "../../transitions/TransitionOutInGrow.vue";

interface GratitudeJournalListProps {
  gratitudeJournal: GratitudeJournal;
  lastRemainingGratitudeJournal: boolean;
  selectedGratitudeJournalId: string;
  loggedIn: boolean;
}

const emit = defineEmits(["selectGratitudeJournal", "deleteGratitudeJournal"]);

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<GratitudeJournalListProps>();
const deleted = ref(false);
const loading = ref(false);
const deleteConfirmed = ref(false);

async function deleteInTwoStages(treeId: string) {
  if (deleteConfirmed.value) {
    await deleteBtnHandler(treeId);
    deleteConfirmed.value = false;
  } else {
    deleteConfirmed.value = true;
    setTimeout(() => {
      deleteConfirmed.value = false;
    }, 2000);
  }
}

async function deleteBtnHandler(treeId: string) {
  loading.value = true;

  const deleteResult = await helpers.deleteGratitudeJournal(treeId, props.loggedIn);

  if (deleteResult === 204) {
    deleted.value = true;

    await new Promise<void>((resolve) => {
      // for the animation goes through before deleting the tree
      setTimeout(() => {
        emit("deleteGratitudeJournal", treeId);
        resolve();
      }, 152);
    });
  } else {
    // TODO: handle delete tree failure
    loading.value = false;
  }
}
</script>

<template>
  <TransitionSlide>
    <li class="my-2 flex justify-between" v-show="!deleted">
      <!-- Tree name -->
      <div
        class="flex flex-grow cursor-pointer flex-col rounded-md px-2 py-2 transition duration-100 ease-out text-textblackdimmer"
        :class="{
          'bg-primary text-white': gratitudeJournal.g_journal_id === selectedGratitudeJournalId,
          'hover:bg-primarylight hover:text-black':
            gratitudeJournal.g_journal_id !== selectedGratitudeJournalId,
        }"
        v-on:click="emit('selectGratitudeJournal', gratitudeJournal.g_journal_id)"
      >
        <span v-text="gratitudeJournal.g_journal_name"></span>
        <div
          v-if="loggedIn"
          class="text-xs text-textblackdimmer2"
          :class="{
            'text-textwhitedimmer2': gratitudeJournal.g_journal_id === selectedGratitudeJournalId,
          }"
          v-text="`${timeUtils.formatTimeShort(gratitudeJournal.date_modified)}`"
        ></div>
      </div>

      <button
        class="mx-3 items-center rounded-md px-2 py-2 transition duration-100 ease-out text-textblackdimmer hover:bg-primarylight hover:text-black"
        v-show="!lastRemainingGratitudeJournal"
        v-on:click="deleteInTwoStages(gratitudeJournal.g_journal_id)"
      >
        <TransitionOutInGrow duration="50">
          <!-- Delete icon -->
          <svg
            v-if="!loading && !deleteConfirmed"
            class="h-7 w-7"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-label="Delete Tree"
          >
            <path
              d="m18 6-.8 12.013c-.071 1.052-.106 1.578-.333 1.977a2 2 0 0 1-.866.81c-.413.2-.94.2-1.995.2H9.994c-1.055 0-1.582 0-1.995-.2a2 2 0 0 1-.866-.81c-.227-.399-.262-.925-.332-1.977L6 6M4 6h16m-4 0-.27-.812c-.263-.787-.394-1.18-.637-1.471a2 2 0 0 0-.803-.578C13.938 3 13.524 3 12.694 3h-1.388c-.829 0-1.244 0-1.596.139a2 2 0 0 0-.803.578c-.243.29-.374.684-.636 1.471L8 6"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <!-- Warning icon -->
          <svg v-else-if="deleteConfirmed"
            class="h-7 w-7 fill-warning"
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

          <!-- Loading icon -->
          <svg
            v-else-if="loading"
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
    </li>
  </TransitionSlide>
</template>
