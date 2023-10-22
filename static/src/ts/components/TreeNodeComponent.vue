<script setup lang="ts">
import { nextTick } from "vue";
import throttle from "lodash/throttle";

import * as treeHelpers from "../treeHelpers";
import TreeNodeComponent from "./TreeNodeComponent.vue";
import { TreeNode } from "../interfaces";

interface TreeNodeProps {
  treeNodes: TreeNode[];
  loggedIn: boolean;
  visibilityToggle: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeProps>();

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

throttle(function () {
  // Your code to create a new element goes here
}, 1000);

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

// × delete symbol
</script>

<template>
  <ul>
    <li
      v-for="node in treeNodes"
      :key="node.node_id"
      v-show="!(node.locked && visibilityToggle)"
    >
      <input type="checkbox" v-model="node.locked" />
      <input
        v-model="node.title"
        @keyup.enter.exact="siblingBtnHandler(node.node_id)"
        @keydown.prevent.tab.exact="childBtnHandler(node.node_id)"
        :id="`${node.node_id}-titleInput`"
      />
      <button @click="childBtnHandler(node.node_id)">Add child</button>
      <button @click="siblingBtnHandler(node.node_id)">Add sibling</button>
      <button @click="deleteBtnHandler(node.node_id)">Delete</button>
      <component
        v-if="node.children.length > 0"
        :is="TreeNodeComponent"
        :tree-nodes="node.children"
        :logged-in="loggedIn"
        :visibility-toggle="visibilityToggle"
      />
    </li>
  </ul>
</template>

<style scoped></style>