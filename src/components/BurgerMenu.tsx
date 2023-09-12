// BurgerMenu.js
import React, { useState } from "react";
import styles from "../styles/components/BurgerMenu.module.scss";
import { useNavigate } from "react-router-dom";
import classNames from "classnames";

const BurgerMenu = (props: {burgerMenuClicked: boolean}) => {
  const navigate = useNavigate();
  const [selectedLinkIndex, setSelectedLinkIndex] = useState(0);

  const menuItems = [
    {
      text: "Главная",
      route: "/",
      icon: "icons/home.svg",
    },
    {
      text: "Подписки",
      route: "/subscriptions",
      icon: "icons/subscriptions.svg",
    },
    {
      text: "Курсы",
      route: "/courses",
      icon: "icons/courses.svg",
    },
    {
      text: "Видео",
      route: "/videos",
      icon: "icons/videos.svg",
    },
  ];

  const handleItemClick = (index: number, route: string) => {
    setSelectedLinkIndex(index);
    navigate(route);
  };

  return (
    <nav className={classNames(styles['burger-menu'], {
      [styles.active]: props.burgerMenuClicked, 
    })}>
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
