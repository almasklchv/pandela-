import React from "react";
import CardInput from "../components/CardInput";
import { videos } from "../fake-db/main";

const AddPlaylist = () => {
  const addPlaylist = () => {
    return "";
  };

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Заголовок", type: "text", name: "title" },
          { title: "Описание", type: "text", name: "description" },
          {
            title: "Добавить видео",
            type: videos.map((video) => video.title),
            name: "video",
          },
          {
            title: "Добавить обложку",
            type: "file",
            name: "profile_image",
            hidden: "hidden",
          },
        ]}
        formTitle="Создание плейлиста"
        buttonText="Опубликовать"
        to="/profile"
        function={addPlaylist}
      />
    </div>
  );
};

export default AddPlaylist;
