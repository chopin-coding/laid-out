export interface GoalNode {
  title: string;
  completed: boolean;
  id: string;
  children: GoalNode[];
}

export interface Goal {
  id: string;
  name: string;
  data: GoalNode[];
  date_created: string;
  date_modified: string;
}
