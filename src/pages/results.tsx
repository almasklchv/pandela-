import React, { useState } from "react";
import { users } from "../fake-db/main";
import { useLocation } from "react-router-dom";
import { videos } from "../fake-db/main";
import CardVideo from "../components/CardVideo";
import styles from "../styles/pages/Results.module.scss";
import CardChannel from "../components/CardChannel";
import Error404 from "./404";

const Results = () => {
  const location = useLocation();
  const searchQuery = decodeURIComponent(location.search.slice(14));

  const [choose, setChoose] = useState("");

  const foundVideos = videos.filter(
    (video) =>
      video.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      video.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const foundPeople = users.filter((user) =>
    user.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (searchQuery !== "") {
    return (
      <div className={styles.container}>
        <div className={styles.buttons}>
          <button className={styles.btn} onClick={() => setChoose("video")}>
            Искать видео
          </button>
          <button className={styles.btn} onClick={() => setChoose("people")}>
            Искать людей
          </button>
        </div>
        {(choose === "video" || choose === "") && (
          <div className={styles.videos}>
            {foundVideos?.map((video) => (
              <CardVideo {...video} option="results-page" />
            ))}
          </div>
        )}
        {choose === "people" && (
          <div className={styles.channels}>
            {foundPeople?.map((channel) => (
              <CardChannel {...channel} />
            ))}
          </div>
        )}
      </div>
    );
  } else {
    return <Error404 />;
  }
};

export default Results;
