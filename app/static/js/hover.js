document.querySelectorAll('a').forEach(link => {
    let old_color = link.style.color;
    link.onmouseover = () => {
      link.style.color = "#ffc107";
    }
    link.onmouseout = () => {
      link.style.color = old_color;
    }
  })