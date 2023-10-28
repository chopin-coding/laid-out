<script setup lang="ts">
import * as treeHelpers from "../treeHelpers";
import { Tree } from "../interfaces";

interface TreeListProps {
  trees: Tree[];
  loggedIn: boolean;
  selectedTreeId: string;
}

const emit = defineEmits(["selectTree", "createTree"]);

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeListProps>();

async function newTree(loggedIn: boolean) {
  const treeId = await treeHelpers.createTree(loggedIn);
  const newTree = treeHelpers.defaultTree(treeId);

  props.trees.push(newTree);
  if (loggedIn) {
    emit("createTree", treeId);
  }
}

async function deleteBtnHandler(treeId: string, loggedIn: boolean) {
  const deleteResult = await treeHelpers.deleteTree(treeId, loggedIn);

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
  <div class="divide-y divide-solid divide-primarylight">
    <div class="py-2 my-1 text-center text-xl text-textblackdim">Trees</div>
    <ul class="list-none">
      <li class="my-2" v-for="tree in trees" :key="tree.tree_id">
        <a
          href="#" class="flex items-center text-textblackdim justify-between rounded-md px-2 py-2 hover:bg-primarylight hover:text-black"
          :class="{ 'text-black bg-primarylight': tree.tree_id === selectedTreeId }"
          v-on:click="emit('selectTree', tree.tree_id)"
        >
          <span class="" v-text="tree.tree_name"> </span>
          <button
            class="items-end text-textblackdim"
            v-show="trees.length > 1"
            @click="deleteBtnHandler(tree.tree_id, loggedIn)"
          >
          <!-- Delete icon -->
            <svg
              class="h-7 w-7"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-label="Delete Tree"
            >
              <path
                d="m18 6-.8 12.013c-.071 1.052-.106 1.578-.333 1.977a2 2 0 0 1-.866.81c-.413.2-.94.2-1.995.2H9.994c-1.055 0-1.582 0-1.995-.2a2 2 0 0 1-.866-.81c-.227-.399-.262-.925-.332-1.977L6 6M4 6h16m-4 0-.27-.812c-.263-.787-.394-1.18-.637-1.471a2 2 0 0 0-.803-.578C13.938 3 13.524 3 12.694 3h-1.388c-.829 0-1.244 0-1.596.139a2 2 0 0 0-.803.578c-.243.29-.374.684-.636 1.471L8 6"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </a>
      </li>
    </ul>

    <div>
      <button
        class="my-2 rounded-md px-1 py-2 hover:bg-primarylight hover:text-black"
        @click="newTree(loggedIn)"
      >
        <!-- New Tree icon -->
        <svg
          class="h-7 w-7 text-textblackdim"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-label="Add Tree"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M10 1a1 1 0 0 0-.707.293l-6 6A1 1 0 0 0 3 8v12a3 3 0 0 0 3 3h8a1 1 0 1 0 0-2H6a1 1 0 0 1-1-1V9h5a1 1 0 0 0 1-1V3h7a1 1 0 0 1 1 1v4a1 1 0 1 0 2 0V4a3 3 0 0 0-3-3h-8ZM9 7H6.414L9 4.414V7Zm11 5a1 1 0 1 0-2 0v3h-3a1 1 0 1 0 0 2h3v3a1 1 0 1 0 2 0v-3h3a1 1 0 1 0 0-2h-3v-3Z"
            fill="currentColor"
          />
        </svg>
      </button>
    </div>
  </div>
</template>
