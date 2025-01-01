<script setup lang="ts">
import { nextTick, ref, computed } from "vue";

import GoalNodeComponent from "./GoalNodeComponent.vue";
import { GoalNode } from "../models";
import * as helpers from "../helpers";

interface GoalProps {
  nodes: GoalNode[];
  loggedIn: boolean;
  hideCompleted: boolean;
  nodeType: "root" | "child";
  parentNodeId: string;
  parentNodeCompleted?: boolean;
}

// defineProps<GoalNode[]>(); doesn't work
let props = defineProps<GoalProps>();

const singleNodeLeft = computed(() => {
  return props.nodes.length === 1;
});

async function childBtnHandler(nodeId: string) {
  const indexToAddTo = props.nodes.findIndex((node) => node.id === nodeId);

  const nodeToAdd: GoalNode = helpers.defaultGoalNode();

  if (indexToAddTo !== -1) {
    props.nodes[indexToAddTo].children.push(nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.id}-titleInput`).focus();
}

async function siblingBtnHandler(nodeId: string) {
  const indexToAddTo =
    props.nodes.findIndex((node) => node.id === nodeId) + 1;

  const nodeToAdd: GoalNode = helpers.defaultGoalNode();

  if (indexToAddTo !== -1) {
    props.nodes.splice(indexToAddTo, 0, nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.id}-titleInput`).focus();
}

async function deleteBtnHandler(nodeId: string, parentNodeId: string) {
  const indexToDelete = props.nodes.findIndex(
    (node) => node.id === nodeId,
  );

  let nodeIdToFocus: string | null = null;

  if (props.nodes.length > 1) {
    if (indexToDelete === 0) {
      nodeIdToFocus = props.nodes[indexToDelete + 1].id;
    } else {
      nodeIdToFocus = props.nodes[indexToDelete - 1].id;
    }
    document.getElementById(`${nodeIdToFocus}-titleInput`).focus();

  } else if (props.nodes.length === 1) {
    try {
      document.getElementById(`${parentNodeId}-titleInput`).focus();
    } catch (error) {
      console.log(`couldn't focus parent node: ${error}`);
    }
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
    class="flex list-none flex-col"
    :class="{
      'child-node': nodeType === 'child',
      'root-node': nodeType === 'root',
    }"
  >
    <component
      v-for="node in nodes"
      :key="node.id"
      :is="GoalNodeComponent"

      :node="node"
      :parent-node-id="parentNodeId"
      :hide-completed="hideCompleted"
      :logged-in="loggedIn"
      :node-type="nodeType"
      :single-node-left="singleNodeLeft"
      :parent-node-completed="parentNodeCompleted"
      @child-btn-handler="(nodeId: string) => childBtnHandler(nodeId)"
      @delete-btn-handler="
        (nodeId: string) => deleteBtnHandler(nodeId, parentNodeId)
      "
      @sibling-btn-handler="(nodeId: string) => siblingBtnHandler(nodeId)"
    />
  </ul>
</template>

<style scoped></style>
