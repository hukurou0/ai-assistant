const tagOptions = ["仕事", "個人", "健康", "自己啓発", "その他"] as const;
type TagOption = typeof tagOptions[number];

export { tagOptions };
export type { TagOption };