import React from "react";
import styles from "../styles/components/BottomNavigationMenu.module.scss";
import { useLocation, useNavigate } from "react-router-dom";

const navigationItems = [
  { path: "/", label: "Главная", icon: "home" },
  { path: "/subscriptions", label: "Подписки", icon: "subscriptions" },
  { path: "/courses", label: "Курсы", icon: "courses" },
  { path: "/videos", label: "Видео", icon: "videos" },
];

const BottomNavigationMenu = () => {
  const url = useLocation();
  const navigate = useNavigate();

  return (
    <div>
      <div className={styles["bottom-navigation-menu"]}>
        {navigationItems.map((item) => (
          <div
            key={item.path}
            className={styles[item.icon]}
            onClick={() => navigate(item.path)}
          >
            <img
              src={`/icons/bottom-navigation-menu/${
                url.pathname === item.path ? "active" : "non-active"
              }/${item.icon}.svg`}
              alt={`${item.label} page`}
            />
            <p>{item.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BottomNavigationMenu;
