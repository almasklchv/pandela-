// BurgerMenu.js
import React, { useEffect, useState } from "react";
import styles from "../styles/components/BurgerMenu.module.scss";
import { useLocation, useNavigate } from "react-router-dom";
import classNames from "classnames";

const BurgerMenu = (props: { burgerMenuClicked: boolean }) => {
  const navigate = useNavigate();
  const [selectedLinkIndex, setSelectedLinkIndex] = useState(0);

  const menuItems = [
    {
      text: "Главная",
      route: "/",
      icon: `/icons/bottom-navigation-menu/non-active/home.svg`,
    },
    {
      text: "Подписки",
      route: "/subscriptions",
      icon: "/icons/bottom-navigation-menu/non-active/subscriptions.svg",
    },
    {
      text: "Курсы",
      route: "/courses",
      icon: "/icons/bottom-navigation-menu/non-active/courses.svg",
    },
    {
      text: "Видео",
      route: "/videos",
      icon: "/icons/bottom-navigation-menu/non-active/videos.svg",
    },
  ];
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === "/subscriptions") {
      setSelectedLinkIndex(1);
    } else if (location.pathname === "/courses") {
      setSelectedLinkIndex(2);
    } else if (location.pathname === "/videos") {
      setSelectedLinkIndex(3);
    } else {
      setSelectedLinkIndex(0);
    }
  }, []);

  const handleItemClick = (index: number, route: string) => {
    setSelectedLinkIndex(index);
    if (route === "/") {
      window.location.href = route;
    }
    navigate(route);
  };

  return (
    <nav
      className={classNames(styles["burger-menu"], {
        [styles.active]: props.burgerMenuClicked,
      })}
    >
      <ul className={styles.links}>
        {menuItems.map((item, index) => (
          <li
            key={index}
            className={classNames(styles.link, {
              [styles.selectedLink]: selectedLinkIndex === index,
            })}
            onClick={() => handleItemClick(index, item.route)}
          >
            <img className={styles.linkImg} src={item.icon} alt={item.text} />
            <p
              className={classNames(styles.linkText, {
                [styles.visible]: props.burgerMenuClicked,
              })}
            >
              {item.text}
            </p>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default BurgerMenu;
