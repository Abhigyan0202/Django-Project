
document.addEventListener("DOMContentLoaded", function () {
    // Check user preference from localStorage
    const theme = localStorage.getItem("theme") || "light";
    setTheme(theme);

    // Toggle function
    document.getElementById("theme-toggle").addEventListener("change", function () {
        let newTheme = this.checked ? "dark" : "light";
        setTheme(newTheme);
    });

    function setTheme(theme) {
        if (theme === "dark") {
            document.documentElement.setAttribute("data-bs-theme", "dark");
            document.getElementById("theme-toggle").checked = true;
        } else {
            document.documentElement.setAttribute("data-bs-theme", "light");
            document.getElementById("theme-toggle").checked = false;
        }
        localStorage.setItem("theme", theme);
    }
});