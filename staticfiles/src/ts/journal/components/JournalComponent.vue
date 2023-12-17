<script setup lang="ts">
import {nextTick, ref, computed} from "vue";
import {Journal} from "../models";
import * as helpers from "../helpers";
import TransitionBasic from "../../transitions/TransitionBasic.vue";

interface JournalProps {
  journal: Journal;
  loggedIn: boolean;
}


let props = defineProps<JournalProps>();
</script>

<template>
  <ul
      class="flex list-disc ml-4 flex-col"
  >
    <TransitionBasic>
      <textarea
          class="w-full resize-none rounded px-2 py-2 align-middle text-sm transition duration-300 ease-out bg-backg placeholder-textblackdimmer2 focus:outline-none"
          placeholder="✎..."
          rows="1"
          v-model="journal.journal_data"
          type="text"
      />
    </TransitionBasic>
  </ul>
</template>

<style scoped></style>
