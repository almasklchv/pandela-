import React, { useEffect, useState } from "react";
import Player from "../components/Player";
import { videos, users } from "../fake-db/main";
import { Link, useLocation, useNavigate } from "react-router-dom";
import styles from "../styles/pages/Video.module.scss";
import stylesFromPlayer from "../styles/components/Player.module.scss";
import CardVideo from "../components/CardVideo";
import classNames from "classnames";
import { useSelector } from "react-redux";
import linkifyHtml from "linkify-html";

const Video = () => {
  // const [isTheater, setIsTheater] = useState<boolean>(false);
  const navigate = useNavigate();
  const location = useLocation();
  const videoId = location.search.slice(4);
  const video = videos.filter((video) => video.videoId === videoId);
  const creatorOfVideo = users.filter(
    (user) => video[0].userId === user.userId
  );
  const isTheater = useSelector((state: any) => state.videoPlayerMode.value);

  const [isDescriptionOpen, setIsDescriptionOpen] = useState(false);

  return (
    <div>
      <Player src={video[0].videoPath} />
      <div className={styles.container}>
        <div
          className={classNames(styles.videoInfo, isTheater && styles.theater)}
        >
          <h2 className={styles.videoTitle}>{video[0].title}</h2>
          <div className={styles.channelInfo}>
            <div className={styles.channel}>
              <div className={styles.channelAvatarWithName}>
                <img
                  className={styles.channelPhoto}
                  src={creatorOfVideo[0].profilePhoto}
                  alt="Фото профиля"
                  onClick={() =>
                    navigate(`/channel/${creatorOfVideo[0].userId}`)
                  }
                />
                <div
                  className={styles.channelInfoContainer}
                  onClick={() =>
                    navigate(`/channel/${creatorOfVideo[0].userId}`)
                  }
                >
                  <p className={styles.channelName}>{creatorOfVideo[0].name}</p>
                  <p className={styles.channelSubscribers}>
                    {creatorOfVideo[0].subscribersCount}
                  </p>
                </div>
              </div>
              <button className={styles.subscribeBtn}>Подписаться</button>
            </div>

            <div className={styles.channelActions}>
              <div className={styles.like}>
                <img
                  src="https://1.downloader.disk.yandex.ru/preview/28207cd9632f4dd7ffd4e7e82b679256e66a73f8042d981b1a58369c1befd0ad/inf/q5M3dHMw52ZTVXksipMpcakEZ0tjOtuz7P6ioKEKZXqaBUj2oW2GftiV1vcC69_JR58-k1R9GGRL4bX4WYjiGQ%3D%3D?uid=1559815427&filename=heart-Filled_1_.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x930"
                  alt="Кнопка лайка"
                />
                <p className={styles.likesCount}>{video[0].likes}</p>
              </div>
              <div className={styles.dislike}>
                <img
                  src="https://3.downloader.disk.yandex.ru/preview/7431e1dc73205ec47b0bf0792f7011c3c30a5094947a80429dded0b798f91453/inf/4I6sJ9ALJQIzb1nmNyxQC996fcUApx8Hv_E3PWRNh5zTILZVCrN_bK8zSBqdKRVOqirLHUMLw3vlKvvcGKJsfQ%3D%3D?uid=1559815427&filename=bookmark-Filled.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x930"
                  alt="Кнопка избранного"
                />
                <p className={styles.dislikesCount}>{video[0].favorites}</p>
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
                <span
                  className={styles.desctiptionText}
                  dangerouslySetInnerHTML={{
                    __html: linkifyHtml(video[0].description),
                  }}
                />
              ) : (
                <>
                  <span
                    className={styles.desctiptionText}
                    dangerouslySetInnerHTML={{
                      __html: linkifyHtml(video[0].description.slice(0, 81)),
                    }}
                  />
                  {video[0].description.length > 81 && (
                    <>
                      ...
                      <span className={styles.readMore}>Читать далее</span>
                    </>
                  )}
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
