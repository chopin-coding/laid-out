<script setup lang="ts">
import { ref, computed } from "vue";
import * as treeHelpers from "../treeHelpers";
import * as timeUtils from "../timeUtils";
import { Tree } from "../models";
import TransitionSlide from "../transitions/TransitionSlide.vue";
import TransitionOutInGrow from "../transitions/TransitionOutInGrow.vue";

interface TreeListProps {
  tree: Tree;
  lastRemainingTree: boolean;
  selectedTreeId: string;
  loggedIn: boolean;
}

const emit = defineEmits(["selectTree", "deleteTree"]);

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeListProps>();
const deleted = ref(false);
const loading = ref(false);


async function deleteBtnHandler(treeId: string) {
  loading.value = true;

  const deleteResult = await treeHelpers.deleteTree(treeId, props.loggedIn);

  if (deleteResult === 204) {
    deleted.value = true;

    await new Promise<void>((resolve) => {
      setTimeout(() => {
        emit("deleteTree", treeId);
        resolve();
      }, 152);
    });
  } else {
    // TODO: handle delete tree failure
    loading.value = false;
  }
}
</script>

<template>
  <TransitionSlide>
    <li class="my-2 flex justify-between" v-show="!deleted">
      <!-- Tree name -->
      <a
        href="#"
        class="flex flex-grow flex-col rounded-md px-2 py-2 transition duration-100 ease-out text-textblackdim"
        :class="{
          'bg-primary text-white': tree.tree_id === selectedTreeId,
          'hover:bg-primarylight hover:text-black':
            tree.tree_id !== selectedTreeId,
        }"
        v-on:click="emit('selectTree', tree.tree_id)"
      >
        <span v-text="tree.tree_name"></span>
      <!-- FIXME: displays UTC when a tree is first created -->
        <div v-if="loggedIn"
          class="text-xs text-textblackdimmer2"
          :class="{
            'text-textwhitedimmer2': tree.tree_id === selectedTreeId,
          }"
          v-text="`${timeUtils.formatTimeShort(tree.date_modified)}`"
        ></div>
      </a>

      <button
        class="mx-3 items-center rounded-md px-2 py-2 transition duration-100 ease-out text-textblackdim hover:bg-primarylight hover:text-black"
        v-show="!lastRemainingTree"
        v-on:click="deleteBtnHandler(tree.tree_id)"
      >
        <TransitionOutInGrow duration="50">
          <!-- Delete icon -->
          <svg
            v-if="!loading"
            class="h-7 w-7 text-textblackdim"
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
          <!-- Loading icon -->
          <svg
            v-else-if="loading"
            class="h-7 w-7 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M20 12a8 8 0 0 1-11.76 7.061"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </TransitionOutInGrow>
      </button>
    </li>
  </TransitionSlide>
</template>
