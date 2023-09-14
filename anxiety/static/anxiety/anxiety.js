const sample_data = [
  {
    title: "Node 1",
    locked: false,
    children: [
      {
        title: "Node 1.1",
        locked: false,
        children: [],
      },
      {
        title: "Node 1.2",
        locked: false,
        children: [],
      },
    ],
  },
];

function htmlToJSON() {
  "use strict";

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

function jsonToHTML(data) {
  "use strict";

  function createNode(input_value = null, locked_value = null) {
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

    if (locked_value !== null) {
      lockedCheckbox.checked = locked_value;
    }

    if (input_value !== null) {
      inputElement.value = input_value;
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

  const ul = document.createElement("ul");
  data.forEach((item) => {
    ul.appendChild(createNodesRecursive(item));
  });

  return ul;
}

const containerElement = document.getElementById("tree-root-container");
const htmlResult = jsonToHTML(sample_data);
containerElement.appendChild(htmlResult);

const jsonResult = htmlToJSON();
console.log(jsonResult);

const newTreeButtonContainer = document.getElementById(
  "new-tree-button-container",
);
const newTreeButton = document.getElementById("newTree-button");
newTreeButton.addEventListener("click", function () {
  li.remove();
});
