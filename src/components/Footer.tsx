import React from "react";
import styles from "../styles/components/Footer.module.scss";
import Logo from "./Logo";
import Navbar from "./Navbar";

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.left}>
        <Logo />
        <Navbar
          data={[
            { title: "Оформить подписку", to: "/premium" },
            { title: "Выложить свой курс", to: "/" },
            { title: "О нас", to: "/" },
          ]}
        />
      </div>
      <div className={styles.right}>
        <div className={styles.socialMediaGroup}>
          <a className={styles.link} href="https://tiktok.com">
            <img src="/icons/tiktok.svg" alt="tiktok" />
          </a>
          <a className={styles.link} href="https://vk.com">
            <img src="/icons/vk.svg" alt="vk" />
          </a>
          <a className={styles.link} href="https://instagram.com">
            <img src="/icons/instagram.svg" alt="instagram" />
          </a>
        </div>
        <p>© 2023 Все права защищены</p>
      </div>
    </footer>
  );
};

export default Footer;
