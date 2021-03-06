(ns bookrecommender.web
  (:require [compojure.core :refer [defroutes GET PUT POST DELETE ANY]]
            [compojure.handler :refer [site]]
            [compojure.route :as route]
            [clojure.java.io :as io]
            [ring.adapter.jetty :as jetty]
            [bookrecommender.mahout :as mahout]
            [ring.util.response :as resp]
            [environ.core :refer [env]]))

(defn splash []
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (pr-str ["Hello" :from 'Heroku])})

(defn get-recommendation [request]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (let [params (:params request)
               user_id (Integer. (re-find #"\d+" (get params :user_id)))
               number_of_preferences (Integer. (re-find #"\d+" (get params :number_of_preferences)))]
           (mahout/json-recommend user_id number_of_preferences))})

(defroutes app
  (GET "/" []
    (splash))
  (POST "/get-recommendation" request
    (get-recommendation request))
  (ANY "*" []
    (route/not-found (slurp (io/resource "404.html")))))

(defn -main [& [port]]
  (let [port (Integer. (or port (env :port) 5000))]
    (jetty/run-jetty (site #'app) {:port port :join? false})))

;; For interactive development:
;; (.stop server)
;; (def server (-main))
