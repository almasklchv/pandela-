import React, { useState } from "react";
import { users } from "../fake-db/main";
import { useLocation } from "react-router-dom";
import { videos } from "../fake-db/main";
import CardVideo from "../components/CardVideo";
import styles from "../styles/pages/Results.module.scss";
import CardChannel from "../components/CardChannel";
import Error404 from "./404";
import classNames from "classnames";
import { useSearchQuery } from "../api/blogs";

const Results = () => {
  const location = useLocation();
  const searchQuery = decodeURIComponent(location.search.slice(14));

  const [choose, setChoose] = useState("");

  const { data: foundVideosOrPeople } = useSearchQuery(searchQuery);
  console.log(foundVideosOrPeople);

  // const foundPeople = foundVideosOrPeople?.matches.filter((user) => {
  //   console.log(
  //     Object.keys(user).includes("name") ||
  //       Object.keys(user).includes("username")
  //   );
  //   console.log(Object.keys(user))
  // });
  // console.log(foundPeople);
  // foundVideosOrPeople?.matches.map((user) => {
  //   console.log(user);
  // });

  if (searchQuery !== "") {
    return (
      <div className={styles.container}>
        <div className={styles.buttons}>
          <button
            className={classNames(styles.btn, {
              [styles.selected]: choose === "video" || choose === "",
            })}
            onClick={() => setChoose("video")}
          >
            Искать Видео
          </button>
          <button
            className={classNames(styles.btn, {
              [styles.selected]: choose === "people",
            })}
            onClick={() => setChoose("people")}
          >
            Искать Людей
          </button>
        </div>
        {(choose === "video" || choose === "") && (
          <div className={styles.videos}>
            {foundVideosOrPeople?.matches?.map((video) => (
              <CardVideo {...video} option="results-page" />
            ))}
          </div>
        )}
        {/* {choose === "people" && (
          <div className={styles.channels}>
            {foundPeople?.map((channel) => (
              <CardChannel {...channel} />
            ))}
          </div>
        )} */}
      </div>
    );
  } else {
    return <Error404 />;
  }
};

export default Results;
