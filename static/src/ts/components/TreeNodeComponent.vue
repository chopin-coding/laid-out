<script setup lang="ts">
import { nextTick, ref } from "vue";

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
  // TODO auto-grow and shrink textarea based on input length, I can use the id of the element since it's unique
}
</script>

<template>
  <ul>
    <li v-show="!(node.locked && hideUncontrollable)">
      <div
        class="group flex items-center my-0.5 gap-x-0.5"
        @mouseover="isHovered = true"
        @mouseleave="isHovered = false"
      >
        <input
          class="h-3 w-3 my-auto py-auto"
          type="checkbox"
          v-model="node.locked"
        />
        <textarea
          ref="textareaRef"
          class="w-32 resize-none px-1 text-xs rounded placeholder-textblackdimmest group-focus:shadow-inner group-hover:shadow-inner group-hover:shadow-bottom focus:ring-1 focus:ring-primary focus:ring-opacity-5 focus:outline-none"
          aria-multiline="true"
          placeholder="✎..."
          rows="1"
          @input="nodeResize"
          v-model="node.title"
          type="text"
          @keyup.enter.exact="emit('siblingBtnHandler', node.node_id)"
          @keydown.prevent.tab.exact="emit('childBtnHandler', node.node_id)"
          :id="`${node.node_id}-titleInput`"
          @focusin="isFocused = true"
          @focusout="isFocused = false"
        />

        <button
          v-show="isHovered || isFocused"
          class="mx-1 h-3.5 w-3.5"
          @click="emit('childBtnHandler', node.node_id)"
        >
          →
        </button>
        <button
          v-show="isHovered || isFocused"
          class="mx-1 h-3.5 w-3.5"
          @click="emit('siblingBtnHandler', node.node_id)"
        >
          ↓
        </button>
        <button
          v-show="
            (!singleNodeLeft || nodeType !== 'root') && (isHovered || isFocused)
          "
          class="mx-1 h-3.5 w-3.5"
          @click="emit('deleteBtnHandler', node.node_id)"
        >
          ⮾
        </button>
      </div>

      <template v-if="node.children.length > 0">
        <component
          :is="TreeComponent"
          :nodes="node.children"
          :logged-in="loggedIn"
          :hide-uncontrollable="hideUncontrollable"
          :node-type="'child'"
        />
      </template>
    </li>
  </ul>
</template>

<style scoped>
.child-node {
  margin-left: 1rem;
}
</style>
