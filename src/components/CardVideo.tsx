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
  views: number;
  ago: string;
  description: string;
  option?: string;
}

export const formatNumbers = (number: number) => {
  if (number >= 1e9) {
    return `${(number / 1e9).toFixed(1)} млрд`;
  } else if (number >= 1e6) {
    return `${(number / 1e6).toFixed(1)} млн`;
  } else if (number >= 1e3) {
    return `${(number / 1e3).toFixed(1)} тыс`;
  } else {
    return `${number}`;
  }
};

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
        [styles.results]: props.option === "results-page",
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
        <p className={styles.videoTitle}>
          {window.innerWidth > 600 && props.option !== "video-page"
            ? props.title
            : props.title.slice(0, 20)}
        </p>
        {props.option === "video-page" && (
          <p className={styles.videoAuthorName}>{creatorOfVideo[0].name}</p>
        )}
        <p className={styles.videoStat}>
          {formatNumbers(props.views)} просмотров&nbsp;&nbsp;&nbsp;&nbsp;
          {props.option === "video-page" &&
          (window.innerWidth > 1200 || window.innerWidth <= 600)
            ? props.ago.slice(0, 3) + (props.ago.length > 7 && "...")
            : props.ago}
        </p>
        {props.option === "results-page" && (
          <div className={styles.videoAuthor}>
            <div className={styles.profileStat}>
              <img
                className={styles.profilePhoto}
                src={creatorOfVideo[0].profilePhoto}
                alt="profilephoto"
              />
              <span className={styles.username}>
                @{creatorOfVideo[0].username} ·&nbsp;
              </span>
              <span className={styles.subscribersCount}>
                <span className={styles.subscribersNumber}>
                  {formatNumbers(creatorOfVideo[0].subscribersCount)}
                </span>{" "}
                подписчиков
              </span>
            </div>

            <p className={styles.description}>
              {props.description.slice(0, 110)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CardVideo;
