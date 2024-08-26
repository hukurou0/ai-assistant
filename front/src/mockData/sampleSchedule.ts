import { ScheduleDataList } from "@/app/api/schedule/route";

export const scheduleDataList: ScheduleDataList = [
  {
    type: "event",
    id: "1",
    summary: "チームミーティング",
    description: "週次のチーム同期ミーティング",
    time: "09:00 - 10:00",
    now: false
  },
  {
    type: "free_time",
    id: "2",
    time: "10:00 - 11:00",
    now: false
  },
  {
    type: "event",
    id: "3",
    summary: "クライアントとの電話",
    description: "プロジェクトの進捗についてクライアントと電話",
    time: "11:00 - 12:00",
    now: false
  },
  {
    type: "free_time",
    id: "4",
    time: "12:00 - 13:00",
    now: true
  },
  {
    type: "event",
    id: "5",
    summary: "コードレビュー",
    description: "新機能のコードレビュー",
    time: "13:00 - 14:00",
    now: false
  },
  {
    type: "free_time",
    id: "6",
    time: "14:00 - 15:00",
    now: false
  }
];
