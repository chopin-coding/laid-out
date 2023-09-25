<script setup lang="ts">
import { nextTick } from "vue";
import throttle from "lodash/throttle";

import * as treeHelpers from "../treeHelpers";
import TreeNodeComponent from "./TreeNodeComponent.vue";

interface TreeNodeComponentProps {
  treeNodes: treeHelpers.TreeNode[];
  visibilityToggle: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeComponentProps>();

async function childBtnHandler(nodeId: string) {
  const indexToAddTo = props.treeNodes.findIndex(
    (node) => node.nodeId === nodeId,
  );

  const nodeToAdd: treeHelpers.TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.treeNodes[indexToAddTo].children.push(nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.nodeId}-titleInput`).focus();
}

throttle(function () {
  // Your code to create a new element goes here
}, 1000);

async function siblingBtnHandler(nodeId: string) {
  const indexToAddTo =
    props.treeNodes.findIndex((node) => node.nodeId === nodeId) + 1;

  const nodeToAdd: treeHelpers.TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.treeNodes.splice(indexToAddTo, 0, nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.nodeId}-titleInput`).focus();
}

function deleteBtnHandler(nodeId: string) {
  const indexToDelete = props.treeNodes.findIndex(
    (node) => node.nodeId === nodeId,
  );

  if (indexToDelete !== -1) {
    props.treeNodes.splice(indexToDelete, 1);
  }
}
</script>

<template>
  <ul>
    <li
      v-for="node in treeNodes"
      :key="node.nodeId"
      v-show="!(node.locked && visibilityToggle)"
    >
      <input type="checkbox" v-model="node.locked" />
      <input
        v-model="node.title"
        @keyup.enter.exact="siblingBtnHandler(node.nodeId)"
        @keydown.prevent.tab.exact="childBtnHandler(node.nodeId)"
        :id="`${node.nodeId}-titleInput`"
      />
      <button @click="childBtnHandler(node.nodeId)">Add child</button>
      <button @click="siblingBtnHandler(node.nodeId)">Add sibling</button>
      <button @click="deleteBtnHandler(node.nodeId)">Delete</button>
      <component
        v-if="node.children.length > 0"
        :is="TreeNodeComponent"
        :tree-nodes="node.children"
        :visibility-toggle="visibilityToggle"
      />
    </li>
  </ul>
</template>

<style scoped></style>
