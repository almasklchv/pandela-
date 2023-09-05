import React from "react";
import CardInput from "../../components/CardInput";

const Register = () => {
  const onRegister = () => {
    return '';
  }

  return (
    <div>
      <CardInput
        inputsData={[
          { title: "Полное имя", type: "text", name: "fullname" },
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
