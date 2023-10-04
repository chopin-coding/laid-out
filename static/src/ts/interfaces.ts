export interface TreeNode {
  title: string;
  locked: boolean;
  node_id: string;
  children: TreeNode[];
}

export interface Tree {
  tree_id: string;
  tree_name: string;
  tree_data: TreeNode[];
}