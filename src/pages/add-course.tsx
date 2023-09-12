import React from "react";
import CardInput from "../components/CardInput";

const AddCourse = () => {
  const addCourse = () => {
    return "";
  };

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Заголовок", type: "text", name: "title" },
          { title: "Описание", type: "text", name: "description" },
          {
            title: "Выберите категорию",
            type: ["Программирование", "Дизайн", "Маркетинг"],
            name: "category",
          },
          {
            title: "Добавить заставку",
            type: "file",
            name: "profile_image",
            hidden: "hidden",
          },
        ]}
        formTitle="Создание курса"
        buttonText="Опубликовать"
        to="/profile"
        function={addCourse}
      />
    </div>
  );
};

export default AddCourse;
