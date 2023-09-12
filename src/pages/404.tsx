import React from 'react'
import styles from '../styles/pages/404.module.scss'

const Error404 = () => {
  return (
    <div className={styles.container}>
        <h3>404</h3>
        <p>Такой страницы не существует</p>
    </div>
  )
}

export default Error404