import React, { useEffect, useState, useMemo } from "react";
import styles from "../styles/pages/Profile.module.scss";
import CardVideo, { formatNumbers } from "../components/CardVideo";
import { videos } from "../fake-db/main";
import { users } from "../fake-db/main";
import { playlists } from "../fake-db/main";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import Error404 from "./404";
import classNames from "classnames";
import linkifyHtml from "linkify-html";

interface IChannel {
  userId?: string;
}

const tabMap = {
  "/videos": "Видео",
  "/playlists": "Плейлисты",
  "/about": "О канале",
};

const Channel = (props: IChannel) => {
  const navigate = useNavigate();
  const { id } = useParams();
  const {username} = useParams();
  const location = useLocation();
  const userIdFromUsername = users.filter((user) => user.username === username)[0]?.userId
  const path = location.pathname.slice(0, 8);
  
  

  if (userIdFromUsername) {
    window.location.href = `/channel/${userIdFromUsername}/videos`
  } else if (!id && !props.userId){
    window.location.href = '/'
  }

  const user = useMemo(() => {
    if (id || props.userId) {
      return users.filter(
        (user) =>
          (id && id === user.userId) ||
          (props.userId && props.userId === user.userId)
      );
    }
    
  }, [id, props.userId]);

  const [tab, setTab] = useState(() => {
    let selected = "";
    location.pathname
      .split("")
      .reverse()
      .reduce((prev, curr) => {
        prev += curr;
        if (curr.toLowerCase() === curr.toUpperCase() && selected === "") {
          selected = prev;
        }
        return prev;
      });
    return selected.split("").reverse().join("");
  });

  let allViews = 0;
  if (user) {
    videos
    .filter((video) => video.userId === user[0]?.userId)
    .forEach((video) => (allViews += video.views));
  }
  

  const handlePlaylistCoverColor = () => {
    var image: HTMLImageElement | null = document.querySelector(
      `.${styles.playlistCover}`
    );

    const playlistInfo: any = document.querySelectorAll(
      `.${styles.playlistInfo}`
    );

    if (image && playlistInfo) {
      // Загружаем изображение с другого домена с указанием "crossOrigin"
      const img = new Image();
      img.crossOrigin = "Anonymous";
      img.src = image.src;

      // Устанавливаем обработчик события "onload" для изображения
      img.onload = function () {
        // Создаем холст (canvas) для анализа изображения
        var canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;

        // Получаем контекст холста
        var context: CanvasRenderingContext2D | null = canvas.getContext("2d");

        if (context) {
          // Отрисовываем изображение на холсте
          context.drawImage(img, 0, 0, img.width, img.height);

          // Получаем цвет пикселя по координатам (x, y)
          var x = 100;
          var y = 50;
          var pixelColor = context.getImageData(x, y, 1, 1).data;

          // pixelColor содержит массив [R, G, B, A], представляющий цвет пикселя

          var brightness =
            (0.299 * pixelColor[0] +
              0.587 * pixelColor[1] +
              0.114 * pixelColor[2]) /
            255;

          // Вычисляем новый цвет в зависимости от яркости
          var red = Math.floor(pixelColor[0] + (brightness < 0.5 ? 81 : -81));
          var green = Math.floor(pixelColor[1] + (brightness < 0.5 ? 81 : -81));
          var blue = Math.floor(pixelColor[2] + (brightness < 0.5 ? 81 : -81));

          for (let i = 0; i < playlistInfo.length; i++) {
            playlistInfo[i].style.background =
              "RGB(" + red + ", " + green + ", " + blue + ")";
          }
        }
      };
    }
  };
  

  useEffect(() => {
    if (
      ![
        "/profile",
        "/profile/videos",
        "/profile/playlists",
        "/profile/about",
      ].includes(location.pathname) &&
      !["/videos", "/playlists", "/about"].includes(tab)
    ) {
      navigate(`/channel/${id}/videos`);
      setTab("/videos");
    }
    if (location.pathname === "/profile") {
      navigate("/profile/videos");
      setTab("/videos");
    }
  }, [tab, id, location.pathname, navigate]);

  if (user?.length !== 0 && user) {
    return (
      <div className={styles.channel}>
        <div className={styles.container}>
          <img
            className={styles.profileBanner}
            src="https://3.downloader.disk.yandex.ru/preview/66d3ba9cf2834f6c32cbfac1b851ed200e8e8a870e68244e5428bdb42bc69fba/inf/O1FL5xXdeAtSZo4OWskn4CUeEDlc8liDg6FnmJgmcdIXVn86IFDFZ-f8mxTPaV0dl7NPtgwwSSDzlvmTRDZ1sg%3D%3D?uid=1559815427&filename=profile-banner.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x867"
            alt="Шапка профиля"
          />
          <div className={styles.profileInfo}>
            <img
              className={styles.profilePhoto}
              src={user[0]?.profilePhoto}
              alt="Фото профиля"
              width={82}
              height={82}
            />
            <div className={styles.personInfo}>
              <p className={styles.name}>{user[0]?.name}</p>
              <p className={styles.username}>
                @{user[0]?.username} {formatNumbers(user[0]?.subscribersCount) + " подписчиков"}
              </p>
              <p className={styles.bio}>{user[0]?.bio}</p>
            </div>
            <button className={styles.subscribeBtn}>Подписаться</button>
          </div>
          <ul className={styles.navbar}>
            {Object.entries(tabMap).map(([tabKey, tabName]) => (
              <li
                key={tabKey}
                className={classNames(styles.navbarItem, {
                  [styles.selected]: tab === tabKey,
                })}
                onClick={() => {
                  const targetUrl = id
                    ? `/channel/${id}${tabKey}`
                    : `/profile${tabKey}`;
                  navigate(targetUrl);
                  setTab(tabKey);
                }}
              >
                {tabName}
              </li>
            ))}
          </ul>
          {tab === "/videos" && (
            <div className={styles.videos}>
              {videos
                .filter(
                  (video) =>
                    video.userId === id || video.userId === props.userId
                )
                .map((video: any) => (
                  <CardVideo key={video.id} {...video} />
                ))}
            </div>
          )}
          {tab === "/playlists" && (
            <div className={styles.playlists}>
              {playlists.map((playlist) =>
                videos.map((video) => {
                  if (
                    playlist.userId === id ||
                    playlist.userId === props.userId
                  ) {
                    if (video.videoId === playlist.videos[0]) {
                      return (
                        <div
                          className={styles.playlist}
                          onMouseEnter={(e) => {
                            const viewPlaylist: any =
                              e.currentTarget.children[0].children[2];
                            viewPlaylist.style.display = "block";
                          }}
                          onMouseLeave={(e) => {
                            const viewPlaylist: any =
                              e.currentTarget.children[0].children[2];
                            viewPlaylist.style.display = "none";
                          }}
                          onClick={() => navigate(`/playlist/${playlist.playlistId}`)}
                        >
                          <div className={styles.thumbnail}>
                            <img
                              className={styles.playlistCover}
                              src={video.coverPath}
                              // src="/images/playlist-cover.png"
                              onLoad={handlePlaylistCoverColor}
                              alt={video.title}
                            />
                            <p className={styles.playlistInfo}>
                              <svg
                                fill="#fff"
                                height="24"
                                viewBox="0 0 24 24"
                                width="24"
                                focusable="false"
                                style={{
                                  pointerEvents: "none",
                                  display: "block",
                                }}
                              >
                                <path d="M22 7H2v1h20V7zm-9 5H2v-1h11v1zm0 4H2v-1h11v1zm2 3v-8l7 4-7 4z"></path>
                              </svg>
                              {playlist.videos.length} видео
                            </p>
                            <p className={styles.viewPlaylist}>
                              ОТКРЫТЬ ПЛЕЙЛИСТ
                            </p>
                          </div>
                          <p className={styles.playlistTitle}>
                            {playlist.title}
                          </p>
                        </div>
                      );
                    } else {
                      return null;
                    }
                  } else {
                    return null;
                  }
                })
              )}
            </div>
          )}
          {tab === "/about" && (
            <div className={styles.about}>
              <div className={styles.left}>
                <div className={styles.description}>
                  <p className={styles.title}>Описание</p>
                  <p>{user[0].bio ? user[0].bio : 'Автор канала не заполнил описание.'}</p>
                </div>
                <div className={styles.links}>
                  <p className={styles.title}>Ссылки</p>
                  <div className={styles.linksItems}>
                    {user[0].links ? user[0].links?.map((link) => {
                      return (
                        <div className={styles.linksItem}>
                          <p className={styles.linkName}>{link.name}</p>
                          <span
                            className={styles.link}
                            dangerouslySetInnerHTML={{
                              __html: linkifyHtml(link.link),
                            }}
                          />
                        </div>
                      );
                    }) : 'Автор канала не добавил ссылок.'}
                  </div>
                </div>
              </div>
              <div className={styles.right}>
                <div className={styles.stats}>
                  <p className={styles.title}>Статистика</p>
                  <p className={styles.views}>{formatNumbers(allViews)} просмотров</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  } else {
    return <Error404 />;
  }
};

export default Channel;
