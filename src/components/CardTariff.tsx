import React from "react";
import styles from "../styles/components/CardTariff.module.scss";

interface ICardTariff {
  name: string;
  price: string;
  opportunities: string[];
  btnText: string;
}

const CardTariff = (props: ICardTariff) => {
  return (
    <div className={styles.card}>
      <h4 className={styles.title}>{props.name}</h4>
      <p className={styles.price}>{props.price}</p>
      <hr className={styles.line} />
      {props.opportunities.map((opportunity) => (
        <div className={styles.opportunities}>
          <div className={styles.opportunity}>
            <img
              className={styles.opportunityImg}
              src="icons/check.svg"
              alt="Галочка"
              width={20}
              height={15}
            />
            <p className={styles.opportunityName}>{opportunity}</p>
          </div>
        </div>
      ))}
      <button className={styles.btn}>{props.btnText}</button>
    </div>
  );
};

export default CardTariff;
