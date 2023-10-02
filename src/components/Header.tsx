import React, { useEffect, useState } from "react";
import styles from "../styles/components/Header.module.scss";
import { useLocation, useNavigate } from "react-router-dom";
import Logo from "./Logo";
import BurgerMenu from "./BurgerMenu";
import classNames from "classnames";

const Header = (props: { isBurgerMenu: boolean }) => {
  const navigate = useNavigate();
  const [burgerMenuClicked, setBurgerMenuClicked] = useState(false);

  const location = useLocation();
  const searchQuery = location.search.slice(14);
  useEffect(() => {
    if (searchQuery !== "") {
      const search: HTMLInputElement | null = document.querySelector(
        `.${styles.search}`
      );
      if (search) {
        search.value = decodeURIComponent(searchQuery);
      }
    }
  }, [])
  

  const handleBurgerMenuClick = () => {
    setBurgerMenuClicked(!burgerMenuClicked);
  };

  const handleSearchClicked = () => {
    if (window.innerWidth <= 710) {
      const search: HTMLInputElement | null = document.querySelector("#search");
      search?.focus();
      const right: HTMLDivElement | null = document.querySelector(
        "." + styles.right
      );
      const left: HTMLDivElement | null = document.querySelector(
        "." + styles.left
      );
      const backBtn: HTMLSpanElement | null = document.querySelector(
        `.${styles.back}`
      );
      if (right && left && backBtn) {
        right.style.display = "none";
        left.style.display = "none";
        backBtn.style.display = "block";
      }

      if (window.innerWidth <= 600) {
        const searchForm: HTMLDivElement | null =
          document.querySelector(`.search-form`);
        if (searchForm) {
          searchForm.classList.add(styles.searchFormFocus);
        }
      }
    }
  };

  const handleSearchSubmit = (e: any) => {
    e.preventDefault();
    const search: HTMLInputElement | null = document.querySelector(
      `.${styles.search}`
    );
    navigate(`/results?search_query=${search?.value}`);
  };

  const handleBackClicked = () => {
    const right: HTMLDivElement | null = document.querySelector(
      "." + styles.right
    );
    const left: HTMLDivElement | null = document.querySelector(
      "." + styles.left
    );
    const backBtn: HTMLSpanElement | null = document.querySelector(
      `.${styles.back}`
    );
    if (right && left && backBtn) {
      right.style.display = "block";
      left.style.display = "flex";
      backBtn.style.display = "none";
    }
    if (window.innerWidth <= 600) {
      const searchForm: HTMLDivElement | null =
        document.querySelector(`.search-form`);
      if (searchForm) {
        searchForm.classList.remove(styles.searchFormFocus);
      }
    }
  };

  return (
    <header className={styles.headerContainer}>
      <div className={styles.header}>
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
          <Logo />
        </div>
        <div className={styles.center}>
          <span className={styles.back} onClick={handleBackClicked}></span>
          <form
            className={classNames(styles.searchForm, "search-form")}
            onSubmit={handleSearchSubmit}
          >
            <span
              className={styles.searchIcon}
              onClick={handleSearchClicked}
            ></span>
            <input
              className={styles.search}
              type="search"
              name="search"
              id="search"
              placeholder="Искать"
              onFocus={handleSearchClicked}
              onBlur={handleBackClicked}
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
      </div>
    </header>
  );
};

export default Header;
