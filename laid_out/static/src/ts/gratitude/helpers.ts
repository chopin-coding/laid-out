import {v4 as uuidv4} from "uuid";
import {GratitudeJournal, GratitudeJournalNode} from "./models";
import * as timeUtils from "../timeUtils";
import axios, {AxiosRequestHeaders} from "axios";
import {getCurrentBaseUrl} from "../common_helpers";
import urlJoin from "url-join";

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
    document.getElementById("GRATITUDE-JOURNAL-API-BASE-URL").textContent,
  )
  API_BASE_URL = urlJoin(baseUrl, apiUri)
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

export function demoGratitudeJournal(): GratitudeJournal {
  const newGJournalId: string = uuidv4();
  return {
    g_journal_id: newGJournalId,
    g_journal_name: "Tutorial",
    g_journal_data: [{
      "title": "Write down things you're grateful for",
      "node_id": "48b1acf5-f2df-4751-9035-af439448d2d4"
    }, {
      "title": "It could be a very small thing that happened today",
      "node_id": "152c94c3-7d16-4ea0-bf79-17d3c2a26ca8"
    }, {
      "title": "Or something bigger and more general",
      "node_id": "efc755be-be18-4e7c-9f6c-56adc684c900"
    }, {
      "title": "You can write down as many or as few as you like",
      "node_id": "f4175def-b4b9-473a-8fc9-7759b5c1f6c4"
    }, {
      "title": "5 items a day is great",
      "node_id": "c881f54a-a947-4963-9cec-9cb95f56a445"
    }, {"title": "To get started, create a new gratitude entry!", "node_id": "7f1704c6-42c3-4ca6-9b45-c4004779c082"}],
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
        urlJoin(API_BASE_URL, gratitudeJournal.g_journal_id),
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
      const {status} = await axios.delete(urlJoin(API_BASE_URL, gJournalId), {
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
