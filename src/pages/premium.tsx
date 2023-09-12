import React from "react";
import styles from "../styles/pages/Premium.module.scss";
import classNames from "classnames";
import CardTariff from "../components/CardTariff";

const Premium = () => {
  const opportunities = [
    {
      title: "Режим Экран В Экране",
      imgPath: "icons/screen-in-screen.svg",
    },
    {
      title: "Нет рекламы",
      imgPath: "icons/no-ads.svg",
    },
    {
      title: "Нет ограничений",
      imgPath: "icons/no-restrictions.svg",
    },
    {
      title: "Скачивайте видео",
      imgPath: "icons/download-video.svg",
    },
  ];

  return (
    <div className={styles.premium}>
      <div className={styles.description}>
        <div className={styles.container}>
          <h2 className={styles.title}>Смотри без ограничений</h2>
          <p className={styles.desc}>
            С подпиской вам доступны удобные функции видео, отключение рекламы,
            возможность скачивать видео и весь сайт без каких-либо ограничений!
          </p>
          <div className={styles.buttons}>
            <button className={classNames(styles.btn, styles.btnDark)}>
              НАЧАТЬ
            </button>
            <button className={classNames(styles.btn, styles.btnTransparent)}>
              ОФОРМИТЬ ПОДПИСКУ
            </button>
          </div>
        </div>
      </div>
      <div className={styles.why}>
        <h2 className={styles.title}>Зачем вам подписка?</h2>
        <div className={styles.opportunities}>
          {opportunities.map((opportunity) => (
            <div className={styles.opportunity}>
              <img
                className={styles.opportunityImg}
                src={opportunity.imgPath}
                alt={opportunity.title}
                width={142}
                height={142}
              />
              <p className={styles.opportunityTitle}>{opportunity.title}</p>
            </div>
          ))}
        </div>
      </div>
      <div className={styles.feel}>
        <h2 className={styles.title}>Почувствуй свободу</h2>
        <p>Подписку можно оформить любой картой</p>
        <CardTariff
          name="Подписка"
          price="399 руб/мес"
          opportunities={[
            "Возможность просмотра экрана в экране",
            "Отсутствие рекламы",
            "Отсутствие ограничений",
            "Можно скачивать видео!",
          ]}
          btnText="ОФОРМИТЬ ПОДПИСКУ"
        />
      </div>
    </div>
  );
};

export default Premium;
