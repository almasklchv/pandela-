import React, { useEffect, useState } from "react";
import styles from "../styles/components/Player.module.scss";
import { useLocation } from "react-router-dom";
import classNames from "classnames";
import { useDispatch } from "react-redux";
import { isTheaterMode } from "../store/playerModeSlice";

interface IPlayer {
  src: string;
}

const Player = (props: IPlayer) => {
  // Состояния для управления плеером
  const [paused, setPaused] = useState<boolean>(true); // Приостановлено ли видео
  const [isTheater, setIsTheater] = useState<boolean>(false); // Включен ли режим театра
  const [isFullScreen, setIsFullScreen] = useState<boolean>(false); // Находится ли видео в полноэкранном режиме
  const [isMuted, setIsMuted] = useState<boolean>(false); // Приглушено ли аудио

  const dispatch = useDispatch();

  // Обработчик контекстного меню для предотвращения его отображения
  const handleContextMenu = (e: any) => {
    e.preventDefault();
  };

  // Обработчик нажатия клавиш
  const handleKeyDown = (e: any) => {
    const tagName = document.activeElement?.tagName.toLowerCase();
    // e.preventDefault();

    if (tagName === "input") return;

    switch (e.key.toLowerCase()) {
      case "f5":
        window.location.reload();
        break;
      case " ":
        e.preventDefault();
        handlePlayPause();
        break;
      case "k":
        handlePlayPause();
        break;
      case "f":
        handleFullScreen();
        break;
      case "t":
        handleTheaterMode();
        break;
      case "m":
        handleMute();
        break;
      case "arrowleft":
      case "j":
        skip(-5);
        break;
      case "arrowright":
      case "l":
        skip(5);
        break;
      case "c":
        // toggleCaptions();
        break;
    }
  };

  // Обработчик переключения режима театра
  const handleTheaterMode = () => {
    setIsTheater(!isTheater);
    dispatch(isTheaterMode(!isTheater));
  };

  // Обработчик переключения режима мини-плеера
  const handleMiniPlayer = () => {
    const videoContainer = document.querySelector(
      `.${styles["video-container"]}`
    );
    const video: HTMLVideoElement | null = document.querySelector("video");
    if (videoContainer?.classList.contains(`.${styles["mini-player"]}`)) {
      document.exitPictureInPicture();
    } else {
      if (video && document.pictureInPictureElement !== video) {
        // Проверяем, не находится ли видео уже в режиме Picture-in-Picture
        video.requestPictureInPicture();
      }
    }
  };

  // Обработчик переключения полноэкранного режима
  const handleFullScreen = () => {
    const videoContainer = document.querySelector(
      `.${styles["video-container"]}`
    );
    if (document.fullscreenElement === null) {
      videoContainer?.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  };

  // Обработчик изменения состояния полноэкранного режима
  const handleFullScreenChange = () => {
    setIsFullScreen(!!document.fullscreenElement);
  };

  // Обработчик приглушения/отмены приглушения аудио
  const handleMute = () => {
    const video: HTMLVideoElement | null = document.querySelector("video");
    const volumeSlider: HTMLInputElement | null = document.querySelector(
      `.${styles["volume-slider"]}`
    );
    if (video && volumeSlider) {
      video.muted = !video.muted;
      setIsMuted(video.muted);
      volumeSlider.value = "0";
      if (!video.muted) {
        video.volume = 1;
        volumeSlider.value = "1";
      }
    }
  };

  // Обработчик изменения уровня громкости
  const handleInputVolume = (e: any) => {
    const volumeSlider: any = document.querySelector(
      `.${styles["volume-slider"]}`
    );
    const video: HTMLVideoElement | null = document.querySelector("video");
    const videoContainer: HTMLDivElement | null = document.querySelector(
      `.${styles["video-container"]}`
    );
    let volumeLevel: string;
    if (video && volumeSlider && videoContainer) {
      video.volume = e.target.value;
      if (parseFloat(e.target.value) !== 0) {
        video.muted = false;
        setIsMuted(false);
        if (video.volume > 0.5) {
          volumeLevel = "high";
        } else {
          volumeLevel = "low";
        }
      } else {
        video.muted = true;
        setIsMuted(true);
        volumeLevel = "muted";
      }

      volumeSlider.value = video.volume;
      videoContainer.dataset.volumeLevel = volumeLevel;
    }
  };

  // Обработчик загрузки видео
  const handleLoadedVideo = () => {
    const video: HTMLVideoElement | null = document.querySelector("video");
    const currentTimeElem: HTMLDivElement | null =
      document.querySelector(".current-time");
    const totalTimeElem: HTMLDivElement | null =
      document.querySelector(".total-time");
    const timelineContainer: HTMLDivElement | null = document.querySelector(
      `.${styles["timeline-container"]}`
    );

    if (currentTimeElem && totalTimeElem && video && timelineContainer) {
      totalTimeElem.textContent = formatDuration(video.duration);
      currentTimeElem.textContent = formatDuration(video.currentTime);
      const percent = video.currentTime / video.duration;
      timelineContainer.style.setProperty(
        "--progress-position",
        percent.toString()
      );
    }
  };

  // Обработчик изменения скорости воспроизведения видео
  const handlePlaybackSpeed = () => {
    const speedBtn: HTMLDivElement | null =
      document.querySelector(".speed-btn");
    const video: HTMLVideoElement | null = document.querySelector("video");

    if (speedBtn && video) {
      let newPlaybackRate = video.playbackRate + 0.25;
      if (newPlaybackRate > 2) newPlaybackRate = 0.25;
      video.playbackRate = newPlaybackRate;
      speedBtn.textContent = `${newPlaybackRate}x`;
    }
  };

  const [isScrubbing, setIsScrubbing] = useState<boolean>(false);
  const [wasPaused, setWasPaused] = useState<boolean>();

  const handleScrubbing = (e: any) => {
    const timelineContainer: HTMLDivElement | null = document.querySelector(
      `.${styles["timeline-container"]}`
    );
    const video: HTMLVideoElement | null = document.querySelector("video");

    if (timelineContainer && video) {
      const rect = timelineContainer.getBoundingClientRect();
      const percent =
        Math.min(Math.max(0, e.screenX - rect.x), rect.width) / rect.width;
      const isScrubbingg = (e.buttons & 1) === 1;

      setIsScrubbing(isScrubbingg);
      if (isScrubbing) {
        setWasPaused(video.paused);
        video.pause();
        setIsMuted(true);
      } else {
        video.currentTime = percent * video.duration;
        if (!wasPaused) {
          video.play();
          setPaused(false);
        }
      }
    }

    handleTimelineUpdate(e);
  };

  function handleTimelineUpdate(e: any) {
    const timelineContainer: HTMLDivElement | null = document.querySelector(
      `.${styles["timeline-container"]}`
    );
    const thumbnailImg: HTMLDivElement | null = document.querySelector(
      `.${styles["thumbnail-img"]}`
    );
    if (timelineContainer && thumbnailImg) {
      const rect = timelineContainer.getBoundingClientRect();
      const percent =
        Math.min(Math.max(0, e.screenX - rect.x), rect.width) / rect.width;
      timelineContainer.style.setProperty(
        "--preview-position",
        percent.toString()
      );

      if (isScrubbing) {
        e.preventDefault();
        timelineContainer.style.setProperty(
          "--progress-position",
          percent.toString()
        );
      }
    }
  }

  // Форматирование чисел с добавлением нулей перед однозначными цифрами
  const leadingZeroFormatter = new Intl.NumberFormat(undefined, {
    minimumIntegerDigits: 2,
  });

  // Форматирование длительности видео в формат часы:минуты:секунды
  function formatDuration(time: number): string {
    const seconds = Math.floor(time % 60);
    const minutes = Math.floor(time / 60) % 60;
    const hours = Math.floor(time / 3600);

    if (hours === 0) {
      return `${minutes}:${leadingZeroFormatter.format(seconds)}`;
    } else {
      return `${hours}:${leadingZeroFormatter.format(
        minutes
      )}:${leadingZeroFormatter.format(seconds)}`;
    }
  }

  // Перемотка видео на указанную длительность
  function skip(duration: number) {
    const video: HTMLVideoElement | null = document.querySelector("video");
    if (video) {
      video.currentTime += duration;
    }
  }

  // Добавляем обработчик событий клавиш при монтировании компонента
  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("fullscreenchange", handleFullScreenChange);
    const timelineContainer = document.querySelector(
      `.${styles["timeline-container"]}`
    );
    if (timelineContainer) {
      timelineContainer.addEventListener("mousemove", handleTimelineUpdate);
      timelineContainer.addEventListener("mousedown", handleScrubbing);
    }

    const handleMouseMove = (e: any) => {
      if (isScrubbing) {
        handleTimelineUpdate(e);
      }
    };

    const handleMouseUp = (e: any) => {
      if (isScrubbing) {
        handleScrubbing(e);
      }
    };
    document.addEventListener("mouseup", handleMouseUp);
    document.addEventListener("mousemove", handleMouseMove);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("fullscreenchange", handleFullScreenChange);
      document.removeEventListener("mouseup", handleMouseUp);
      document.removeEventListener("mousemove", handleMouseMove);
      if (timelineContainer) {
        timelineContainer.removeEventListener(
          "mousemove",
          handleTimelineUpdate
        );
        timelineContainer.removeEventListener("mousedown", handleScrubbing);
      }
    };
  }, []);

  // Обработчик воспроизведения/паузы видео
  const handlePlayPause = () => {
    const video: HTMLVideoElement | null = document.querySelector("video");
    setPaused(!video?.paused);
    video?.paused ? video?.play() : video?.pause();
  };

  return (
    <div
      className={classNames(
        styles["video-container"],
        paused && styles.paused,
        isTheater && styles.theater,
        isFullScreen && styles["full-screen"],
        isMuted && styles.muted,
        isScrubbing && styles.scrubbing
      )}
      onContextMenu={handleContextMenu}
      data-volume-level={isMuted ? "muted" : "high"}
    >
      <img className={styles["thumbnail-img"]} src="" alt="" />
      <div className={styles["video-controls-container"]}>
        <div className={styles["timeline-container"]}>
          <div className={styles.timeline}>
            <img className={styles["preview-img"]} />
            <div className={styles["thumb-indicator"]}></div>
          </div>
        </div>
        <div className={styles.controls}>
          <button
            className={styles["play-pause-button"]}
            onClick={handlePlayPause}
          >
            <svg className={styles["play-icon"]} viewBox="0 0 24 24">
              <path fill="currentColor" d="M8,5.14V19.14L19,12.14L8,5.14Z" />
            </svg>
            <svg className={styles["pause-icon"]} viewBox="0 0 24 24">
              <path fill="currentColor" d="M14,19H18V5H14M6,19H10V5H6V19Z" />
            </svg>
          </button>
          <div className={styles["volume-container"]}>
            <button className={styles["mute-btn"]} onClick={handleMute}>
              <svg className={styles["volume-high-icon"]} viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M14,3.23V5.29C16.89,6.15 19,8.83 19,12C19,15.17 16.89,17.84 14,18.7V20.77C18,19.86 21,16.28 21,12C21,7.72 18,4.14 14,3.23M16.5,12C16.5,10.23 15.5,8.71 14,7.97V16C15.5,15.29 16.5,13.76 16.5,12M3,9V15H7L12,20V4L7,9H3Z"
                />
              </svg>
              <svg className={styles["volume-low-icon"]} viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M5,9V15H9L14,20V4L9,9M18.5,12C18.5,10.23 17.5,8.71 16,7.97V16C17.5,15.29 18.5,13.76 18.5,12Z"
                />
              </svg>
              <svg className={styles["volume-muted-icon"]} viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M12,4L9.91,6.09L12,8.18M4.27,3L3,4.27L7.73,9H3V15H7L12,20V13.27L16.25,17.53C15.58,18.04 14.83,18.46 14,18.7V20.77C15.38,20.45 16.63,19.82 17.68,18.96L19.73,21L21,19.73L12,10.73M19,12C19,12.94 18.8,13.82 18.46,14.64L19.97,16.15C20.62,14.91 21,13.5 21,12C21,7.72 18,4.14 14,3.23V5.29C16.89,6.15 19,8.83 19,12M16.5,12C16.5,10.23 15.5,8.71 14,7.97V10.18L16.45,12.63C16.5,12.43 16.5,12.21 16.5,12Z"
                />
              </svg>
            </button>
            <input
              className={styles["volume-slider"]}
              type="range"
              min="0"
              max="1"
              step="any"
              onInput={handleInputVolume}
            />
          </div>
          <div className={styles["duration-container"]}>
            <div className="current-time">0:00</div>/
            <div className="total-time"></div>
          </div>
          {/* <button className={styles["captions-btn"]}>
            <svg viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M18,11H16.5V10.5H14.5V13.5H16.5V13H18V14A1,1 0 0,1 17,15H14A1,1 0 0,1 13,14V10A1,1 0 0,1 14,9H17A1,1 0 0,1 18,10M11,11H9.5V10.5H7.5V13.5H9.5V13H11V14A1,1 0 0,1 10,15H7A1,1 0 0,1 6,14V10A1,1 0 0,1 7,9H10A1,1 0 0,1 11,10M19,4H5C3.89,4 3,4.89 3,6V18A2,2 0 0,0 5,20H19A2,2 0 0,0 21,18V6C21,4.89 20.1,4 19,4Z"
              />
            </svg>
          </button> на будущее */}
          <button
            className={classNames("speed-btn", styles["wide-btn"])}
            onClick={handlePlaybackSpeed}
          >
            1x
          </button>
          <button
            className={styles["mini-player-btn"]}
            onClick={handleMiniPlayer}
          >
            <svg viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zm-10-7h9v6h-9z"
              />
            </svg>
          </button>
          <button className={styles["theater-btn"]} onClick={handleTheaterMode}>
            <svg className={styles.tall} viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M19 6H5c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 10H5V8h14v8z"
              />
            </svg>
            <svg className={styles.wide} viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M19 7H5c-1.1 0-2 .9-2 2v6c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zm0 8H5V9h14v6z"
              />
            </svg>
          </button>
          <button
            className={styles["full-screen-btn"]}
            onClick={handleFullScreen}
          >
            <svg className={styles.open} viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"
              />
            </svg>
            <svg className={styles.close} viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"
              />
            </svg>
          </button>
        </div>
      </div>
      <video
        src={props.src}
        onClick={handlePlayPause}
        onPlay={() => {
          setPaused(false);
        }}
        onPause={() => {
          setPaused(true);
        }}
        onDoubleClick={handleFullScreen}
        onLoadedData={handleLoadedVideo}
        onTimeUpdate={handleLoadedVideo}
        autoPlay
      ></video>
    </div>
  );
};

export default Player;
