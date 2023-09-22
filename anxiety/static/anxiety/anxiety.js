

function uuid4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16),
  );
}

function renderTreeList(treeList = getAnxietyTrees()) {
  const parentContainer = document.getElementById("tree-list-container");

  for (const item of treeList) {
    const treeInfoContainer = document.createElement("div");
    const treeInfo = document.createElement("input");
    treeInfoContainer.appendChild(treeInfo);
    treeInfo.value = item.treeName;
    treeInfo.dataset.frontendTreeId = item.frontendTreeId;
    parentContainer.appendChild(treeInfoContainer);
  }
}

function getAnxietyTrees() {
  let anxietyTrees = localStorage.getItem("anxietyTrees") || "[]";

  return JSON.parse(anxietyTrees);
}

function saveAnxietyTrees(anxietyTrees) {
  localStorage.setItem("anxietyTrees", JSON.stringify(anxietyTrees));
}

function addAnxietyTrees(treesToAdd = null) {
  let existingTrees = getAnxietyTrees();

  if (treesToAdd) {
    for (const tree in treesToAdd) {
      existingTrees.push(tree);
    }
  } else {
    existingTrees.push(newAnxietyTree());
  }
  saveAnxietyTrees(existingTrees);
}

function initializeLocalStorageAnxietyTrees() {
  let anxietyTrees = getAnxietyTrees();
  if (anxietyTrees.length === 0) {
    anxietyTrees.push(newAnxietyTree());
    saveAnxietyTrees(anxietyTrees);
  }
}

function newAnxietyTree(treeName = null, treeData = null) {
  const newTreeId = uuid4();
  return {
    frontendTreeId: newTreeId,
    treeName: treeName || "New Tree",
    treeData: treeData || [
      {
        title: "",
        locked: false,
        children: [],
      },
    ],
  };
}

function initializeAnxietyPage() {
  initializeLocalStorageAnxietyTrees();
  renderAnxietyTree(getAnxietyTrees()[0].treeData);
  renderTreeList();
}

initializeAnxietyPage();

function renderAnxietyTree(treeData) {
  const ul = document.createElement("ul");
  treeData.forEach((item) => {
    ul.appendChild(createNodesRecursive(item));
  });

  document.getElementById("tree-root-container").appendChild(ul);
}

function htmlToJSON() {
  const tree_root = document.getElementById("tree-root-container");

  const result = [];

  function convertNode(node) {
    const tree_node = {
      title: node.querySelector(":scope > .node-text").value,
      locked: node.querySelector(":scope > .node-locked").checked,
      children: [],
    };
    const childNodes = node.querySelectorAll(":scope > ul > li"); // Selects immediate children

    childNodes.forEach((childNode) => {
      tree_node.children.push(convertNode(childNode));
    });
    return tree_node;
  }

  const topLevelNodes = tree_root.querySelectorAll(":scope > ul > li");
  topLevelNodes.forEach((node) => {
    result.push(convertNode(node));
  });

  return result;
}

function createNode(inputValue = null, lockedValue = null) {
  const li = document.createElement("li");
  const lockedCheckbox = document.createElement("input");
  const inputElement = document.createElement("input");
  const deleteNodeButton = document.createElement("button");

  deleteNodeButton.textContent = "Delete";
  lockedCheckbox.type = "checkbox";
  lockedCheckbox.className = "node-locked";
  inputElement.className = "node-text";

  li.appendChild(lockedCheckbox);
  li.appendChild(inputElement);
  li.appendChild(deleteNodeButton);

  if (lockedValue !== null) {
    lockedCheckbox.checked = lockedValue;
  }

  if (inputValue !== null) {
    inputElement.value = inputValue;
  }

  deleteNodeButton.addEventListener("click", function () {
    li.remove();
  });

  inputElement.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      createSiblingNode(li);
    }

    if (event.key === "Tab") {
      createChildNode(li);
      event.preventDefault();
    }
  });

  return {
    li: li,
    lockedCheckbox: lockedCheckbox,
    inputElement: inputElement,
    deleteNodeButton: deleteNodeButton,
  };
}

function createChildNode(node) {
  const ul = document.createElement("ul");
  node.appendChild(ul);

  const { li, lockedCheckbox, inputElement, deleteNodeButton } = createNode();
  ul.appendChild(li);

  inputElement.focus();
}

function createSiblingNode(node) {
  const { li, lockedCheckbox, inputElement, deleteNodeButton } = createNode();

  node.parentNode.insertBefore(li, node.nextSibling);

  inputElement.focus();
}

function createNodesRecursive(item) {
  const { li, lockedCheckbox, inputElement, deleteNodeButton } = createNode(
    item.title,
    item.locked,
  );

  if (item.children.length > 0) {
    const ul = document.createElement("ul");
    item.children.forEach((child) => {
      ul.appendChild(createNodesRecursive(child));
    });
    li.appendChild(ul);
  }

  return li;
}
