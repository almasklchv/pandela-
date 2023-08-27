export function videoPlayer() {
    let control = document.querySelector('.control');
    document.querySelector('.play').addEventListener('click', () => {
        if (control.classList.contains('play')) {
            document.querySelector('.poster').style.display = "none";
            control.classList.remove('play');
            document.querySelector('.video-player').play();
            document.querySelector('.video-player').setAttribute("controls", "controls");
        }
       
    })
    
    document.querySelector('.video-player').addEventListener('click', (event) => {
        event.preventDefault();
        if (!control.classList.contains('play') && !control.classList.contains('pause')) {
            document.querySelector('.control').classList.add('pause');
            document.querySelector('.video-player').pause();
            document.querySelector('.video-player').removeAttribute("controls");
        } else if (!control.classList.contains('play')) {
            document.querySelector('.control').classList.remove('pause');
            document.querySelector('.video-player').setAttribute("controls", "controls");
            document.querySelector('.video-player').play();
            
        }
    
        if (control.classList.contains('pause')) {
            document.querySelector('.pause').addEventListener('click', () => {
                document.querySelector('.control').classList.remove('pause');
                document.querySelector('.video-player').play();
                document.querySelector('.video-player').setAttribute("controls", "controls");
            })
        }
        
    })
    
    document.querySelector('.video-player').addEventListener('pause', () => {
        document.querySelector('.control').classList.add('pause');
        document.querySelector('.video-player').removeAttribute("controls");
    })
}
