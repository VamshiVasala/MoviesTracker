document.addEventListener("DOMContentLoaded", () => {
    const watchStatus = document.querySelectorAll('.movie-card');
    const buttonWatch = document.querySelectorAll('.btn-watch');
    watchStatus.forEach(btn => {
        btn.addEventListener("mouseover", () => {
            buttonWatch.forEach(buttonWatch => {
                if (btn.contains(buttonWatch)) {
                    buttonWatch.style.display = 'flex';
                }
            }); 
        });
    });
    watchStatus.forEach(btn => {
        btn.addEventListener("mouseout", () => {
            buttonWatch.forEach(buttonWatch => {
                if (btn.contains(buttonWatch)) {
                    buttonWatch.style.display = 'none';
                }
            }); 
        });
    });
});
