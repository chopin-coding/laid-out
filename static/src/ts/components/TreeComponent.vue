<script setup lang="ts">
import TreeNodeComponent from "./TreeNodeComponent.vue";
import * as treeHelpers from "../treeHelpers";



interface TreeNodeArray {
  treeNodes: treeHelpers.TreeNode[];
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeArray>();


</script>

<template>
  <component :is="TreeNodeComponent" :treeNodes="treeNodes" />
</template>

<style scoped></style>