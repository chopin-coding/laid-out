export interface GratitudeJournalNode {
  title: string;
  node_id: string;
}

export interface GratitudeJournal {
  g_journal_id: string;
  g_journal_name: string;
  g_journal_data: GratitudeJournalNode[];
  date_created: string;
  date_modified: string;
}
