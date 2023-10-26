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
</script>

<template>
  <ul>
    <li v-show="!(node.locked && hideUncontrollable)">
      <div @mouseover="isHovered = true" @mouseleave="isHovered = false">
        <input
          v-show="isHovered || isFocused"
          type="checkbox"
          v-model="node.locked"
        />
        <input
          class="w-32 px-1 m-1 rounded shadow-lg focus:ring-1 focus:ring-primary focus:ring-opacity-5 focus:outline-none"
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
          class="px-1 text-2xl"
          @click="emit('childBtnHandler', node.node_id)"
        >
          →
        </button>
        <button
          v-show="isHovered || isFocused"
          class="px-1 text-2xl"
          @click="emit('siblingBtnHandler', node.node_id)"
        >
          ↓
        </button>
        <button
          v-show="(!singleNodeLeft || nodeType !== 'root') && (isHovered || isFocused)"
          class="px-1 text-2xl"
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
