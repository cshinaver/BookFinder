(ns bookrecommender.config)
(defn- get-database-config []
  (let [database-url (System/getenv "DATABASE_URL")]
    (if
     (nil? database-url)
      {:db-user "postgres"
       :db-pass "test"
       :db-host "localhost"
       :db-port 5432
       :db-name "test"}
      (let
       [regex-matches (re-find #"postgres://(\S+):(\S+)@(\S+):(\d+)/(\S+)$" database-url)
        db-user (nth regex-matches 1)
        db-pass (nth regex-matches 2)
        db-host (nth regex-matches 3)
        db-port (nth regex-matches 4)
        db-name (nth regex-matches 5)]
        {:db-user db-user :db-pass db-pass :db-host db-host :db-port db-port :db-name db-name}))))

(def config (get-database-config))
