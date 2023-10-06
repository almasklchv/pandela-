import React from "react";
import styles from "../styles/pages/AddVideo.module.scss";
import CardInput from "../components/CardInput";
import { playlists } from "../fake-db/main";

const AddVideo = () => {
  const addVideo = () => {
    return "";
  };

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Заголовок", type: "text", name: "title" },
          { title: "Описание", type: "text", name: "description" },
          {
            title: "Выберите плейлист",
            type: playlists.map((playlist) => playlist.title),
            name: "playlist",
          },
          {
            title: "Кто увидит видео?",
            type: ["Только я", "Все люди"],
            name: "is_published"
          },
          {
            title: "Добавить обложку",
            type: "file",
            name: "profile_image",
            hidden: "hidden",
          },
          {
            title: "Добавить видео",
            type: "file",
            name: "video_file",
            hidden: "hidden",
          },
        ]}
        formTitle="Публикация видео"
        buttonText="Опубликовать"
        to="/profile"
        function={addVideo}
      />
    </div>
  );
};

export default AddVideo;
