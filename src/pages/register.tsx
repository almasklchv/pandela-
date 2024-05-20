import React, { useEffect } from "react";
import CardInput from "../components/CardInput";
import { useSignUpMutation } from "../api/auth";
import { useNavigate } from "react-router-dom";
import { USER } from "../consts/user";

interface User {
  name: string;
  username: string;
  email: string;
  password: string;
}

const Register = () => {
  const navigate = useNavigate();
  const [signUp, result] = useSignUpMutation();
  const onRegister = (user: User) => {
    signUp(user);
  };

  useEffect(() => {
    if (result.data) {
      localStorage.setItem("token", result.data?.access);
      navigate("/login");
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
