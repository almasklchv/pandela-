import React from "react";
import CardInput from "../components/CardInput";

interface User {
  name: string;
  username: string;
  email: string;
  password: string;
}

const Register = () => {
  const onRegister = (user: User) => {
    return fetch("https://youtube-new-s0hr.onrender.com/api/auth/signup/", {
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
          { title: "Ваше имя", type: "text", name: "name" },
          { title: "Придумайте никнейм", type: "text", name: "username" },
          { title: "Почта", type: "email", name: "email" },
          { title: "Пароль", type: "password", name: "password" },
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
