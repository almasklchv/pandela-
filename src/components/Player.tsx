import React, { useEffect, useState } from "react";
import styles from "../styles/components/Player.module.scss";
import { useLocation } from "react-router-dom";
import classNames from "classnames";

const Player = () => {
  return (
    <div className={classNames(styles.player, styles.theater)}>
      <video src="videos/sample.mp4"></video>
    </div>
  );
};

export default Player;
