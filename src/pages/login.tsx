import React, { useEffect } from "react";
import CardInput from "../components/CardInput";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useSignInMutation } from "../api/auth";
import { USER } from "../consts/user";

interface User {
  username: string;
  password: string;
}

const Login = () => {
  const navigate = useNavigate();
  const [signIn, result] = useSignInMutation();

  const onLogin = (data: any) => {
    signIn(data);
  };

  useEffect(() => {
    if (result.data) {
      localStorage.setItem("token", result.data?.access);
      localStorage.setItem("user", JSON.stringify(result.data?.user));
      navigate("/");
    }
  }, [result]);

  useEffect(() => {
    if (USER) {
      navigate("/");
    }
  }, []);

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Никнейм", type: "text", name: "username" },
          { title: "Email", type: "email", name: "email" },
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
