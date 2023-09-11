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

function htmlToJSON(element) {
  "use strict";

  const result = [];

  function convertNode(node) {
    const item = { title: node.querySelector("input").value, children: [] };
    const childNodes = node.querySelectorAll(":scope > ul > li"); // Selects immediate children

    childNodes.forEach((childNode) => {
      item.children.push(convertNode(childNode));
    });
    return item;
  }

  const topLevelNodes = element.querySelectorAll(":scope > ul > li");
  topLevelNodes.forEach((node) => {
    result.push(convertNode(node));
  });

  return result;
}

function jsonToHTML(data) {
  "use strict";

  function createChildNode(node) {
    const ul = document.createElement("ul");
    node.appendChild(ul);
    const li = document.createElement("li");
    ul.appendChild(li);
    const lockedCheckbox = document.createElement("input");
    const inputElement = document.createElement("input");

    lockedCheckbox.type = "checkbox";
    lockedCheckbox.value = "false";

    li.appendChild(lockedCheckbox);
    li.appendChild(inputElement);

    inputElement.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        createSiblingNode(li);
      }

      if (event.key === "Tab") {
        createChildNode(li);
        event.preventDefault();
      }
    });
    inputElement.focus();
  }

  function createSiblingNode(node) {
    const li = document.createElement("li");
    const lockedCheckbox = document.createElement("input");
    const inputElement = document.createElement("input");

    lockedCheckbox.type = "checkbox";
    lockedCheckbox.value = "false";

    li.appendChild(lockedCheckbox);
    li.appendChild(inputElement);

    node.parentNode.insertBefore(li, node.nextSibling);

    inputElement.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        createSiblingNode(inputElement.parentNode);
      }

      if (event.key === "Tab") {
        createChildNode(li);
        event.preventDefault();
      }
    });
    inputElement.focus();
  }

  function createHTMLNode(item) {
    const li = document.createElement("li");
    const lockedCheckbox = document.createElement("input");
    const inputElement = document.createElement("input");

    inputElement.value = item.title;

    lockedCheckbox.type = "checkbox";
    lockedCheckbox.value = item.locked;

    li.appendChild(lockedCheckbox);
    li.appendChild(inputElement);

    inputElement.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        createSiblingNode(li);
      }
      if (event.key === "Tab") {
        createChildNode(li);
        event.preventDefault();
      }
    });

    if (item.children.length > 0) {
      const ul = document.createElement("ul");
      item.children.forEach((child) => {
        ul.appendChild(createHTMLNode(child));
      });
      li.appendChild(ul);
    }

    return li;
  }

  const ul = document.createElement("ul");
  data.forEach((item) => {
    ul.appendChild(createHTMLNode(item));
  });

  return ul;
}

const containerElement = document.getElementById("tree-root-container");
const htmlResult = jsonToHTML(sample_data);
containerElement.appendChild(htmlResult);

const htmlElement = document.getElementById("tree-root-container");
const jsonResult = htmlToJSON(htmlElement);
// console.log(jsonResult);
