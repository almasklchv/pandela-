let popularCourses = document.querySelector('.popular-courses');
let newCourses = document.querySelector('.new-courses');

export function updateVisibleItems (item) {
    const parentWidth = document.body.clientWidth - 92.8;
    const visibleItems = Math.floor(parentWidth / 329); 
    if (parentWidth >= 692.2) {
        item.style.width = (visibleItems * 359) + 'px';
        item.style.overflow = 'hidden';
        
        item.children[0].style.flexWrap = "nowrap";
    } else {
        item.style.width = '100%';
        item.style.overflow = '';
        item.children[0].style.flexWrap = "wrap";
    }
    if (visibleItems <= 1) {
        if (item.children[0].children[0].style.marginRight != '0px') {
            item.children[0].style.marginRight = '0px';
            for (let i = 0; i < item.children[0].children.length; i++) {
                item.children[0].children[i].style.marginRight = '0';
            }
        }
    }
    
    if (parentWidth >= 520.2) {
        if (item.children[0].children[0].style.marginRight == '0px') {
            item.children[0].style.marginRight = '-30px';
            for (let i = 0; i < item.children[0].children.length; i++) {
                item.children[0].children[i].style.marginRight = '30px  ';
            }
        }
    }

    if (parentWidth <= 677.2) {
        popularCourses.style.left = '';
        newCourses.style.left = '';
        for (let i = 0; i < item.children[0].children.length; i++) {
            item.children[0].children[i].style.marginRight = '0px';
        }
    }

    if (parentWidth >= 528) {
        for (let i = 0; i < item.children[0].children.length; i++) {
            item.children[0].children[i].style.marginRight = '30px';
        }
    }
}


export function nextSlide (item) {
    const parentWidth = document.body.clientWidth - 102.8;
    const visibleItems = Math.floor(parentWidth / 329);
    const offset = visibleItems * 359;
    const left = parseInt(item.style.left);
    if (item.style.left) {
        item.style.left = -(offset - left)-26 + 'px';
    } else {
        item.style.left = -(offset)-26 + 'px';
    }

    if (Math.abs(left) + offset >= (item.children.length * 359)) {
        item.style.left = left + 'px';
    }
}

export function prevSlide (item) {
    const parentWidth = document.body.clientWidth - 102.8;
    const visibleItems = Math.floor(parentWidth / 329);
    const offset = visibleItems * 359;
    const left = parseInt(item.style.left);
    if (item.style.left) {
        item.style.left = left + offset + 26 + 'px';
    } else {
        item.style.left = offset + 26 + 'px';
    }
    
    if ((left + offset) > 0  ) {
        item.style.left = 0;
    }
}


export function addEventToCoursesCarousel() {
    document.addEventListener('DOMContentLoaded', () => {
        const courses = document.querySelectorAll(".courses-carousel")[0];
        updateVisibleItems(courses)
    });
    document.addEventListener('DOMContentLoaded', () => {
        const courses = document.querySelectorAll(".courses-carousel")[1];
        updateVisibleItems(courses)
    });
    window.addEventListener("resize", () => {
        const courses = document.querySelectorAll(".courses-carousel")[0];
        updateVisibleItems(courses)
    });
    window.addEventListener("resize", () => {
        const courses = document.querySelectorAll(".courses-carousel")[1];
        updateVisibleItems(courses)
    });
    document.querySelectorAll('.right-btn')[0].addEventListener('click', () => {
        const courses = document.querySelector(".popular-courses");
        nextSlide(courses)
    })
    document.querySelectorAll('.right-btn')[1].addEventListener('click', () => {
        const courses = document.querySelector(".new-courses");
        nextSlide(courses)
    })
    document.querySelectorAll('.left-btn')[0].addEventListener('click', () => {
        const courses = document.querySelector(".popular-courses");
        prevSlide(courses)
    })
    document.querySelectorAll('.left-btn')[1].addEventListener('click', () => {
        const courses = document.querySelector(".new-courses");
        prevSlide(courses)
    })
}
