<script setup lang="ts">
import * as treeHelpers from "../treeHelpers";
import {Tree} from "../interfaces";

interface TreeListProps {
  trees: Tree[];
  loggedIn: boolean;
}

const emit = defineEmits(["selectTree", "createTree"]);

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeListProps>();

async function newTree(loggedIn: boolean) {
  const treeId = await treeHelpers.createTree(loggedIn)
  const newTree = treeHelpers.defaultTree(treeId)

  props.trees.push(newTree)
  if (loggedIn) {
    emit('createTree', treeId)
  }
}

async function deleteBtnHandler(treeId: string, loggedIn: boolean) {
  const deleteResult = await treeHelpers.deleteTree(treeId, loggedIn)

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
      <button v-show="trees.length > 1" @click="deleteBtnHandler(tree.tree_id, loggedIn)">Delete</button>
    </div>
    <div>
      <button @click="newTree(loggedIn)">Add</button>
    </div>
  </div>
</template>