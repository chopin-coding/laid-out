"use strict";

const sample_data = [
  {
    title: "Node 1",
    children: [
      {
        title: "Node 1.1",
        children: [],
      },
      {
        title: "Node 1.2",
        children: [],
      },
    ],
  },
  {
    title: "Node 2",
    children: [
      {
        title: "Node 2.1",
        children: [],
      },
      {
        title: "Node 2.2",
        children: [
          {
            title: "Node 2.2.3",
            children: [],
          },
        ],
      },
    ],
  },
  {
    title: "funny stuff",
    children: [],
  },
  {
    title: "Node 4",
    children: [
      {
        title: "Node 4.1",
        children: [
          {
            title: "Node 4.1.1",
            children: [],
          },
          {
            title: "Node 4.1.2",
            children: [
              {
                title: "some node",
                children: [],
              },
            ],
          },
        ],
      },
    ],
  },
];

function htmlToJSON2(element) {
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
  function createHTMLNode(item) {
    const li = document.createElement("li");
    const input_element = document.createElement("input");
    input_element.value = item.title;
    li.appendChild(input_element);

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
const jsonResult = htmlToJSON2(htmlElement);
console.log(jsonResult);
