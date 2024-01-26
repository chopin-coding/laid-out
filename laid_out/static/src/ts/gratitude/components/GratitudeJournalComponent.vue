<script setup lang="ts">
import {nextTick, ref, computed} from "vue";

import GratitudeJournalNodeComponent from "./GratitudeJournalNodeComponent.vue";
import {GratitudeJournalNode} from "../models";
import * as helpers from "../helpers";

interface GratitudeJournalProps {
  nodes: GratitudeJournalNode[];
  loggedIn: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<GratitudeJournalProps>();

const singleNodeLeft = computed(() => {
  return props.nodes.length === 1;
});

async function siblingBtnHandler(nodeId: string) {
  const indexToAddTo =
      props.nodes.findIndex((node) => node.node_id === nodeId) + 1;

  const nodeToAdd: GratitudeJournalNode = helpers.defaultGratitudeJournalNode();

  if (indexToAddTo !== -1) {
    props.nodes.splice(indexToAddTo, 0, nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}

async function deleteBtnHandler(nodeId: string) {
  const indexToDelete = props.nodes.findIndex(
      (node) => node.node_id === nodeId,
  );

  let nodeIdToFocus: string | null = null;

  if (props.nodes.length > 1) {
    if (indexToDelete === 0) {
      nodeIdToFocus = props.nodes[indexToDelete + 1].node_id;
    } else {
      nodeIdToFocus = props.nodes[indexToDelete - 1].node_id;
    }
    document.getElementById(`${nodeIdToFocus}-titleInput`).focus();
  }

  // let the animation play out before deleting the node
  await new Promise<void>((resolve) => {
    setTimeout(() => {
      props.nodes.splice(indexToDelete, 1);
      resolve();
    }, 152);
  });
}
</script>

<template>
  <ul
      class="flex list-disc ml-4 flex-col gap-y-1.5"
  >
    <component
        v-for="node in nodes"
        :key="node.node_id"
        :is="GratitudeJournalNodeComponent"
        :node="node"
        :logged-in="loggedIn"
        :single-node-left="singleNodeLeft"
        @delete-btn-handler="(nodeId: string) => deleteBtnHandler(nodeId)"
        @sibling-btn-handler="(nodeId: string) => siblingBtnHandler(nodeId)"
    />
  </ul>
</template>

<style scoped></style>
