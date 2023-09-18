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
            <img
              className={styles.channelPhoto}
              src={creatorOfVideo[0].profilePhoto}
              alt="Фото профиля"
              onClick={() => navigate(`/channel/${creatorOfVideo[0].userId}`)}
            />
            <div
              className={styles.channelInfoContainer}
              onClick={() => navigate(`/channel/${creatorOfVideo[0].userId}`)}
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
                  src="https://s668sas.storage.yandex.net/rdisk/95e6f82899cd8fd1c4df1309a349db06b4dd22cf68a827e57eb3b94959daa44e/65088411/7J95rr6kdzAcx7CEtM-ULsD_T8pRMUr6nuxNKUAiZy6W-YnTX5yCojRkPe-qnS0c_07lvhAIULZxEzNiOSin8Q==?uid=0&filename=heart-Filled_1_.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&fsize=319&hid=e804a923bef2bda4032e8b218f076a7c&media_type=image&tknv=v2&etag=b055694ee5077640dac89cea68b97a8c&rtoken=ZNzfiI4x4ug4&force_default=no&ycrid=na-152b78b835db2a9fb1333318c1ba048c-downloader15h&ts=605a5312c6640&s=e2efb6d282b480e9659e672d9559b342af034c19974da6ad24fb3725c6fd866a&pb=U2FsdGVkX1_fQh5yMWmNreAiwxzcz1v9KrQDZOm3ttW1WVRlWYOqAUhUDPjt_tiZW2NI9vD0OYhKkzMg5QkwLZSHAXp5KoXxoUBwzRkeqBg"
                  alt="Кнопка лайка"
                />
                <p className={styles.likesCount}>{video[0].likes}</p>
              </div>
              <div className={styles.dislike}>
                <img
                  src="https://s188sas.storage.yandex.net/rdisk/5e6daceb6b39fe0c0af12501a7209729affedee8a9d2da2a49cfba3bbe276784/65088444/7J95rr6kdzAcx7CEtM-ULvlLO6KytyB2MBKQzKEyStVISAYdZjRmqQ6nfFgM_Uwv89eC9lulym03Ph20TPCrBg==?uid=0&filename=bookmark-Filled.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&fsize=248&hid=da3adcdc2abec7af0044126bc2a477c6&media_type=image&tknv=v2&etag=c59ccb5fcf99b98cda4f1ca12a836d60&rtoken=MVmwugxQuvCi&force_default=no&ycrid=na-591d624515bb36b9fe23b5709140c14d-downloader15h&ts=605a534369900&s=327fb07c5395e33a4846bcaebc1ecc9e74cd5e8bcbd89edce80a40e32b508f72&pb=U2FsdGVkX18iTJ9fCxYadAjor4pNRp-6WQzMIn02bNdnTEQiGgeImCQVZ8naulPTnjRjXRZ5IUm3zOSS49gOZZVg5jk3WWsF8WOmn8jiN_s"
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
