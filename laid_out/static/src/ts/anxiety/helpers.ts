import {v4 as uuidv4} from "uuid";
import {Tree, TreeNode} from "./models";
import * as timeUtils from "../timeUtils";
import axios, {AxiosRequestHeaders} from "axios";
import {getCurrentBaseUrl} from "../common_helpers";
import urlJoin from 'url-join';

const baseUrl: string = getCurrentBaseUrl()
let API_BASE_URL: string = null;
const csrftoken: string = (document.querySelector('[name=csrfmiddlewaretoken]') as HTMLInputElement).value;

axios.interceptors.request.use(
  (config) => {
    (config.headers as AxiosRequestHeaders)["X-CSRFTOKEN"] = csrftoken;
    return config;
  },
  (error) => Promise.reject(error)
);


try {
  const apiUri = JSON.parse(
    document.getElementById("ANXIETY-API-BASE-URL").textContent,
  )
  API_BASE_URL = urlJoin(baseUrl, apiUri)
} catch (error) {
  console.log(`Couldn't parse ANXIETY-API-BASE-URL: ${error}`);
}

export function defaultTreeNode(): TreeNode {
  const newNodeId: string = uuidv4();
  return {
    title: "",
    locked: false,
    node_id: newNodeId,
    children: [],
  };
}


function defaultTreeData(): TreeNode[] {
  return [defaultTreeNode()];
}

export function demoTree(): Tree {
  const newTreeId: string = uuidv4();
  return {
    tree_id: newTreeId,
    tree_name: "Tutorial",
    tree_data: [{
      "title": "Welcome to Anxiety!",
      "locked": false,
      "node_id": "7b7308fe-9c1b-4f1a-b081-9463e01ad19c",
      "children": []
    }, {
      "title": "Write down your worries",
      "locked": false,
      "node_id": "ca6d96c7-0149-4ec0-bf84-e2a65600581e",
      "children": []
    }, {
      "title": "Break each worry down",
      "locked": false,
      "node_id": "b28ddc71-7d7f-4e35-a356-c00b5af839a4",
      "children": [{
        "title": "into parts",
        "locked": false,
        "node_id": "55bb6223-6655-4dfd-80e5-27d1935b3b32",
        "children": [{
          "title": "if you like",
          "locked": false,
          "node_id": "41344c91-14a4-439a-a471-fded11f73674",
          "children": []
        }]
      }]
    }, {
      "title": "Cross off the ones that you can't control right now",
      "locked": true,
      "node_id": "a7babe33-46cc-4ff9-88c4-ee16cae90eef",
      "children": []
    }, {
      "title": "Accept the ones you can't control right now",
      "locked": false,
      "node_id": "f7fab8b7-4883-4e67-b765-48b1e239e848",
      "children": []
    }, {
      "title": "Finally, action the rest",
      "locked": false,
      "node_id": "3d4b4f55-ab54-4aa4-a4be-b476e0e5fc7a",
      "children": []
    }, {
      "title": "To get started, create a new anxiety tree!",
      "locked": false,
      "node_id": "19cc5385-aa61-467c-80a6-9f031cd3f715",
      "children": []
    }],
    date_modified: timeUtils.toDjangoTimeString(new Date()),
    date_created: timeUtils.toDjangoTimeString(new Date()),
  };
}

export function defaultTree(
  treeId: string = null,
  treeName: string = null,
  treeData: TreeNode[] = null,
): Tree {
  const newTreeId: string = uuidv4();
  return {
    tree_id: treeId || newTreeId,
    tree_name: treeName || "New Tree",
    tree_data: treeData || defaultTreeData(),
    date_modified: timeUtils.toDjangoTimeString(new Date()),
    date_created: timeUtils.toDjangoTimeString(new Date()),
  };
}

export async function createTree(loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {data, status} = await axios.post(
        API_BASE_URL,
        {},
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          withCredentials: true,
        },
      );

      return data.tree_id;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while creating tree: ", error.message);
        return error.message;
      } else {
        console.log("Error while creating tree: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    const newTree: Tree = defaultTree();
    return newTree.tree_id;
  }
}

export async function updateTree(tree: Tree, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.patch(
        urlJoin(API_BASE_URL, tree.tree_id),
        {tree_name: tree.tree_name, tree_data: tree.tree_data},
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          withCredentials: true,
        },
      );

      return status;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while updating tree: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while updating tree: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 200;
  }
}

export async function deleteTree(treeId: string, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.delete(urlJoin(API_BASE_URL, treeId), {
        withCredentials: true,
      });

      return status;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while deleting tree: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while deleting tree: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 204;
  }
}
