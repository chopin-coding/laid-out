<script setup lang="ts">
import { ref } from "vue";
import * as treeHelpers from "../treeHelpers";

interface TreeArray {
  trees: treeHelpers.Tree[];
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeArray>();

function newTree() {
  props.trees.push(treeHelpers.defaultTree());
}

function deleteBtnHandler(frontendTreeId: string) {
  const indexToDelete = props.trees.findIndex(
    (tree) => tree.frontendTreeId === frontendTreeId,
  );

  if (indexToDelete !== -1) {
    props.trees.splice(indexToDelete, 1);
  }
}

const emit = defineEmits(["selectTree"]);
</script>

<template>
  <div></div>
  <div>
    <h2>Trees</h2>
    <div v-for="tree in trees" :key="tree.frontendTreeId">
      <span
        v-text="tree.treeName"
        v-on:click="emit('selectTree', tree.frontendTreeId)"
      ></span>
      <button @click="deleteBtnHandler(tree.frontendTreeId)">Delete</button>
    </div>
    <div>
      <button @click="newTree">Add</button>
    </div>
  </div>
</template>
