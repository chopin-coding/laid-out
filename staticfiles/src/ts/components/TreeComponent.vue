<script setup lang="ts">
import { nextTick, ref, computed } from "vue";

import TreeNodeComponent from "./TreeNodeComponent.vue";
import { TreeNode } from "../models";
import * as treeHelpers from "../treeHelpers";

interface TreeProps {
  nodes: TreeNode[];
  loggedIn: boolean;
  hideUncontrollable: boolean;
  nodeType: "root" | "child";
  parentNodeId: string;
  parentNodeLocked?: boolean;
}

// defineProps<TreeNode[]>(); doesn't work
let props = defineProps<TreeProps>();

const singleNodeLeft = computed(() => {
  return props.nodes.length === 1;
});

async function childBtnHandler(nodeId: string) {
  const indexToAddTo = props.nodes.findIndex((node) => node.node_id === nodeId);

  const nodeToAdd: TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.nodes[indexToAddTo].children.push(nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}

async function siblingBtnHandler(nodeId: string) {
  const indexToAddTo =
    props.nodes.findIndex((node) => node.node_id === nodeId) + 1;

  const nodeToAdd: TreeNode = treeHelpers.defaultTreeNode();

  if (indexToAddTo !== -1) {
    props.nodes.splice(indexToAddTo, 0, nodeToAdd);
  }

  await nextTick();
  document.getElementById(`${nodeToAdd.node_id}-titleInput`).focus();
}

async function deleteBtnHandler(nodeId: string, parentNodeId: string) {
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
    // try {
    //   nodeIdToFocus = props.nodes[indexToDelete].node_id;
    // } catch {
    //   nodeIdToFocus = props.nodes[indexToDelete - 1].node_id;
    // } finally {
    //   document.getElementById(`${nodeIdToFocus}-titleInput`).focus();
    // }
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

  // // let the animation play out before deleting the node
  // await new Promise<void>((resolve) => {
  //   setTimeout(() => {
  //     props.nodes.splice(indexToDelete, 1);
  //     resolve();
  //   }, 152);
  // });
  //
  // await nextTick();
  //
  // let nodeIdToFocus: string | null = null;
  //
  // if (props.nodes.length > 0) {
  //   try {
  //     nodeIdToFocus = props.nodes[indexToDelete].node_id;
  //   } catch {
  //     nodeIdToFocus = props.nodes[indexToDelete - 1].node_id;
  //   } finally {
  //     document.getElementById(`${nodeIdToFocus}-titleInput`).focus();
  //   }
  // } else if (props.nodes.length === 0) {
  //   try {
  //     document.getElementById(`${parentNodeId}-titleInput`).focus();
  //   } catch (error) {
  //     console.log(`couldn't focus parent node: ${error}`);
  //   }
  // }
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
      :key="node.node_id"
      :is="TreeNodeComponent"

      :node="node"
      :parent-node-id="parentNodeId"
      :hide-uncontrollable="hideUncontrollable"
      :logged-in="loggedIn"
      :node-type="nodeType"
      :single-node-left="singleNodeLeft"
      :parent-node-locked="parentNodeLocked || node.locked"
      @child-btn-handler="(nodeId: string) => childBtnHandler(nodeId)"
      @delete-btn-handler="
        (nodeId: string) => deleteBtnHandler(nodeId, parentNodeId)
      "
      @sibling-btn-handler="(nodeId: string) => siblingBtnHandler(nodeId)"
    />
  </ul>
</template>

<style scoped></style>
