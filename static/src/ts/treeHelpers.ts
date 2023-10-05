import { v4 as uuidv4 } from "uuid";
import { Tree, TreeNode } from "./interfaces";
import axios from "axios";

const API_BASE_URL: string = "http://127.0.0.1:8000/anxiety/api/trees/";

const getCookieValue = (name: string): string =>
  // case sensitive
  document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || "";

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
  treeName: string = null,
  treeData: TreeNode[] = null,
): Tree {
  const newTreeId: string = uuidv4();
  return {
    tree_id: newTreeId,
    tree_name: treeName || "New Tree",
    tree_data: treeData || defaultTreeData(),
  };
}

async function createTree() {
  try {
    const { data, status } = await axios.post<string>(
      API_BASE_URL,
      { name: "John Smith", job: "manager" },
      {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-CSRFTOKEN": getCookieValue("csrftoken"),
        },
        withCredentials: true,
      },
    );

    console.log(JSON.stringify(data, null, 4));

    console.log(status);

    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log("error message: ", error.message);
      // 👇️ error: AxiosError<any, any>
      return error.message;
    } else {
      console.log("unexpected error: ", error);
      return "An unexpected error occurred";
    }
  }
}

export async function getTrees() {
  try {
    const { data, status } = await axios.get<Tree[]>(API_BASE_URL, {
      headers: {
        Accept: "application/json",
      },
    });

    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}

export async function updateTree(tree: Tree) {
  try {
    const { status } = await axios.patch(
      API_BASE_URL + tree.tree_id,
      { tree_name: tree.tree_name, tree_data: tree.tree_data },
      {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-CSRFTOKEN": getCookieValue("csrftoken"),
        },
        withCredentials: true,
      },
    );

    return status;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log("error message: ", error.message);
      // 👇️ error: AxiosError<any, any>
      return error.message;
    } else {
      console.log("unexpected error: ", error);
      return "An unexpected error occurred";
    }
  }
}
