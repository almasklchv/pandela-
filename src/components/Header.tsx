import React, { useState } from "react";
import styles from "../styles/components/Header.module.scss";
import { useNavigate } from "react-router-dom";
import Logo from "./Logo";
import BurgerMenu from "./BurgerMenu";

const Header = (props: { isBurgerMenu: boolean }) => {
  const navigate = useNavigate();
  const [burgerMenuClicked, setBurgerMenuClicked] = useState(false);

  const handleBurgerMenuClick = () => {
    setBurgerMenuClicked(!burgerMenuClicked);
  };

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        {props.isBurgerMenu && (
          <img
            className={styles.burgerMenuBtn}
            src="/icons/burger-menu.svg"
            alt="burger menu icon"
            height={20}
            onClick={handleBurgerMenuClick}
          />
        )}
        <Logo style={{marginTop: '15px'}} />
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
        <div className={styles.signIn} onClick={() => navigate("/login")}>
          <span className={styles.accountImg}></span>
          <p className={styles.signInTitle}>Войти</p>
        </div>
      </div>
      {props.isBurgerMenu && (
        <div className={styles.burgerMenu}>
          <BurgerMenu burgerMenuClicked={burgerMenuClicked} />
        </div>
      )}
    </header>
  );
};

export default Header;
