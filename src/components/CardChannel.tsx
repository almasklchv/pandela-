import React from "react";
import styles from "../styles/components/CardChannel.module.scss";
import { users, videos } from "../fake-db/main";
import { formatNumbers } from "./CardVideo";
import { useNavigate } from "react-router-dom";

interface User {
  userId: string;
  name: string;
  username: string;
  profilePhoto: string;
  subscribersCount: number;
  bio: string;
}

const CardChannel = (props: User) => {
  const navigate = useNavigate();
  const channelVideos = videos.filter((video) => video.userId === props.userId);

  return (
    <div className={styles.container}>
      <div
        className={styles.profileInfo}
        onClick={() => navigate(`/channel/${props.userId}/videos`)}
      >
        <img
          className={styles.profilePhoto}
          src={props.profilePhoto}
          alt="profilephoto"
        />
        <div>
          <p className={styles.name}>{props.name}</p>
          <p className={styles.username}>
            {props.username} {formatNumbers(props.subscribersCount) + " подписчиков"}
            {formatNumbers(channelVideos.length)} видео
          </p>
          <p className={styles.bio}>{props.bio}</p>
        </div>
      </div>
      <button className={styles.subscribeBtn}>Подписаться</button>
    </div>
  );
};

export default CardChannel;
