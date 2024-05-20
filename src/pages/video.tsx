import React, { useEffect, useState } from "react";
import Player from "../components/Player";
import { Link, useLocation, useNavigate } from "react-router-dom";
import styles from "../styles/pages/Video.module.scss";
import stylesFromPlayer from "../styles/components/Player.module.scss";
import CardVideo, { formatNumbers } from "../components/CardVideo";
import classNames from "classnames";
import { useSelector } from "react-redux";
import linkifyHtml from "linkify-html";
import { useBlogsQuery, useVideoQuery } from "../api/blogs";
import { useInfoQuery } from "../api/profiles";

const Video = () => {
  // const [isTheater, setIsTheater] = useState<boolean>(false);
  const navigate = useNavigate();
  const location = useLocation();
  const videoId = location.search.slice(4);
  const { data: videos } = useBlogsQuery("");

  const { data: video } = useVideoQuery(videoId);
  const { data: creatorOfVideo } = useInfoQuery(video?.author.id ?? "");
  console.log(video);
  const isTheater = useSelector((state: any) => state.videoPlayerMode.value);

  const [isDescriptionOpen, setIsDescriptionOpen] = useState(false);

  const handleCommentInput = (e: any) => {
    const submitBtn: HTMLButtonElement | null = document.querySelector(
      `.${styles.submitBtn}`
    );
    const buttons: HTMLDivElement | null = document.querySelector(
      `.${styles.buttons}`
    );

    if (buttons) {
      buttons.style.display = "flex";
    }

    if (e.currentTarget.value !== "" && submitBtn) {
      submitBtn.removeAttribute("disabled");
    } else {
      if (submitBtn) {
        submitBtn.disabled = true;
      }
    }
  };

  const handleCancelButton = () => {
    const buttons: HTMLDivElement | null = document.querySelector(
      `.${styles.buttons}`
    );

    if (buttons) {
      buttons.style.display = "none";
    }
  };

  return (
    <div>
      <Player src={video?.video ?? ""} />
      <div className={styles.container}>
        <div
          className={classNames(styles.videoInfo, isTheater && styles.theater)}
        >
          <h2 className={styles.videoTitle}>{video?.title}</h2>
          <div className={styles.channelInfo}>
            <div className={styles.channel}>
              <div className={styles.channelAvatarWithName}>
                <img
                  className={styles.channelPhoto}
                  src={creatorOfVideo?.dp}
                  alt="Фото профиля"
                  onClick={() => navigate(`/channel/${creatorOfVideo?.id}`)}
                />
                <div
                  className={styles.channelInfoContainer}
                  onClick={() => navigate(`/channel/${creatorOfVideo?.id}`)}
                >
                  <p className={styles.channelName}>{creatorOfVideo?.name}</p>
                  <p className={styles.channelSubscribers}>
                    {formatNumbers(creatorOfVideo?.no_of_followers ?? 0) +
                      " подписчиков"}
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
                <p className={styles.likesCount}>{video?.no_of_likes}</p>
              </div>
              <div className={styles.dislike}>
                <img
                  src="https://3.downloader.disk.yandex.ru/preview/7431e1dc73205ec47b0bf0792f7011c3c30a5094947a80429dded0b798f91453/inf/4I6sJ9ALJQIzb1nmNyxQC996fcUApx8Hv_E3PWRNh5zTILZVCrN_bK8zSBqdKRVOqirLHUMLw3vlKvvcGKJsfQ%3D%3D?uid=1559815427&filename=bookmark-Filled.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x930"
                  alt="Кнопка избранного"
                />
                <p className={styles.dislikesCount}>{video?.no_of_saves}</p>
              </div>
            </div>
          </div>
          <div
            className={styles.description}
            onClick={() => setIsDescriptionOpen(!isDescriptionOpen)}
          >
            <p>
              {isDescriptionOpen
                ? `${video?.views} просмотров`
                : formatNumbers(video?.views ?? 0) + " просмотров"}
            </p>
            <p>
              {isDescriptionOpen ? (
                <span
                  className={styles.desctiptionText}
                  dangerouslySetInnerHTML={{
                    __html: linkifyHtml(video?.description ?? ""),
                  }}
                />
              ) : (
                <>
                  <span
                    className={styles.desctiptionText}
                    dangerouslySetInnerHTML={{
                      __html: linkifyHtml(
                        video?.description?.slice(0, 81) ?? ""
                      ),
                    }}
                  />
                  {video?.description?.length > 81 && (
                    <>
                      ...
                      <span className={styles.readMore}>Читать далее</span>
                    </>
                  )}
                </>
              )}
            </p>
          </div>
          <div className={styles.commentInput}>
            <img
              className={styles.profilePhoto}
              src={creatorOfVideo?.dp}
              alt="profilephoto"
            />
            <div className={styles.inputBtns}>
              <input
                type="text"
                placeholder="Добавить комментарий..."
                onChange={handleCommentInput}
                onClick={handleCommentInput}
              />
              <div className={styles.buttons}>
                <button
                  className={styles.cancelBtn}
                  onClick={handleCancelButton}
                >
                  Отменить
                </button>
                <button className={styles.submitBtn} disabled>
                  Комментировать
                </button>
              </div>
            </div>
          </div>
          {/* <div className={styles.comments}>
            {video[0].comments.map((comment) => {
              const commentAuthor = users.filter(
                (user) => user.userId === comment.userId
              )[0];

              return (
                <div className={styles.comment}>
                  <img
                    onClick={() =>
                      navigate(`/channel/${comment.userId}/videos`)
                    }
                    className={styles.profilePhoto}
                    src={commentAuthor.profilePhoto}
                    alt=""
                  />
                  <div className={styles.commentInfo}>
                    <div
                      className={styles.commentAuthorInfo}
                      onClick={() =>
                        navigate(`/channel/${comment.userId}/videos`)
                      }
                    >
                      <span className={styles.commentAuthorUsername}>
                        @{commentAuthor.username}&nbsp;
                      </span>
                      <span className={styles.commentAuthorSubscribers}>
                        <span className={styles.subscribersNumber}>
                          {formatNumbers(commentAuthor.subscribersCount)}
                        </span>
                        &nbsp;подписчиков
                      </span>
                    </div>
                    <p className={styles.commentText}>{comment.text}</p>
                  </div>
                </div>
              );
            })}
          </div> */}
        </div>
        <div className={styles.videos}>
          {videos?.results.blogs.map((video) => (
            <CardVideo {...video} option="video-page" />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Video;
