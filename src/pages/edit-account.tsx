import React from 'react'
import CardInput from '../components/CardInput'

const EditAccount = () => {
    const onEdit = () => {
        return '';
    }

  return (
    <div>
        <CardInput
        inputsData={[
          { title: "Никнейм", type: "text", name: "username" },
          { title: "Имя и Фамилия", type: "text", name: "username" },
          { title: "Почта", type: "email", name: "email" },
          { title: "Фотография профиля", type: "file", name: "profile_image", hidden: 'hidden' },
        ]}
        formTitle="Редактировать аккаунт"
        buttonText="Изменить"
        to="/profile"
        function={onEdit}
      />
    </div>
  )
}

export default EditAccount