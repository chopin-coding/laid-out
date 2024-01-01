<script setup lang="ts">
import {nextTick, ref, computed, onMounted} from "vue";
import {Journal} from "../models";
import * as helpers from "../helpers";
import TransitionBasic from "../../transitions/TransitionBasic.vue";
import {useTextareaAutosize} from "@vueuse/core";

interface JournalProps {
  journal: Journal;
  loggedIn: boolean;
}

let props = defineProps<JournalProps>();

function nodeResize() {
  let textarea = document.getElementById("journal-text");

  textarea.style.height = "18px";
  textarea.style.height = textarea.scrollHeight + "px";
}

onMounted(() => {
  nodeResize();
});

</script>
<template>
  <TransitionBasic>
      <textarea
          id="journal-text"
          class="w-full resize-none rounded mb-32 px-2 py-2 align-middle text-sm transition duration-300 ease-out bg-backg placeholder-textblackdimmer2 focus:outline-none"
          placeholder="✎..."
          v-model="journal.journal_data"
          @input="nodeResize"
          rows="1"
          type="text"
      />
  </TransitionBasic>
</template>

<style scoped></style>
