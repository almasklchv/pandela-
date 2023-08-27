import { openOrCloseMenu, toggleMenu } from "./base.js";
import { addEventToCoursesCarousel } from "./courses-carousel.js";
import { videoPlayer } from "./course-page.js";
import { onBurgerMenu } from "./burger-menu.js";

document.querySelector('.dropdown-menu').addEventListener('click', openOrCloseMenu);
if (document.querySelector('.burger-icon')) {
    document.querySelector('.burger-icon').addEventListener('click', toggleMenu);   
}

if (document.querySelectorAll('.popular-courses').length > 0) {
    addEventToCoursesCarousel();
}

if (document.querySelector('.video-player')) {
    videoPlayer();
}

onBurgerMenu();