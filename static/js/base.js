document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".message");
    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.transition = "opacity 0.5s ease-out";
            message.style.opacity = "0";
            setTimeout(function () {
                message.remove();
            }, 500);
        }, 5000);
    });
});