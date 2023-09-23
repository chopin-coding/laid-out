<script setup lang="ts">
import * as treeHelpers from "../treeHelpers";
import TreeNodeComponent from "./TreeNodeComponent.vue";

interface TreeNodeArray {
  treeNodes: treeHelpers.TreeNode[];
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeArray>();

function childBtnHandler(nodeId: string) {
  const indexToAddTo = props.treeNodes.findIndex(node => node.nodeId === nodeId)

  if (indexToAddTo !== -1) {
    props.treeNodes[indexToAddTo].children.push(treeHelpers.defaultTreeNode())
  }

}

function siblingBtnHandler(nodeId: string) {
  const indexToAddTo = props.treeNodes.findIndex(node => node.nodeId === nodeId)

  if (indexToAddTo !== -1) {
    props.treeNodes.splice(indexToAddTo + 1, 0, treeHelpers.defaultTreeNode());
  }
}

function deleteBtnHandler(nodeId: string) {
  const indexToDelete = props.treeNodes.findIndex(node => node.nodeId === nodeId)

  if (indexToDelete !== -1) {
    props.treeNodes.splice(indexToDelete, 1);
  }
}
</script>

<template>
  <ul >
    <li v-for="node in treeNodes" :key="node.nodeId">
      <input type="checkbox">
      <input v-model="node.title" />
      <button @click="childBtnHandler(node.nodeId)">Add child</button>
      <button @click="siblingBtnHandler(node.nodeId)">Add sibling</button>
      <button @click="deleteBtnHandler(node.nodeId)">Delete</button>
      <component
        v-if="node.children.length > 0"
        :is="TreeNodeComponent"
        :treeNodes="node.children"
      />
    </li>
  </ul>
</template>

<style scoped></style>