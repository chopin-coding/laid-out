import { v4 as uuidv4 } from "uuid";

export interface TreeNode {
  title: string
  locked: boolean
  nodeId: string
  children: TreeNode[];
}

export interface Tree {
  frontendTreeId: string
  treeName: string
  treeData: TreeNode[]
}

export function defaultTreeNode(): TreeNode {
  const newNodeId: string = uuidv4();
  return {
      title: "",
      locked: false,
      nodeId: newNodeId,
      children: [],
    }
}

function defaultTreeData(): TreeNode[] {
  return [
    defaultTreeNode()
  ];
}

export function defaultTree(
  treeName: string = null,
  treeData: TreeNode[] = null,
): Tree {
  const newFrontendTreeId: string = uuidv4();
  return {
    frontendTreeId: newFrontendTreeId,
    treeName: treeName || "New Tree",
    treeData: treeData || defaultTreeData(),
  };
}

export function addTrees(treesToAdd: Tree[] = null): void {
  let existingTrees: Tree[] = getTrees();

  if (treesToAdd) {
    for (const tree of treesToAdd) {
      existingTrees.push(tree);
    }
  } else {
    existingTrees.push(defaultTree());
  }
  saveTrees(existingTrees);
}

export function getTrees(): Tree[] {
  let trees: string = localStorage.getItem("anxietyTrees") || "[]";
  return JSON.parse(trees);
}

export function getTreeDataByFrontendTreeId(
  frontendTreeId: string,
): TreeNode[] {
  const trees: Tree[] = getTrees();
  const indexToReturn: number = trees.findIndex(
    (tree: Tree): boolean => tree.frontendTreeId === frontendTreeId,
  );

  return trees[indexToReturn].treeData;
}

export function updateTree(
  frontendTreeId: string,
  treeName: string = null,
  treeData: TreeNode[] = null,
): void {
  let trees: Tree[] = getTrees();

  const indexToUpdate: number = trees.findIndex(
    (tree: Tree): boolean => tree.frontendTreeId === frontendTreeId,
  );

  if (indexToUpdate !== -1) {
    if (treeName !== null) {
      trees[indexToUpdate].treeName = treeName;
    }
    if (treeData !== null) {
      trees[indexToUpdate].treeData = treeData;
    }
  }

  saveTrees(trees);
}

export function deleteTree(frontendTreeId: string): void {
  let trees: Tree[] = getTrees();

  const indexToDelete = trees.findIndex(
    (tree) => tree.frontendTreeId === frontendTreeId,
  );
  if (indexToDelete !== -1) {
    trees.splice(indexToDelete, 1);
  }

  saveTrees(trees);
}

function saveTrees(trees: Tree[]) {
  localStorage.setItem("anxietyTrees", JSON.stringify(trees));
  window.dispatchEvent(new Event("tree-storage"));
}

export function initLocalStorageTrees() {
  let trees: Tree[] = getTrees();
  if (trees.length === 0) {
    trees.push(defaultTree());
    saveTrees(trees);
  }
}

export function initTreePage(): void {
  initLocalStorageTrees();
  renderTree(getTrees()[0].treeData); // the first tree
}

function renderTreeNode(treeNode: TreeNode) {
  const { htmlTreeNode } = createNode(treeNode.title, treeNode.locked);

  if (treeNode.children.length > 0) {
    const ul = document.createElement("ul");
    treeNode.children.forEach((child) => {
      ul.appendChild(renderTreeNode(child));
    });
    htmlTreeNode.appendChild(ul);
  }

  return htmlTreeNode;
}

export function renderTree(treeData: TreeNode[]): HTMLElement {
  const rootEl = document.createElement("div");
  rootEl.id = "tree-root-container";
  const ul = document.createElement("ul");
  treeData.forEach((item) => {
    ul.appendChild(renderTreeNode(item));
  });

  rootEl.appendChild(ul);
  return rootEl;
}

// function parseHtmlTree() {
//   const htmlTreeRoot: HTMLElement = document.getElementById(
//     "tree-root-container",
//   );
//   const treeNodeArray: TreeNode[] = [];
//
//   // Convert HTML TreeHelpers Node to TreeNode
//   function convertNode(htmlTreeNode): TreeNode {
//     const parsedHtmlTreeNode: TreeNode = {
//       title: htmlTreeNode.querySelector(":scope > .node-text").value,
//       locked: htmlTreeNode.querySelector(":scope > .node-locked").checked,
//       children: [],
//     };
//     const childNodes = htmlTreeNode.querySelectorAll(":scope > ul > li");
//
//     childNodes.forEach((childNode): void => {
//       parsedHtmlTreeNode.children.push(convertNode(childNode));
//     });
//     return parsedHtmlTreeNode;
//   }
//
//   const topLevelNodes = htmlTreeRoot.querySelectorAll(":scope > ul > li");
//   topLevelNodes.forEach((htmlTreeNode): void => {
//     treeNodeArray.push(convertNode(htmlTreeNode));
//   });
//
//   return treeNodeArray;
// }

function createNode(title: string = null, locked: boolean = null) {
  const htmlTreeNode: HTMLLIElement = document.createElement("li");
  const lockedElement = document.createElement("input");
  const titleElement = document.createElement("input");
  const deleteNodeButton = document.createElement("button");

  deleteNodeButton.textContent = "Delete";
  lockedElement.type = "checkbox";
  lockedElement.className = "node-locked";
  titleElement.className = "node-text";

  htmlTreeNode.appendChild(lockedElement);
  htmlTreeNode.appendChild(titleElement);
  htmlTreeNode.appendChild(deleteNodeButton);

  if (locked !== null) {
    lockedElement.checked = locked;
  }

  if (title !== null) {
    titleElement.value = title;
  }

  deleteNodeButton.addEventListener("click", function () {
    htmlTreeNode.remove();
  });

  titleElement.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      createSiblingNode(htmlTreeNode);
    }

    if (event.key === "Tab") {
      createChildNode(htmlTreeNode);
      event.preventDefault();
    }
  });

  return {
    htmlTreeNode: htmlTreeNode,
    lockedCheckbox: lockedElement,
    title: titleElement,
    deleteNodeButton: deleteNodeButton,
  };
}

function createChildNode(htmlNode: HTMLElement): void {
  const ul: HTMLUListElement = document.createElement("ul");
  htmlNode.appendChild(ul);

  const { htmlTreeNode, title } = createNode();
  ul.appendChild(htmlTreeNode);

  title.focus();
}

function createSiblingNode(htmlNode: HTMLElement) {
  const { htmlTreeNode, title } = createNode();

  htmlNode.parentNode.insertBefore(htmlTreeNode, htmlNode.nextSibling);

  title.focus();
}
