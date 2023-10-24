<script setup lang="ts">
import { ref } from "vue";

import TreeNodeComponent from "./TreeNodeComponent.vue";
import { TreeNode } from "../interfaces";

interface TreeProps {
  treeNodes: TreeNode[];
  loggedIn: boolean;
  hideUncontrollable: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeProps>();

</script>

<template>


  <component
    :is="TreeNodeComponent"
    :tree-nodes="treeNodes"
    :visibility-toggle="hideUncontrollable"
    :logged-in="loggedIn"
    :node-type="'root'"
  />
</template>

<style scoped></style>