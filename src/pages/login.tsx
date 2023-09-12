import React from "react";
import CardInput from "../components/CardInput";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface User {
  username: string;
  password: string;
}

async function checkUserCredentials(user: User) {
  fetch("https://aphinapandela.onrender.com/api/users/token/", {
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
}

const Login = () => {
  const navigate = useNavigate();

  const onLogin = (data: any) => {
    checkUserCredentials(data);
    navigate("/");
    return "Hello";
  };

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Никнейм", type: "text", name: "username" },
          { title: "Пароль", type: "password", name: "password" },
        ]}
        formTitle="Авторизация"
        buttonText="Войти"
        to="/register"
        linkText="Не зарегистрированы? Зарегистрироваться"
        function={onLogin}
      />
    </div>
  );
};

export default Login;
