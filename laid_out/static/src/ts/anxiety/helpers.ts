import {v4 as uuidv4} from "uuid";
import {Tree, TreeNode} from "./models";
import * as timeUtils from "../timeUtils";
import axios, {AxiosRequestHeaders} from "axios";

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
  API_BASE_URL = JSON.parse(
    document.getElementById("ANXIETY-API-BASE-URL").textContent,
  );
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
        API_BASE_URL + tree.tree_id,
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
      const {status} = await axios.delete(API_BASE_URL + treeId, {
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
