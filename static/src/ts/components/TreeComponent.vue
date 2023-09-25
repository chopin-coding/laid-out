<script setup lang="ts">
import { ref } from "vue";

import TreeNodeComponent from "./TreeNodeComponent.vue";
import * as treeHelpers from "../treeHelpers";



interface TreeNodeArray {
  treeNodes: treeHelpers.TreeNode[];
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeNodeArray>();

let visibilityToggle = ref(false)


</script>

<template>
<!-- TODO: global toggle for uncontrollable item visibility -->
  <div>
    <label for="uncontrollable-visibility toggle" >Hide Uncontrollable</label>
    <input id="uncontrollable-visibility toggle" type="checkbox" v-model="visibilityToggle"/>
  </div>
  <component :is="TreeNodeComponent" :tree-nodes="treeNodes" :visibility-toggle="visibilityToggle" />
</template>

<style scoped></style>