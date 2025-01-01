import {v4 as uuidv4} from "uuid";
import {Goal, GoalNode} from "./models";
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
    document.getElementById("GOAL-API-BASE-URL").textContent,
  )
  API_BASE_URL = urlJoin(baseUrl, apiUri)
} catch (error) {
  console.log(`Couldn't parse GOAL-API-BASE-URL: ${error}`);
}

export function defaultGoalNode(): GoalNode {
  const newNodeId: string = uuidv4();
  return {
    title: "",
    completed: false,
    id: newNodeId,
    children: [],
  };
}


function defaultGoalData(): GoalNode[] {
  return [defaultGoalNode()];
}

export function demoGoal(): Goal {
  const newId: string = uuidv4();
  return {
    id: newId,
    name: "Tutorial",
    data: [{
      "title": "Write down your goals precisely",
      "completed": false,
      "id": "ca6d96c7-0149-4ec0-bf84-e2a65600581e",
      "children": []
    }, {
      "title": "Break them",
      "completed": false,
      "id": "b28ddc71-7d7f-4e35-a356-c00b5af839a4",
      "children": [{
        "title": "into parts",
        "completed": false,
        "id": "55bb6223-6655-4dfd-80e5-27d1935b3b32",
        "children": [{
          "title": "if you'd like",
          "completed": false,
          "id": "41344c91-14a4-439a-a471-fded11f73674",
          "children": []
        }]
      }]
    },
      {
        "title": "Optionally check the ones you completed",
        "completed": true,
        "id": "c0ae7a24-06c9-44de-8eb0-f308a24bb365",
        "children": [],
      },
      {
        "title": "Come back here whenever you lose focus",
        "completed": false,
        "id": "560758f6-aa5a-484a-828c-424f58d40d0a",
        "children": [],
      },],
    date_modified: timeUtils.toDjangoTimeString(new Date()),
    date_created: timeUtils.toDjangoTimeString(new Date()),
  };
}

export function defaultGoal(
  id: string = null,
  name: string = null,
  data: GoalNode[] = null,
): Goal {
  const newId: string = uuidv4();
  return {
    id: id || newId,
    name: name || "New Goal List",
    data: data || defaultGoalData(),
    date_modified: timeUtils.toDjangoTimeString(new Date()),
    date_created: timeUtils.toDjangoTimeString(new Date()),
  };
}

export async function createGoal(loggedIn: boolean) {
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

      return data.id;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while creating goal: ", error.message);
        return error.message;
      } else {
        console.log("Error while creating goal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    const newGoal: Goal = defaultGoal();
    return newGoal.id;
  }
}

export async function updateGoal(goal: Goal, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.patch(
        urlJoin(API_BASE_URL, goal.id),
        {name: goal.name, data: goal.data},
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
        console.log("Error while updating goal: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while updating goal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 200;
  }
}

export async function deleteGoal(goalId: string, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.delete(urlJoin(API_BASE_URL, goalId), {
        withCredentials: true,
      });

      return status;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while deleting goal: ", error);
        return error.message;
      } else {
        console.log("Unexpected error while deleting goal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 204;
  }
}
