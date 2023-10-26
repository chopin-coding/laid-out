<script setup lang="ts">
import { nextTick, ref, computed } from "vue";

import TreeNodeComponent from "./TreeNodeComponent.vue";
import { TreeNode } from "../interfaces";
import * as treeHelpers from "../treeHelpers";

interface TreeProps {
  nodes: TreeNode[];
  loggedIn: boolean;
  hideUncontrollable: boolean;
  nodeType: "root" | "child";
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeProps>();

const singleNodeLeft = computed(() => {
  return props.nodes.length === 1;
});

async function childBtnHandler(nodeId: string) {
  const indexToAddTo = props.nodes.findIndex((node) => node.node_id === nodeId);

  const nodeToAdd: TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.nodes[indexToAddTo].children.push(nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}

function deleteBtnHandler(nodeId: string) {
  const indexToDelete = props.nodes.findIndex(
    (node) => node.node_id === nodeId,
  );

  if (indexToDelete !== -1) {
    props.nodes.splice(indexToDelete, 1);
  }
}

async function siblingBtnHandler(nodeId: string) {
  const indexToAddTo =
    props.nodes.findIndex((node) => node.node_id === nodeId) + 1;

  const nodeToAdd: TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.nodes.splice(indexToAddTo, 0, nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}
</script>

<template>
  <ul class="w-60 list-none" :class="{ 'child-node': nodeType === 'child', 'root-node': nodeType === 'root' }">
    <component
      v-for="node in nodes"
      :is="TreeNodeComponent"
      :node="node"
      :hide-uncontrollable="hideUncontrollable"
      :logged-in="loggedIn"
      :node-type="nodeType"
      :single-node-left="singleNodeLeft"
      @child-btn-handler="(nodeId: string) => childBtnHandler(nodeId)"
      @delete-btn-handler="(nodeId: string) => deleteBtnHandler(nodeId)"
      @sibling-btn-handler="(nodeId: string) => siblingBtnHandler(nodeId)"
    />
  </ul>
</template>

<style scoped></style>
