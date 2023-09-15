import React, { useEffect, useState } from "react";
import Player from "../components/Player";
import { videos, users } from "../fake-db/main";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "../styles/pages/Video.module.scss";
import stylesFromPlayer from "../styles/components/Player.module.scss";
import CardVideo from "../components/CardVideo";
import classNames from "classnames";
import { useSelector } from "react-redux";

const Video = () => {
  // const [isTheater, setIsTheater] = useState<boolean>(false);
  const navigate = useNavigate();
  const location = useLocation();
  const videoId = location.search.slice(4);
  const video = videos.filter((video) => video.videoId === videoId);
  const creatorOfVideo = users.filter(
    (user) => video[0].userId === user.userId
  );
  const isTheater = useSelector((state: any) => state.videoPlayerMode.value)
  
  const [isDescriptionOpen, setIsDescriptionOpen] = useState(false);
  

  return (
    <div>
      <Player src={video[0].videoPath}/>
      <div className={styles.container}>
        <div
          className={classNames(styles.videoInfo, isTheater && styles.theater)}
        >
          <h2 className={styles.videoTitle}>{video[0].title}</h2>
          <div className={styles.channelInfo}>
            <img
              className={styles.channelPhoto}
              src={creatorOfVideo[0].profilePhoto}
              alt="Фото профиля"
              onClick={() =>
                navigate(`/channel?id=${creatorOfVideo[0].userId}`)
              }
            />
            <div
              className={styles.channelInfoContainer}
              onClick={() =>
                navigate(`/channel?id=${creatorOfVideo[0].userId}`)
              }
            >
              <p className={styles.channelName}>{creatorOfVideo[0].name}</p>
              <p className={styles.channelSubscribers}>
                {creatorOfVideo[0].subscribersCount}
              </p>
            </div>
            <button className={styles.subscribeBtn}>Подписаться</button>
            <div className={styles.channelActions}>
              <div className={styles.like}>
                <img
                  src="https://4.downloader.disk.yandex.ru/preview/d57ff91b155322899f09c8439abebf36ca6e1c112e5e73f60bad9e52d674294f/inf/_0J5OM5mtjsY9nryWr2n8Val_GSfBuh7qGGWnkHdbyBpnwXKN-e6cO5WXbf4XcFkdWIx6LirQ2UwP6bppABgTQ%3D%3D?uid=1559815427&filename=like.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x867"
                  alt="Кнопка лайка"
                />
                <p className={styles.likesCount}>{video[0].likes}</p>
              </div>
              <div className={styles.dislike}>
                <img
                  src="https://1.downloader.disk.yandex.ru/preview/f3556b916196d49f49831cd786b98934d291c33d3985e35e771721587b1c5aa0/inf/Hyws5XLMlvZrufhoAqO-mHHk_3tF7ru242mYSOe-csG6SGcHzA4dY4kvIgw2VOLFOCwNMvs3TLJGxhGm5VNN3A%3D%3D?uid=1559815427&filename=dislike.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x867"
                  alt="Кнопка дизлайка"
                />
                <p className={styles.dislikesCount}>{video[0].dislikes}</p>
              </div>
            </div>
          </div>
          <div
            className={styles.description}
            onClick={() => setIsDescriptionOpen(!isDescriptionOpen)}
          >
            <p>{video[0].views}</p>
            <p>
              {isDescriptionOpen ? (
                <>{video[0].description}</>
              ) : (
                <>
                  {video[0].description.slice(0, 81) + "..."}
                  <span>Читать далее</span>
                </>
              )}
            </p>
          </div>
        </div>
        <div className={styles.videos}>
          {videos.map((video) => (
            <CardVideo {...video} option="video-page" />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Video;
