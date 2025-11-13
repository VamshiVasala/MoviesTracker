document.addEventListener("DOMContentLoaded", function() {
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach((toast, i) => {
    setTimeout(() => {
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 4000);
    }, i * 300);
  });
});
