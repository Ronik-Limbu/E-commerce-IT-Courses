
  function showContent(section) {
    document.querySelectorAll('.tab').forEach(tab => {
      tab.classList.remove('active');
    });
    document.querySelectorAll('.content').forEach(content => {
      content.classList.remove('active');
    });
    document.querySelector(`.tab[onclick*="showContent('${section}')"]`).classList.add('active');
    document.getElementById(section).classList.add('active');
  }
