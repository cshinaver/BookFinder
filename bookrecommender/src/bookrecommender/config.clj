(ns bookrecommender.config)
(def config {:database-url (or (System/getenv "DATABASE_URL") "localhost")})
