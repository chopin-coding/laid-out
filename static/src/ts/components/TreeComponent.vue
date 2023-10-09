<script setup lang="ts">
import { ref } from "vue";

import TreeNodeComponent from "./TreeNodeComponent.vue";
import { TreeNode } from "../interfaces";

interface TreeProps {
  treeNodes: TreeNode[];
  loggedIn: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeProps>();

let visibilityToggle = ref(false);
</script>

<template>
  <div>
    <label for="uncontrollable-visibility toggle">Hide Uncontrollable</label>
    <input
      id="uncontrollable-visibility toggle"
      type="checkbox"
      v-model="visibilityToggle"
    />
  </div>

  <component
    :is="TreeNodeComponent"
    :tree-nodes="treeNodes"
    :visibility-toggle="visibilityToggle"
    :logged-in="loggedIn"
  />
</template>

<style scoped></style>