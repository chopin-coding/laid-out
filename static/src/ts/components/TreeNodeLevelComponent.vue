<script setup lang="ts">
import { nextTick, ref } from "vue";

import * as treeHelpers from "../treeHelpers";
import TreeNodeComponent from "./TreeNodeLevelComponent.vue";
import { TreeNode } from "../interfaces";

interface TreeNodeProps {
  treeNodes: TreeNode[];
  loggedIn: boolean;
  visibilityToggle: boolean;
  nodeType: "root" | "child";
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeProps>();

const isHovered = ref(false);
const isFocused = ref(false);

async function childBtnHandler(nodeId: string) {
  const indexToAddTo = props.treeNodes.findIndex(
    (node) => node.node_id === nodeId,
  );

  const nodeToAdd: TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.treeNodes[indexToAddTo].children.push(nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}

async function siblingBtnHandler(nodeId: string) {
  const indexToAddTo =
    props.treeNodes.findIndex((node) => node.node_id === nodeId) + 1;

  const nodeToAdd: TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.treeNodes.splice(indexToAddTo, 0, nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}

function deleteBtnHandler(nodeId: string) {
  const indexToDelete = props.treeNodes.findIndex(
    (node) => node.node_id === nodeId,
  );

  if (indexToDelete !== -1) {
    props.treeNodes.splice(indexToDelete, 1);
  }
}
</script>

<template>
  <ul class="w-60 list-none" :class="{ 'child-node': nodeType !== 'root' }">
    <li
      v-for="node in treeNodes"
      :key="node.node_id"
      v-show="!(node.locked && visibilityToggle)"
    >
      <div
        @mouseover="isHovered = true"
        @mouseleave="isHovered = false"
        @focus="isFocused = true"
      >
        <input
          v-show="isHovered || isFocused"
          type="checkbox"
          v-model="node.locked"
        />
        <input
          class="w-20 rounded shadow-lg focus:ring-1 focus:ring-primary focus:ring-opacity-5 focus:outline-none"
          v-model="node.title"
          type="text"
          @keyup.enter.exact="siblingBtnHandler(node.node_id)"
          @keydown.prevent.tab.exact="childBtnHandler(node.node_id)"
          :id="`${node.node_id}-titleInput`"
        />
        <button class="p-1 text-2xl" @click="childBtnHandler(node.node_id)">
          →
        </button>
        <button
          class="p-1 text-2xl"
          v-show="treeNodes.length > 1 || nodeType !== 'root'"
          @click="deleteBtnHandler(node.node_id)"
        >
          ⮾
        </button>
        <button class="p-1 text-2xl" @click="siblingBtnHandler(node.node_id)">
          ↓
        </button>
      </div>
      <component
        v-if="node.children.length > 0"
        :is="TreeNodeComponent"
        :tree-nodes="node.children"
        :logged-in="loggedIn"
        :visibility-toggle="visibilityToggle"
        :node-type="'child'"
      />
    </li>
  </ul>
</template>

<style scoped>
.child-node {
  margin-left: 1rem;
}
</style>
