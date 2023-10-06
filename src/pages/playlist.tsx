import React, { useEffect, useState } from "react";
import styles from "../styles/pages/Playlist.module.scss";
import { playlists, users, videos } from "../fake-db/main";
import { useNavigate, useParams } from "react-router-dom";
import Error404 from "./404";
import CardVideo, { formatNumbers } from "../components/CardVideo";


const Playlist = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const playlist = playlists.filter((playlist) => playlist.playlistId === id);
  const user = users.filter((user) => user.userId === playlist[0].userId)[0];

  let videosFromPlaylist = [];
  for (let i = 0; i < playlist[0].videos.length; i++) {
    videosFromPlaylist.push(
      videos.filter((video) => video.videoId === playlist[0].videos[i])[0]
    );
  }

  let allViews = 0;

  if (user) {
    videosFromPlaylist
      .filter((video) => video.userId === user.userId)
      .forEach((video) => (allViews += video.views));
  }

  const handlePlaylistInfoGradient = () => {
    let image: HTMLImageElement | null = document.querySelector(
      `.${styles.playlistThumbnail}`
    );

    const playlistInfo: any = document.querySelector(`.${styles.playlistInfo}`);
    console.log(playlistInfo, image);
    if (image && playlistInfo) {
      // Загружаем изображение с другого домена с указанием "crossOrigin"
      const img = new Image();
      img.crossOrigin = "Anonymous";
      img.src = image.src;

      // Устанавливаем обработчик события "onload" для изображения
      img.onload = function () {
        // Получаем цвет пикселя по координатам (x, y)
        let x = 100;
        let y = 50;
        let pixelColor = getPixelColor(img, x, y);

        // Создаем линейный градиент
        let gradient = `linear-gradient(rgba(${pixelColor.join(
          ", "
        )}, 0.7), rgba(0, 0, 0, 0.7))`;

        playlistInfo.style.background = gradient;
      };
    }
  };

  // Функция для получения цвета пикселя из изображения
  function getPixelColor(
    image: HTMLImageElement,
    x: number,
    y: number
  ): number[] {
    var canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    var context: CanvasRenderingContext2D | null = canvas.getContext("2d");

    if (context) {
      context.drawImage(image, 0, 0, image.width, image.height);
      var pixelData = context.getImageData(x, y, 1, 1).data;

      // Возвращаем массив [R, G, B, A]
      return [pixelData[0], pixelData[1], pixelData[2]];
    }

    return [255, 255, 255];
  }

  if (playlist[0]) {
    return (
      <div className={styles.playlist}>
        <div className={styles.playlistInfo}>
          <img
            className={styles.playlistThumbnail}
            src={videosFromPlaylist[0].coverPath}
            alt={videosFromPlaylist[0].title}
            onLoad={handlePlaylistInfoGradient}
          />
          <h3 className={styles.playlistTitle}>{playlist[0].title}</h3>
          <p className={styles.description}>{playlist[0].description}</p>
          <p className={styles.playlistAuthor} onClick={() => navigate(`/channel/${playlist[0].userId}/videos`)}>{user.name}</p>
          <p className={styles.playlistStats}>
            {videosFromPlaylist.length} видео {formatNumbers(allViews)} просмотров
          </p>
        </div>
        <div className={styles.videos}>
          {videosFromPlaylist.map((video) => {
            return <CardVideo {...video} option="results-page" />;
          })}
        </div>
      </div>
    );
  } else {
    return <Error404 />;
  }
};

export default Playlist;
