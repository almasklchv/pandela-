import React from "react";
import styles from "../styles/components/Logo.module.scss";
import { useNavigate } from "react-router-dom";

const Logo = (props: any) => {
  return (
    <div>
      <div
        className={styles.logo}
        onClick={() => {
          window.location.href = "/";
        }}
        {...props}
      >
        <img
          className={styles.logoImg}
          src="/icons/logo.png"
          alt="logo"
          height={25}
        />
        <p className={styles.logoTitle}>Pandela</p>
      </div>
    </div>
  );
};

export default Logo;
