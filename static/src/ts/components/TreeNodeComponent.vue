<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";

import * as treeHelpers from "../treeHelpers";
import TreeNodeComponent from "./TreeNodeComponent.vue";
import { TreeNode } from "../interfaces";
import TreeComponent from "./TreeComponent.vue";

interface TreeNodeProps {
  node: TreeNode;
  loggedIn: boolean;
  hideUncontrollable: boolean;
  nodeType: "root" | "child";
  singleNodeLeft: boolean;
  parentNodeId: string;
  parentNodeLocked: boolean
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeProps>();

const emit = defineEmits([
  "childBtnHandler",
  "deleteBtnHandler",
  "siblingBtnHandler",
]);

const isHovered = ref(false);
const isFocused = ref(false);

function nodeResize() {
  let textarea = document.getElementById(`${props.node.node_id}-titleInput`);

  textarea.style.height = "18px";
  textarea.style.height = textarea.scrollHeight + "px";
}

async function focusinHandler() {
  isFocused.value = true;
  await nextTick();
  nodeResize();
}

onMounted(() => {
  nodeResize();
});
</script>

<template>
  <ul>
    <li v-show="!(node.locked && hideUncontrollable)">
      <div
        class="flex justify-between gap-x-1 group text-textblackdim"
        @mouseover="isHovered = true"
        @mouseleave="isHovered = false"
      >
        <div class="flex gap-x-1 justify-self-start min-w-0">
          <!-- controllable/uncontrollable switch -->
          <div class="flex">
            <button
              class="text-textblackdim"
              v-on:click="node.locked = !node.locked"
            >
              <!-- Locked icon -->
              <svg
                v-show="node.locked"
                class="h-6 w-6"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M7 10.029C7.471 10 8.053 10 8.8 10h6.4c.747 0 1.329 0 1.8.029m-10 0c-.588.036-1.006.117-1.362.298a3 3 0 0 0-1.311 1.311C4 12.28 4 13.12 4 14.8v1.4c0 1.68 0 2.52.327 3.162a3 3 0 0 0 1.311 1.311C6.28 21 7.12 21 8.8 21h6.4c1.68 0 2.52 0 3.162-.327a3 3 0 0 0 1.311-1.311C20 18.72 20 17.88 20 16.2v-1.4c0-1.68 0-2.52-.327-3.162a3 3 0 0 0-1.311-1.311c-.356-.181-.774-.262-1.362-.298m-10 0V8a5 5 0 0 1 10 0v2.029"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <!-- Unlocked icon -->
              <svg
                v-show="!node.locked"
                class="h-6 w-6"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M16.584 6A5.001 5.001 0 0 0 7 8v2.029m0 0C7.471 10 8.053 10 8.8 10h6.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C20 12.28 20 13.12 20 14.8v1.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C17.72 21 16.88 21 15.2 21H8.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C4 18.72 4 17.88 4 16.2v-1.4c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311c.356-.181.774-.262 1.362-.298Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>

          <!-- node text -->
          <div class="flex">
            <textarea
              @keydown.enter.exact.prevent.stop="
                emit('siblingBtnHandler', node.node_id)
              "
              @keydown.tab.exact.prevent.stop="
                emit('childBtnHandler', node.node_id)
              "
              @input="nodeResize"
              class="resize-none bg-backg rounded w-full px-1 align-middle py-2 placeholder-textblackdimmer2 focus:outline-none"
              :class="{ 'text-textblackdimmer2 line-through': parentNodeLocked || node.locked }"
              placeholder="✎..."
              rows="1"
              v-model="node.title"
              type="text"
              :id="`${node.node_id}-titleInput`"
              @focusin="focusinHandler"
              @focusout="isFocused = false"
            />
          </div>
        </div>

        <!-- child, sibling, and delete buttons -->
        <div class="flex" v-show="isHovered || isFocused">
          <!-- Sibling node button -->
          <button class="" @click="emit('siblingBtnHandler', node.node_id)">
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
          <button class="" @click="emit('childBtnHandler', node.node_id)">
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
            class=""
            @click="emit('deleteBtnHandler', node.node_id)"
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

      <template v-if="node.children.length > 0">
        <component
          :is="TreeComponent"
          :nodes="node.children"
          :logged-in="loggedIn"
          :hide-uncontrollable="hideUncontrollable"
          :node-type="'child'"
          :parent-node-id="node.node_id"
          :parent-node-locked="parentNodeLocked || node.locked"
        />
      </template>
    </li>
  </ul>
</template>

<style scoped>
/* make this different for mobile and desktop */
.child-node {
  margin-left: 1em;
}
</style>
