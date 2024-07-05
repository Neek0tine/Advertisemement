document.addEventListener('DOMContentLoaded', function() {
    var coderForm = document.getElementById('coderForm');
    if (coderForm) {
        var formRect = coderForm.getBoundingClientRect();
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        var clientHeight = document.documentElement.clientHeight;

        // Calculate the vertical position to scroll to
        var scrollPosition = formRect.top + scrollTop - (clientHeight / 2) + (formRect.height / 2);

        window.scrollTo({
            top: scrollPosition,
            left: 0,
            behavior: 'smooth'
        });
    }
});
