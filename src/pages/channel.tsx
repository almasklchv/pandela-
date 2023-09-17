import React from "react";
import styles from "../styles/pages/Profile.module.scss";
import CardVideo from "../components/CardVideo";
import { videos } from "../fake-db/main";
import { users } from "../fake-db/main";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import Error404 from "./404";

interface IChannel {
  userId?: string;
}

const Channel = (props: IChannel) => {
  const { id } = useParams();
  console.log(id);
  const navigate = useNavigate();
  const location = useLocation();
  const userId = location.search.slice(4);
  const user = users.filter((user) => id && id === user.userId);

  if (user[0]) {
    return (
      <div className={styles.channel}>
        <div className={styles.container}>
          <img
            className={styles.profileBanner}
            src="https://3.downloader.disk.yandex.ru/preview/66d3ba9cf2834f6c32cbfac1b851ed200e8e8a870e68244e5428bdb42bc69fba/inf/O1FL5xXdeAtSZo4OWskn4CUeEDlc8liDg6FnmJgmcdIXVn86IFDFZ-f8mxTPaV0dl7NPtgwwSSDzlvmTRDZ1sg%3D%3D?uid=1559815427&filename=profile-banner.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1559815427&tknv=v2&size=1905x867"
            alt="Шапка профиля"
          />
          <div className={styles.profileInfo}>
            <img
              className={styles.profilePhoto}
              src={user[0].profilePhoto}
              alt="Фото профиля"
              width={82}
              height={82}
            />
            <div className={styles.personInfo}>
              <div className={styles.nameWithSubscribe}>
                <p className={styles.name}>{user[0].name}</p>
                <button className={styles.subscribeBtn}>Подписаться</button>
              </div>
              <p className={styles.username}>
                @{user[0].username} {user[0].subscribersCount}
              </p>
              <p className={styles.bio}>{user[0].bio}</p>
            </div>
          </div>
          <div className={styles.videos}>
            {videos.map((video) => {
              if (video.userId === id) {
                return <CardVideo {...video} />;
              } else {
                return "";
              }
            })}
          </div>
        </div>
      </div>
    );
  } else {
    return <Error404 />;
  }
};

export default Channel;
