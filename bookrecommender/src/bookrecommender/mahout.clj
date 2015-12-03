(ns bookrecommender.mahout
  (:import
   [org.apache.mahout.cf.taste.impl.model.file FileDataModel]
   [org.apache.mahout.cf.taste.impl.neighborhood ThresholdUserNeighborhood]
   [org.apache.mahout.cf.taste.impl.recommender GenericBooleanPrefUserBasedRecommender]
   [org.apache.mahout.cf.taste.impl.similarity TanimotoCoefficientSimilarity]
   [org.apache.mahout.cf.taste.neighborhood UserNeighborhood]
   [org.apache.mahout.cf.taste.recommender Recommender]
   [org.apache.mahout.cf.taste.similarity UserSimilarity]
   [org.apache.mahout.cf.taste.impl.model GenericDataModel]
   [org.apache.mahout.cf.taste.impl.common FastByIDMap]
   [org.apache.mahout.cf.taste.impl.model BooleanUserPreferenceArray]
   [org.apache.mahout.cf.taste.impl.model BooleanPreference]
   [java.util ArrayList]
   [java.io File]))

(def datastuff (vector
                (hash-map :user_id 1 :preferences '[5 6 7])
                (hash-map :user_id 2 :preferences '[4 6 7])
                (hash-map :user_id 3 :preferences '[2 5 7])))

(defn recommend [user-id num-recommendations data]
  (map
   #(hash-map :item_id (.getItemID %) :value (.getValue %))
   (vec
    (let [model (create-data-model data)
          similarity (TanimotoCoefficientSimilarity. model)
          neighborhood (ThresholdUserNeighborhood. 0.1, similarity, model)
          recommender (GenericBooleanPrefUserBasedRecommender. model, neighborhood, similarity)]
      (.recommend recommender user-id num-recommendations)))))
(recommend 2 1 datastuff)

(defn- create-data-model [data]
  (GenericDataModel.
   (let [id-map (FastByIDMap.)]
     (doseq [user-hash data]
       (let [user-id (:user_id user-hash)
             prefs-array
             ((fn get-prefs-array [user-hash]
                (let [preferences (:preferences user-hash)
                      prefs-array (BooleanUserPreferenceArray. (count preferences))]
                  (doseq ;set preferences in preference array
                   [v (map-indexed vector preferences)]
                    (.set prefs-array (first v) (BooleanPreference. user-id (second v))))
                  prefs-array)) user-hash)]
         (.put id-map user-id prefs-array)))
     id-map)))
