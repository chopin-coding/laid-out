<script setup lang="ts">
import * as treeHelpers from "../treeHelpers";
import { Tree } from "../interfaces";

interface TreeArray {
  trees: Tree[];
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
    <div v-for="tree in trees" :key="tree.tree_id">
      <span
        v-text="tree.tree_name"
        v-on:click="emit('selectTree', tree.tree_id)"
      ></span>
      <button @click="deleteBtnHandler(tree.tree_id)">Delete</button>
    </div>
    <div>
      <button @click="newTree">Add</button>
    </div>
  </div>
</template>