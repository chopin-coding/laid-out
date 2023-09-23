<script setup lang="ts">
import { ref } from "vue";
import * as treeHelpers from "../treeHelpers";

interface TreeArray {
  trees: treeHelpers.Tree[];
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeArray>();

function clearStorage() {
  localStorage.removeItem("anxietyTrees");
}

function newTree() {
  props.trees.push(treeHelpers.defaultTree())
}

function deleteBtnHandler(frontendTreeId: string) {
  const indexToDelete = props.trees.findIndex(tree => tree.frontendTreeId === frontendTreeId)

  if (indexToDelete !== -1) {
    props.trees.splice(indexToDelete, 1)
  }
}


// v-on:click="treeBtnHandler(tree.frontendTreeId)"
</script>

<template>
  <div>
  </div>
  <div>
    <h2>Trees</h2>
    <div v-for="tree in trees" :key="tree.frontendTreeId">
      <input
        v-model="tree.treeName"
      />
      <button @click="deleteBtnHandler(tree.frontendTreeId)">Delete</button>
    </div>
    <div>
      <button @click="newTree">
        Add
      </button>
    </div>
  </div>
</template>
