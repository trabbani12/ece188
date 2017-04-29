/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav_1() {
    document.getElementById("mySidenav_1").style.width = "250px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav_1() {
    document.getElementById("mySidenav_1").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
}
