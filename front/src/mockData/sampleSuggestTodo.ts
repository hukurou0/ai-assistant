import { SuggestTodoData } from "@/app/api/suggest/route";

export const suggestTodoDataSample: SuggestTodoData[] = [
  {
    free_time_id: "2",
    suggest_todo: {
      id: "todo1",
      title: "コードのリファクタリング",
      required_time: 60,
      note: "モジュールの最適化"
    },
    selected: false
  },
  {
    free_time_id: "2",
    suggest_todo: {
      id: "todo2",
      title: "クライアントへのメール返信",
      required_time: 30,
      note: "契約更新に関する質問への対応"
    },
    selected: true
  },
  {
    free_time_id: "4",
    suggest_todo: {
      id: "todo3",
      title: "プロジェクト計画の見直し",
      required_time: 90,
      note: "次のスプリントに向けたタスクの再整理"
    },
    selected: false
  },
  {
    free_time_id: "4",
    suggest_todo: {
      id: "todo4",
      title: "ミーティングのアジェンダ作成",
      required_time: 45,
      note: "次回のミーティングのための議題をまとめる"
    },
    selected: false
  },
  {
    free_time_id: "6",
    suggest_todo: {
      id: "todo5",
      title: "技術ブログ執筆",
      required_time: 120,
      note: "新しいフレームワークの使用感をまとめる"
    },
    selected: true
  },
  {
    free_time_id: "6",
    suggest_todo: {
      id: "todo6",
      title: "ドキュメントの整理",
      required_time: 60,
      note: "最新の仕様書をアップデート"
    },
    selected: false
  }
];
