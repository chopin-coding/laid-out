<script setup lang="ts">
import {ref, onMounted, nextTick} from "vue";

import {GoalNode} from "../models";
import GoalComponent from "./GoalComponent.vue";
import TransitionBasic from "../../transitions/TransitionBasic.vue";
import TransitionSlide from "../../transitions/TransitionSlide.vue";

interface GoalNodeProps {
  node: GoalNode;
  loggedIn: boolean;
  hideCompleted: boolean;
  nodeType: "root" | "child";
  singleNodeLeft: boolean;
  parentNodeId: string;
  parentNodeCompleted?: boolean;
}

// defineProps<GoalNode[]>(); doesn't work
let props = defineProps<GoalNodeProps>();

const emit = defineEmits([
  "childBtnHandler",
  "deleteBtnHandler",
  "siblingBtnHandler",
]);

const hovered = ref(false);
const focused = ref(false);
const deleted = ref(false);


function nodeResize() {
  let textarea = document.getElementById(`${props.node.id}-titleInput`);

  textarea.style.height = "18px";
  textarea.style.height = textarea.scrollHeight + "px";
}

async function focusinHandler() {
  focused.value = true;
  await nextTick();
  nodeResize();
}

function handleDelete(
    event: KeyboardEvent,
    title: string,
    singleNodeLeft: boolean,
    nodeType: string,
    nodeId: string
) {
  if (title === "" && (!singleNodeLeft || nodeType !== "root")) {
    event.preventDefault();
    emit("deleteBtnHandler", nodeId);
  }
}

onMounted(() => {
  nodeResize();
});
</script>

<template>
  <TransitionSlide>
    <li
        v-show="!(node.completed && hideCompleted) && !deleted"
        class="pt-1.5"
        :class="{
        'border-l border-textblackdimmer2 ml-3 sm:ml-3 pl-4 sm:pl-4':
          nodeType !== 'root',
      }"
    >
      <div
          class="flex justify-between gap-x-1 group text-textblackdim"
          @mouseover="hovered = true"
          @mouseleave="hovered = false"
      >
        <div class="flex w-full min-w-0 gap-x-1 justify-self-start">
          <!-- controllable/uncontrollable switch -->
          <div class="flex items-center">
            <input v-show="!parentNodeCompleted"
                   class="w-6 h-6 mr-2 custom-checkbox" type="checkbox"
                   v-model="node.completed"/>
          </div>

          <!-- node text -->
          <div class="flex w-full">
            <TransitionBasic>
              <textarea
                  @keydown.enter.exact.prevent.stop="emit('siblingBtnHandler', node.id)"
                  @keydown.tab.exact.prevent.stop="emit('childBtnHandler', node.id)"
                  @keydown.delete.exact.stop="handleDelete($event, node.title, singleNodeLeft, nodeType, props.node.id)"
                  @input="nodeResize"
                  class="w-full resize-none rounded bg-backg px-2 py-2 align-middle text-sm transition duration-300 ease-out placeholder-textblackdimmer2 focus:outline-none"
                  :class="{
                  'text-textblackdimmer2 line-through':
                    parentNodeCompleted || node.completed,
                    'bg-primarylight': focused
                }"
                  placeholder="✎..."
                  rows="1"
                  v-model="node.title"
                  type="text"
                  :id="`${node.id}-titleInput`"
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
                  v-on:click="emit('siblingBtnHandler', node.id)"
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

          <!-- Child node button -->
          <button class="transition duration-100 ease-out hover:text-black"
                  v-on:click="emit('childBtnHandler', node.id)"
                  title="Add child node (↹ Tab)"
          >
            <svg
                viewBox="0 0 24 24"
                class="h-8 w-8"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
              <path
                  d="m13 15 3-3m0 0-3-3m3 3H8m-.8 8h9.6c1.12 0 1.68 0 2.108-.218a2 2 0 0 0 .874-.874C20 18.48 20 17.92 20 16.8V7.2c0-1.12 0-1.68-.218-2.108a2 2 0 0 0-.874-.874C18.48 4 17.92 4 16.8 4H7.2c-1.12 0-1.68 0-2.108.218a2 2 0 0 0-.874.874C4 5.52 4 6.08 4 7.2v9.6c0 1.12 0 1.68.218 2.108a2 2 0 0 0 .874.874C5.52 20 6.08 20 7.2 20Z"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
              />
            </svg>
          </button>

          <!-- Delete node button -->
          <button
              v-show="!singleNodeLeft || nodeType !== 'root'"
              class="transition duration-100 ease-out hover:text-black"
              v-on:click="
              emit('deleteBtnHandler', props.node.id);
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

      <template v-if="node.children?.length > 0">
        <component
            :is="GoalComponent"
            :nodes="node.children"
            :logged-in="loggedIn"
            :hide-completed="hideCompleted"
            :node-type="'child'"
            :parent-node-id="node.id"
            :parent-node-completed="parentNodeCompleted || node.completed"
        />
      </template>
    </li>
  </TransitionSlide>
</template>

<style scoped></style>
