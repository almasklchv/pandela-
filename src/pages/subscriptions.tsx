import React from "react";
import CardChannel from "../components/CardChannel";
import styles from "../styles/pages/Subscriptions.module.scss"
import { users } from "../fake-db/main";
import { useNavigate } from "react-router-dom";

const Subscriptions = () => {
  const subscriptions: any[] = [];
  users[0].subscriptions.forEach((subscription) => {
    subscriptions.push(users.filter((user) => user.userId === subscription)[0]);
  });

  return (
    <div className={styles.subscriptions}>
      {subscriptions.map((subscription: any) => (
        <CardChannel  {...subscription} />
      ))}
    </div>
  );
};

export default Subscriptions;
