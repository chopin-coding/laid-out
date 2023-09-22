import { v4 as uuidv4 } from "uuid";

export interface TreeNode {
  title: string;
  locked: boolean;
  children: TreeNode[];
}

export interface Tree {
  frontendTreeId: string;
  treeName: string;
  treeData: TreeNode[];
}

function defaultTreeData(): TreeNode[] {
  return [
    {
      title: "",
      locked: false,
      children: [],
    },
  ];
}

function createTree(
  treeName: string = null,
  treeData: TreeNode[] = null,
): Tree {
  const newId: string = uuidv4();
  return {
    frontendTreeId: newId,
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
    existingTrees.push(createTree());
  }
  saveTrees(existingTrees);
}

export function getTrees(): Tree[] {
  let trees: string = localStorage.getItem("anxietyTrees") || "[]";
  return JSON.parse(trees);
}

function updateTree(
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

function initLocalStorageTrees() {
  let trees: Tree[] = getTrees();
  if (trees.length === 0) {
    trees.push(createTree());
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

function renderTree(treeData: TreeNode[]) {
  const ul = document.createElement("ul");
  treeData.forEach((item) => {
    ul.appendChild(renderTreeNode(item));
  });

  document.getElementById("tree-root-container").appendChild(ul);
}

function parseHtmlTree() {
  const htmlTreeRoot: HTMLElement = document.getElementById(
    "tree-root-container",
  );
  const treeNodeArray: TreeNode[] = [];

  // Convert HTML Tree Node to TreeNode
  function convertNode(htmlTreeNode): TreeNode {
    const parsedHtmlTreeNode: TreeNode = {
      title: htmlTreeNode.querySelector(":scope > .node-text").value,
      locked: htmlTreeNode.querySelector(":scope > .node-locked").checked,
      children: [],
    };
    const childNodes = htmlTreeNode.querySelectorAll(":scope > ul > li");

    childNodes.forEach((childNode): void => {
      parsedHtmlTreeNode.children.push(convertNode(childNode));
    });
    return parsedHtmlTreeNode;
  }

  const topLevelNodes = htmlTreeRoot.querySelectorAll(":scope > ul > li");
  topLevelNodes.forEach((htmlTreeNode): void => {
    treeNodeArray.push(convertNode(htmlTreeNode));
  });

  return treeNodeArray;
}

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
