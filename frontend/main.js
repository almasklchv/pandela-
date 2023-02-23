let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')

if (token){
    loginBtn.remove()
} else {
    logout.remove()
}


logout.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = '/Users/vbobrov/PycharmProjects/pallada/pandela/frontend/login.html'
})


let coursesUrl = 'http://127.0.0.1:8000/api/courses/'

let getCourses = () => {

    fetch(coursesUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildStories(data)
        })
}


let buildCourses = (courses) => {
    let coursesWrapper = document.getElementById('courses--wrapper')

    for (let i =0; courses.length > i; i++){
        let course = courses[i]

        let courseCard = `
            <div class="course--card">
                <div>
                    <div class="card--header">
                        <h3>${course.title}</h3>
                        /*<img src="img/like.svg" class="card--img like--option" data-story="${story.id}"/>*/
                        /*раньше тут были лайки, но в курсах нет лайков. только будут оценки и наберное просмотры. вобщем их нужно будет добавить для идеального апи*/
                    </div>
                    <p>${course.description.substring(0, 150)}</p>
                </div>
            </div>
        `
        coursesWrapper.innerHTML += courseCard
    }

    /*addLikeEvents()*/
}

//let addLikeEvents () => {
//    let likeBtns = document.getElementsByClassName('like--option')
//
//    for (let i =0; likeBtns.length > i; i++){
//        voteBtns[i].addEventListener('click', (e) => {
//            let vote = e.target.dataset.like
//            let story = e.target.dataset.story
//
//            fetch(`http://127.0.0.1:8000/api/stories/${story}/like/`, {
//                method: 'POST',
//                headers: {
//                'Content-Type': 'application/json',
//                Authorization: `Bearer`
//            })
//        })
//    }
//}

getStories()