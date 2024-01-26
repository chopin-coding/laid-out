<script setup lang="ts">
import {Journal} from "../models";
import TransitionBasic from "../../transitions/TransitionBasic.vue";

interface JournalProps {
  journal: Journal;
  loggedIn: boolean;
}

let props = defineProps<JournalProps>();


</script>
<template>
  <TransitionBasic>
      <textarea
          id="journal-text"
          class="w-full h-96 ring-1 ring-opacity-5 ring-primarylight resize rounded mb-32 px-2 py-2 align-middle text-sm transition duration-300 ease-out bg-backg placeholder-textblackdimmer2 focus:outline-none focus:ring-primary"
          placeholder="✎..."
          v-model="journal.journal_data"
          rows="1"
          type="text"
      />
  </TransitionBasic>
</template>

<style scoped></style>
