(ns bookrecommender.db
  (:require
   [clojure.java.jdbc :as db]
   [bookrecommender.config :as config]
   ))

(let [db-host (:database-url config/config)
      db-port 5432
      db-name "test"]
  (def db-spec {:subprotocol "postgresql"
                :subname (str "//" db-host ":" db-port "/" db-name)
                :user "postgres"
                :password "test"}))

(defn get-recommendation-data []
  (let [raw-data (group-by :user_id (db/query db-spec ["select * from BooksViewed"]))
        hash-keys (keys raw-data)]
    (map
     (fn [k]
       (let [prefs (let [raw-tuples-for-user (raw-data k)]
                     (map #(:book_id %) raw-tuples-for-user))]
         (hash-map :user_id k :preferences prefs)))
     hash-keys)))
