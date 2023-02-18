(ns palindrome
  "Playing with words and letters a little."
  (:require [clojure.java.io :as io]
            [cuerdas.core :as str]
            [clojure.edn :as edn]))

(defn palindrome?
  [string]
  (let [reversed (apply str (reverse string))]
    (= string reversed)))

(defn palindromes
  [file]
  (let [lines (line-seq (io/reader file))]
    (filter palindrome? lines)))

(defn generate-palindromes
  "Generate a lazy list of palendromes, formed from randomly indexing the
  alphabet, all of length n. Calls `palindromes` to filter out non-palindromes."
  [n]
  (let [alphabet "abcdefghijklmnopqrstuvwxyz"
        random-index (fn [] (rand-int (count alphabet)))
        random-letter (fn [] (str (nth alphabet (random-index))))]
    (apply str (repeat n (random-letter)))
    #_(filter palindrome?
              (map #(apply str (repeat n (random-letter))) (range)))))

(map palindrome? '("racecar" "racecars" "racecar" "racecars"))
(generate-palindromes 3)
