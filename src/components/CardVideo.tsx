import React from "react";
import styles from "../styles/components/CardVideo.module.scss";
import { useNavigate } from "react-router-dom";
import classNames from "classnames";
import { users } from "../fake-db/main";

interface ICardVideo {
  userId: string;
  videoId: string;
  coverPath: string;
  videoPath: string;
  title: string;
  views: string;
  ago: string;
  option?: string;
}

const CardVideo = (props: ICardVideo) => {
  // const handlePlayVideo = () => {
  //   const video: HTMLVideoElement | null = document.querySelector(
  //     'video'
  //   );
  //   video?.play();
  // };

  // const handlePauseVideo = () => {
  //   const video: HTMLVideoElement | null = document.querySelector(
  //     'video'
  //   );
  //   video?.pause();
  // };

  const creatorOfVideo = users.filter((user) => user.userId === props.userId);
  const navigate = useNavigate();
  const openVideo = () => {
    navigate(`/video?id=${props.videoId}`);
  };

  return (
    <div
      className={classNames(styles.card, {
        [styles.video]: props.option === "video-page",
      })}
      onClick={openVideo}
    >
      <img
        className={styles.videoCover}
        src={props.coverPath}
        alt={props.title}
      />
      {/* <video
        className={styles.playerCover}
        src={props.videoPath}
        onMouseMove={handlePlayVideo}
        onMouseOut={handlePauseVideo}
      ></video> */}
      <div>
        <p className={styles.videoTitle}>{props.title.slice(0, 30)}</p>
        {props.option === "video-page" && (
          <p className={styles.videoAuthorName}>{creatorOfVideo[0].name}</p>
        )}
        <p className={styles.videoStat}>
          {props.views}&nbsp;&nbsp;&nbsp;&nbsp;
          {props.option === "video-page"
            ? props.ago.slice(0, 7) + (props.ago.length > 7 && "...")
            : props.ago}
        </p>
      </div>
    </div>
  );
};

export default CardVideo;
