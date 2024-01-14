import {v4 as uuidv4} from "uuid";
import {Journal} from "./models";
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
    document.getElementById("JOURNAL-API-BASE-URL").textContent,
  )
  API_BASE_URL = urlJoin(baseUrl, apiUri)
} catch (error) {
  console.log(`Couldn't parse JOURNAL-API-BASE-URL: ${error}`);
}

export function defaultJournal(
  journalId: string = null,
  journalName: string = null,
  journalData: string = null,
): Journal {
  const newjournalId: string = uuidv4();
  return {
    journal_id: journalId || newjournalId,
    journal_name: journalName || "New Journal",
    journal_data: journalData || "",
    date_modified: timeUtils.toDjangoTimeString(new Date()),
    date_created: timeUtils.toDjangoTimeString(new Date()),
  };
}

export async function createJournal(loggedIn: boolean) {
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

      return data.journal_id;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while creating journal: ", error.message);
        return error.message;
      } else {
        console.log("Error while creating journal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    const newJournal: Journal = defaultJournal();
    return newJournal.journal_id;
  }
}

export async function updateJournal(journal: Journal, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.patch(
        urlJoin(API_BASE_URL, journal.journal_id),
        {journal_name: journal.journal_name, journal_data: journal.journal_data},
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
        console.log("Error while updating journal: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while updating journal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 200;
  }
}

export async function deleteJournal(journalId: string, loggedIn: boolean) {
  if (loggedIn) {
    try {
      const {status} = await axios.delete(urlJoin(API_BASE_URL, journalId), {
        withCredentials: true,
      });

      return status;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("Error while deleting journal: ", error.message);
        return error.message;
      } else {
        console.log("Unexpected error while deleting journal: ", error);
        return "An unexpected error occurred";
      }
    }
  } else {
    return 204;
  }
}
