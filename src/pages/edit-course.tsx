import React from 'react'
import CardInput from '../components/CardInput'

const EditCourse = () => {
    const onEditCourse = () => {
        return '';
    }

  return (
    <div>
        <CardInput
        inputsData={[
          { title: "Заголовок курса", type: "text", name: "title" },
          { title: "Описание курса", type: "text", name: "description" },
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
          { title: "Описание видео", type: "text", name: "description" },
          {
            title: "Добавить видео",
            type: "file",
            name: "profile_image",
            hidden: "hidden",
          },
        ]}
        formTitle="Редактировать курс"
        buttonText="Опубликовать"
        to="/course"
        function={onEditCourse}
      />
    </div>
  )
}

export default EditCourse