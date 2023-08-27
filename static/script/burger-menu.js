let burgerIcon = document.querySelector('.burger-icon');
let burgerMenu = document.querySelector('.burger-menu');
let body = document.body.children;

export function onBurgerMenu() {
    burgerIcon.addEventListener('click', () => {
        
        burgerMenu.style.display = 'flex';
        if (burgerMenu.classList.contains('open')) {
            setTimeout(() => {
                burgerMenu.style.display = 'none';
                for (let i = 0; i <= body.length; i++) {
                    if (body[i] != burgerMenu) {
                        for (let j = 0; j < body[i].children.length; j++) {
                            body[i].children[j].style.opacity = '';
                            body[i].children[j].style.pointerEvents = '';
                        }
                    }
                }
            }, 400)
        }
        setTimeout(() => {
            burgerMenu.classList.toggle('open');
            for (let i = 0; i <= body.length; i++) {
                if (body[i] != burgerMenu) {
                    for (let j = 0; j < body[i].children.length; j++) {
                        body[i].children[j].style.opacity = '0.2';
                        burgerIcon.style.opacity = '';
                        body[i].children[j].style.pointerEvents = 'none';
                        burgerIcon.style.pointerEvents = '';
                    }
                }
            }
        }, 200)
    
        
    });
    
    window.addEventListener('resize', () => {
        if (document.body.clientWidth > 769) {
            burgerMenu.style.display = 'none';
            
            for (let i = 0; i <= body.length; i++) {
                if (body[i] != burgerMenu) {
                    for (let j = 0; j < body[i].children.length; j++) {
                        body[i].children[j].style.opacity = '';
                        body[i].children[j].style.pointerEvents = '';
                    }
                }
            }

            
        }
    })
    
}
