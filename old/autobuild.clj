(ns autobuild
  (:use [clojure.java.io :only [file]]
        [clojure.string :only [join]])
  (:require [cljs.closure :as cljsc]))

(defn rebuild [target options]
  (try 
    (cljsc/build (.getPath target) (if options options {}))
    (println (str "built " target " at " (java.util.Date.)))
    (catch Exception e
      (println "build failed: ")
      (.printStackTrace e))))

(let [paths+timestamps (atom {})]
  (defn file-updated? [target]
    (let [path (.getPath target)
          last-stamp (get @paths+timestamps path)
          new-stamp (.lastModified target)]
      (swap! paths+timestamps assoc path new-stamp) 
      (not (= last-stamp new-stamp)))))

(defn files-updated? [target]
  (if (.isFile target)
    (file-updated? target)
    (some identity (map files-updated? (.listFiles target)))))

(defn -main [raw-args]
  (let [args (rest raw-args)
        [raw-files [& raw-options]] (split-with (fn [string] (not= (first string) \{)) args)
        files (map file raw-files)
        options (if raw-options (read-string (join " " raw-options)))]
    (while true
      (when (some identity (map files-updated? files))
        (rebuild (first files) options)
        (flush)
        )
      (Thread/sleep 500))))

(-main *command-line-args*)
