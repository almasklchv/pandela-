export function openOrCloseMenu() {
    const dropdownMenuContent = document.querySelector(".dropdown-menu__content");
    
    dropdownMenuContent.classList.toggle("active");
    dropdownMenuContent.classList.toggle("hidden");

    const dropdownMenuIcon = document.querySelector(".dropdown-menu__icon");
    dropdownMenuIcon.classList.toggle("close");

}

export function toggleMenu() {
    var icon = document.querySelector(".burger-icon");
    icon.classList.toggle("open");
}