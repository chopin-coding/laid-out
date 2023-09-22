<script setup lang="ts">
import { ref } from "vue";
import * as treeHelpers from "../tree";

let trees = ref(treeHelpers.getTrees());

function updateTrees() {
  trees.value = treeHelpers.getTrees();
}

window.addEventListener("tree-storage", updateTrees);

function clearStorage() {
  localStorage.removeItem("anxietyTrees");
}

function newTree() {
  treeHelpers.addTrees();
}

function deleteTreeButton(frontendTreeId: string) {
  treeHelpers.deleteTree(frontendTreeId)
}


</script>

<template>
  <div>
    <button v-on:click="clearStorage">Clear Storage</button>
    <button v-on:click="newTree">New Tree</button>
  </div>
  <div>
    <h2>Trees</h2>
    <div v-for="tree in trees">
<!--    <input :value="tree.treeName" :disabled="">-->
    <button @click="deleteTreeButton(tree.frontendTreeId)">Delete Tree</button>
  </div>
  </div>

</template>
