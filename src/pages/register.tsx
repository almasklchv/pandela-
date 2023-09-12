import React from "react";
import CardInput from "../components/CardInput";

interface User {
  username: string;
  email: string;
  password1: string;
  password2: string;
}

const Register = () => {
  const onRegister = (user: User) => {
    return fetch("https://aphinapandela.onrender.com/api/users/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("DATA:", data);
      });
  };

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Никнейм", type: "text", name: "username" },
          { title: "Почта", type: "email", name: "email" },
          { title: "Пароль", type: "password", name: "password1" },
          { title: "Подтвердите пароль", type: "password", name: "password2" },
        ]}
        formTitle="Регистрация"
        buttonText="Зарегистрироваться"
        to="/login"
        linkText="Уже зарегистрированы? Войти"
        function={onRegister}
      />
    </div>
  );
};

export default Register;
