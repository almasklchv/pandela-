import React from "react";
import CardInput from "../../components/CardInput";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate()

  const onLogin = () => {
    navigate('/')
    return 'Hello';
  }

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Почта", type: "email", name: "email" },
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
