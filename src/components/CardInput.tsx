import React from "react";
import styles from "../styles/components/CardInput.module.scss";
import { Link } from "react-router-dom";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";

interface ICardInput {
  inputsData: Inputs[];
  formTitle: string;
  buttonText: string;
  to: string;
  linkText: string;
  function: () => {};
}
interface Inputs {
  title: string;
  type: string;
  name: string;
}

const CardInput = (props: ICardInput) => {
  const schemaFields: any = {};

  props.inputsData.forEach((input) => {
    if (input.type === "email") {
      schemaFields[input.name] = yup
        .string()
        .email("Введите корректный email!")
        .required("Введите почту!");
    } else if (input.type === "password") {
      schemaFields[input.name] = yup
        .string()
        .min(8, "Минимум 8 символов!")
        .required();
    } else if (input.type === "text") {
      schemaFields[input.name] = yup
        .string()
        .required("Поле обязательно для заполнения!");
    }
  });

  const schema = yup.object().shape({
    ...schemaFields,
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });

  return (
    <div className={styles.card}>
      <div className={styles.container}>
        <h3 className={styles.formTitle}>{props.formTitle}</h3>
        <form onSubmit={handleSubmit(props.function)}>
          {props.inputsData.map((input: any) => {
            const error = errors[input.name]?.message?.toString();

            return (
              <>
                <p className={styles.inputTitle}>{input.title}</p>
                <input
                  className={styles.input}
                  type={input.type}
                  {...register(input.name)}
                />
                <p className={styles.error}>{error}</p>
              </>
            );
          })}
          <hr />
          <input
            className={styles.btn}
            type="submit"
            value={props.buttonText}
          />
        </form>
        <Link className={styles.link} to={props.to}>
          {props.linkText}
        </Link>
      </div>
    </div>
  );
};

export default CardInput;
