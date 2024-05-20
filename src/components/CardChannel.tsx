import React from "react";
import styles from "../styles/components/CardChannel.module.scss";
import { formatNumbers } from "./CardVideo";
import { useNavigate } from "react-router-dom";
import { UserType } from "../types/user.type";
import { useInfoQuery } from "../api/profiles";

const CardChannel = (props: UserType) => {
  const navigate = useNavigate();
  const { data: profile } = useInfoQuery(props.id);
  console.log(props);

  return (
    <div className={styles.container}>
      <div
        className={styles.profileInfo}
        onClick={() => navigate(`/channel/${props.id}/videos`)}
      >
        <img
          className={styles.profilePhoto}
          src={profile?.dp}
          alt="profilephoto"
        />
        <div>
          <p className={styles.name}>{props.name}</p>
          <p className={styles.username}>
            {props.username}{" "}
            {formatNumbers(profile?.no_of_followers ?? 0) + " подписчиков"}
            {formatNumbers(profile?.no_of_blogs ?? 0)} видео
          </p>
          <p className={styles.bio}>{props.bio}</p>
        </div>
      </div>
      <button className={styles.subscribeBtn}>Подписаться</button>
    </div>
  );
};

export default CardChannel;
