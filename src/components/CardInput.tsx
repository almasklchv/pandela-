import React, { ChangeEvent } from "react";
import styles from "../styles/components/CardInput.module.scss";
import classNames from "classnames";
import { Link, useNavigate } from "react-router-dom";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";

interface ICardInput {
  inputsData: Inputs[];
  formTitle: string;
  buttonText: string;
  to: string;
  linkText?: string;
  function: (data: any) => {};
}
interface Inputs {
  title: string;
  type: string | string[];
  name: string;
  hidden?: string;
}

const CardInput = (props: ICardInput) => {
  const schemaFields: any = {};
  const navigate = useNavigate();

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
                <p className={styles.inputTitle}>
                  {input.title}{" "}
                  {input.title === "Выберите плейлист" && (
                    <a href="/add-playlist">· Создать новый плейлист</a>
                  )}
                </p>
                {typeof input.type === "object" ? (
                  <select className={styles.selectCategory}>
                    {input.type.map((option: string) => (
                      <option className={styles.optionCategory}>
                        {option}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    className={classNames(styles.input, input.name)}
                    type={input.type}
                    hidden={input.hidden}
                    {...register(input.name)}
                  />
                )}

                {input.type === "file" && (
                  <div className={styles.uploadFile}>
                    <button
                      onClick={(e: any) => {
                        e.preventDefault();

                        let isVideoFile =
                          e.target.classList.contains("video_file_btn");
                        let isProfileImage =
                          e.target.classList.contains("profile_image_btn");
                        let isBannerImage =
                          e.target.classList.contains("banner_image_btn");

                        const uploadBtn: HTMLInputElement | null =
                          document.querySelector(
                            (isVideoFile && ".video_file") ||
                              (isProfileImage && ".profile_image") ||
                              (isBannerImage && ".banner_image")
                          );
                        console.log(uploadBtn);
                        uploadBtn?.click();
                        const uploadText: HTMLSpanElement =
                          document.querySelector(
                            (isVideoFile && ".video_file_text") ||
                              (isProfileImage && ".profile_image_text") ||
                              (isBannerImage && ".banner_image_text")
                          ) as HTMLSpanElement;
                        if (uploadBtn) {
                          uploadBtn.addEventListener("change", (e: Event) => {
                            const inputElement = e.target as HTMLInputElement;
                            if (inputElement) {
                              const match = inputElement.value.match(
                                /[/\\]([\w\d\s.\-()]+)$/
                              );
                              if (match) {
                                uploadText.innerText = match[1];
                              }
                            }
                          });
                        }
                      }}
                      className={classNames(
                        styles.uploadFileBtn,
                        input.name + "_btn"
                      )}
                    >
                      Выбрать файл
                    </button>
                    <span
                      className={classNames(
                        styles.uploadText,
                        input.name + "_text"
                      )}
                    >
                      Файл не выбран
                    </span>
                  </div>
                )}
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
        {props.linkText && (
          <Link className={styles.link} to={props.to}>
            {props.linkText}
          </Link>
        )}
      </div>
    </div>
  );
};

export default CardInput;
