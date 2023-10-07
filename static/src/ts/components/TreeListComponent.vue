<script setup lang="ts">
import * as treeHelpers from "../treeHelpers";
import {Tree} from "../interfaces";

interface TreeArray {
  trees: Tree[];
}

const emit = defineEmits(["selectTree", "createTree"]);

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeArray>();

async function newTree() {
  // props.trees.push(treeHelpers.defaultTree());


  const treeId = await treeHelpers.createTree()
  const newTree = treeHelpers.defaultTree(treeId)

  props.trees.push(newTree)
  emit('createTree', treeId)
}

async function deleteBtnHandler(treeId: string) {
  const deleteResult = await treeHelpers.deleteTree(treeId)

  if (deleteResult === 204) {
    const indexToDelete = props.trees.findIndex(
        (tree) => tree.tree_id === treeId,
    );

    if (indexToDelete !== -1) {
      props.trees.splice(indexToDelete, 1);
    }
  }
}


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
      <button v-show="trees.length > 1" @click="deleteBtnHandler(tree.tree_id)">Delete</button>
    </div>
    <div>
      <button @click="newTree">Add</button>
    </div>
  </div>
</template>