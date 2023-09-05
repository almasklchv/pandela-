import React from "react";
import { Link } from "react-router-dom";
import styles from '../styles/components/Navbar.module.scss'

interface INavbar {
  data: Links[];
}

interface Links {
  title: string;
  to: string;
}

const Navbar = (props: INavbar) => {
  return (
    <div>
      <nav className={styles.nav}>
        {props.data.map((link: Links) => (
          <Link to={link.to}>{link.title}</Link>
        ))}
      </nav>
    </div>
  );
};

export default Navbar;
