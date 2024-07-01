# commands
```
開発サーバの起動   
npm run dev
```

# coding-rule
1. next.jsのAppRouterを用いる
2. page.tsx内で用いるコンポーネントはfront/src/componets内に保管
3. 外部との通信などで情報を取得、変換するロジックはfront/src/servicesに保管
4. APIサーバとの通信をするservicesはfront/src/util/axios-baseのAxiosUtilを使って実装
5. 外部からの情報の取得はpage.tsxのみに記述し、componentではpropsのみ使う