(ns bookrecommender.mahout
  (:import
   [org.apache.mahout.cf.taste.impl.model.file FileDataModel]
   [org.apache.mahout.cf.taste.impl.neighborhood ThresholdUserNeighborhood]
   [org.apache.mahout.cf.taste.impl.recommender GenericBooleanPrefUserBasedRecommender]
   [org.apache.mahout.cf.taste.impl.similarity TanimotoCoefficientSimilarity]
   [org.apache.mahout.cf.taste.neighborhood UserNeighborhood]
   [org.apache.mahout.cf.taste.recommender Recommender]
   [org.apache.mahout.cf.taste.similarity UserSimilarity]
   [java.io File]))

(defn recommend [filepath user-id num-recommendations]
  (let [model (FileDataModel. (File. filepath))
        similarity (TanimotoCoefficientSimilarity. model)
        neighborhood (ThresholdUserNeighborhood. 0.1, similarity, model)
        recommender (GenericBooleanPrefUserBasedRecommender. model, neighborhood, similarity)]
    (.recommend recommender user-id num-recommendations)))
