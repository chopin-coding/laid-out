import {v4 as uuidv4} from "uuid";
import {GratitudeJournal, GratitudeJournalNode} from "./models";
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
    document.getElementById("GRATITUDE-JOURNAL-API-BASE-URL").textContent,
  );
} catch (error) {
  console.log(`Couldn't parse GRATITUDE-JOURNAL-API-BASE-URL: ${error}`);
}

export function defaultGratitudeJournalNode(): GratitudeJournalNode {
  const newNodeId: string = uuidv4();
  return {
    title: "",
    node_id: newNodeId,
  };
}

function defaultGratitudeJournalData(): GratitudeJournalNode[] {
  return [defaultGratitudeJournalNode()];
}

export function defaultGratitudeJournal(
  gJournalId: string = null,
  gJournalName: string = null,
  gJournalData: GratitudeJournalNode[] = null,
): GratitudeJournal {
  const newGJournalId: string = uuidv4();
  return {
    g_journal_id: gJournalId || newGJournalId,
    g_journal_name: gJournalName || "New Gratitude",
    g_journal_data: gJournalData || defaultGratitudeJournalData(),
    date_modified: timeUtils.toDjangoTimeString(new Date()),
    date_created: timeUtils.toDjangoTimeString(new Date()),
  };
}

export async function createGratitudeJournal(loggedIn: boolean) {
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

      return data.g_journal_id;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while creating gratitude journal: ", error.message);
        return error.message;
      } else {
        console.log("Error while creating gratitude journal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    const newGratitudeJournal: GratitudeJournal = defaultGratitudeJournal();
    return newGratitudeJournal.g_journal_id;
  }
}

export async function updateGratitudeJournal(gratitudeJournal: GratitudeJournal, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.patch(
        API_BASE_URL + gratitudeJournal.g_journal_id,
        {g_journal_name: gratitudeJournal.g_journal_name, g_journal_data: gratitudeJournal.g_journal_data},
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
        console.log("Error while updating gratitude journal: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while updating gratitude journal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 200;
  }
}

export async function deleteGratitudeJournal(gJournalId: string, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.delete(API_BASE_URL + gJournalId, {
        withCredentials: true,
      });

      return status;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while deleting gratitude journal: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while deleting gratitude journal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 204;
  }
}
