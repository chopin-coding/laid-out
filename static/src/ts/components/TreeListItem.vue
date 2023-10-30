<script setup lang="ts">
import { ref } from "vue";
import * as treeHelpers from "../treeHelpers";
import { Tree } from "../interfaces";
import TransitionSlide from "../transitions/TransitionSlide.vue";

interface TreeListProps {
  tree: Tree;
  isLastRemainingTree: boolean;
  selectedTreeId: string;
}

const emit = defineEmits(["selectTree", "deleteTree"]);

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeListProps>();

const deleted = ref(false);
</script>

<template>
  <li class="my-2" v-show="!deleted">
    <a
      href="#"
      class="flex transition ease-out duration-100 items-center text-textblackdim justify-between rounded-md px-2 py-2 hover:bg-primarylight hover:text-black"
      :class="{
        'text-black bg-primarylight': tree.tree_id === selectedTreeId,
      }"
      v-on:click="emit('selectTree', tree.tree_id)"
    >
      <span class="" v-text="tree.tree_name"> </span>
      <button
        class="items-end text-textblackdim"
        v-show="!isLastRemainingTree"
        @click="emit('deleteTree', tree.tree_id)"
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
</template>
