<script setup lang="ts">
import {ref, onMounted, nextTick, watch} from "vue";

import * as helpers from "../helpers";
import GratitudeJournalNodeComponent from "./GratitudeJournalNodeComponent.vue";
import {GratitudeJournalNode} from "../models";
import GratitudeJournalComponent from "./GratitudeJournalComponent.vue";
import TransitionBasic from "../../transitions/TransitionBasic.vue";
import TransitionSlide from "../../transitions/TransitionSlide.vue";

interface GratitudeJournalNodeProps {
  node: GratitudeJournalNode;
  loggedIn: boolean;
  singleNodeLeft: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<GratitudeJournalNodeProps>();

const emit = defineEmits([
  "deleteBtnHandler",
  "siblingBtnHandler",
]);

const hovered = ref(false);
const focused = ref(false);
const deleted = ref(false);

function nodeResize() {
  let textarea = document.getElementById(`${props.node.node_id}-titleInput`);

  textarea.style.height = "18px";
  textarea.style.height = textarea.scrollHeight + "px";
}

async function focusinHandler() {
  focused.value = true;
  await nextTick();
  nodeResize();
}

onMounted(() => {
  nodeResize();
});
</script>

<template>
  <TransitionSlide>
    <li
        v-show="!deleted"
    >
      <div
          class="flex justify-between gap-x-1 group text-textblackdim"
          @mouseover="hovered = true"
          @mouseleave="hovered = false"
      >
        <div class="flex w-full min-w-0 gap-x-1 justify-self-start">
          <!-- node text -->
          <div class="flex w-full">
            <TransitionBasic>
              <textarea
                  @keydown.enter.exact.prevent.stop="
                  emit('siblingBtnHandler', node.node_id)
                "
                  @keydown.delete.exact.stop="
                  node.title === '' && !singleNodeLeft && emit('deleteBtnHandler', props.node.node_id)
                "
                  @input="nodeResize"
                  class="w-full resize-none rounded px-2 py-2 align-middle text-sm transition duration-300 ease-out bg-backg placeholder-textblackdimmer2 focus:outline-none"
                  :class="{
                    'bg-primarylight': focused
                }"
                  placeholder="✎..."
                  rows="1"
                  v-model="node.title"
                  type="text"
                  :id="`${node.node_id}-titleInput`"
                  @focusin="focusinHandler"
                  @focusout="focused = false"
                  data-gramm="false"
                  data-gramm_editor="false"
                  data-enable-grammarly="false"
              />
            </TransitionBasic>
          </div>
        </div>

        <!-- child, sibling, and delete buttons -->
        <div class="flex text-textblackdimmer" v-show="hovered || focused">
          <!-- Sibling node button -->
          <button class="transition duration-100 ease-out hover:text-black"
                  v-on:click="emit('siblingBtnHandler', node.node_id)"
                  title="Add node (↵ Enter)"
          >
            <svg
                viewBox="0 0 24 24"
                class="h-8 w-8"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
              <path
                  d="m9 13 3 3m0 0 3-3m-3 3V8M7.2 20h9.6c1.12 0 1.68 0 2.108-.218a2 2 0 0 0 .874-.874C20 18.48 20 17.92 20 16.8V7.2c0-1.12 0-1.68-.218-2.108a2 2 0 0 0-.874-.874C18.48 4 17.92 4 16.8 4H7.2c-1.12 0-1.68 0-2.108.218a2 2 0 0 0-.874.874C4 5.52 4 6.08 4 7.2v9.6c0 1.12 0 1.68.218 2.108a2 2 0 0 0 .874.874C5.52 20 6.08 20 7.2 20Z"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
              />
            </svg>
          </button>

          <!-- Delete node button -->
          <button
              v-show="!singleNodeLeft"
              class="transition duration-100 ease-out hover:text-black"
              v-on:click="
              emit('deleteBtnHandler', props.node.node_id);
              deleted = true;
            "
              title="Delete node (⌫ Backspace or Delete)"
          >
            <svg
                viewBox="0 0 24 24"
                class="h-8 w-8"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
              <path
                  d="m12 9.5 5 5m0-5-5 5m-7.492-.545 2.932 3.8c.352.457.528.685.75.85a2 2 0 0 0 .652.32c.266.075.554.075 1.131.075H17.8c1.12 0 1.68 0 2.108-.218a2 2 0 0 0 .874-.874C21 17.48 21 16.92 21 15.8V8.2c0-1.12 0-1.68-.218-2.108a2 2 0 0 0-.874-.874C19.481 5 18.92 5 17.8 5H9.973c-.577 0-.865 0-1.13.075a2 2 0 0 0-.653.32c-.222.165-.398.393-.75.85l-2.932 3.8c-.54.7-.81 1.05-.913 1.435a2 2 0 0 0 0 1.04c.104.385.374.735.913 1.435Z"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
              />
            </svg>
          </button>
        </div>
      </div>
    </li>
  </TransitionSlide>
</template>

<style scoped></style>
