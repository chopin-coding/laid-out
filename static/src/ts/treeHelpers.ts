import { v4 as uuidv4 } from "uuid";
import { Tree, TreeNode } from "./interfaces";
import axios from "axios";

const API_BASE_URL: string = 'http://127.0.0.1:8000/anxiety/api/trees/'

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

export async function axiosGetTrees() {
  try {
    const { data, status } = await axios.get<Tree[]>(
      API_BASE_URL,
      {
        headers: {
          Accept: 'application/json',
        },
      },
    );

    console.log(JSON.stringify(data, null, 4));

    // 👇️ "response status is: 200"
    console.log('response status is: ', status);

    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

function fetchTest() {
  // asd
}
