import React from "react";
import styles from "../styles/components/Header.module.scss";
import { useNavigate } from "react-router-dom";
import Logo from "./Logo";

const Header = () => {
  const navigate = useNavigate();





  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <img src="icons/burger-menu.svg" alt="burger menu icon" height={20} />
        <Logo />
      </div>
      <div className={styles.center}>
        <form className={styles.searchForm}>
          <span className={styles.searchIcon}></span>
          <input
            className={styles.search}
            type="search"
            name="search"
            id="search"
            placeholder="Искать"
          />
        </form>
      </div>
      <div className={styles.right}>
        <div className={styles.signIn} onClick={() => { navigate("/login") }}>
          <span className={styles.accountImg}></span>
          <p className={styles.signInTitle}>Войти</p>
        </div>
      </div>
    </header>
  );
};

export default Header;
