document.querySelectorAll('button').forEach((b) => {
    b.addEventListener('click', function(e){
        fetch(`/app/like/${b.dataset.id}`)
        .then(response => response.json())
        .then(data => {
            let d = document.getElementById(`like_counter_${b.dataset.id}`)
            d.innerText = data.likes
            if(data.flag==='remove') b.innerHTML = `<i class="bi bi-hand-thumbs-up" style="font-size: 1.5rem; color: cornflowerblue;"></i>`;
            else b.innerHTML = `<i class="bi bi-hand-thumbs-up-fill" style="font-size: 1.5rem; color: cornflowerblue;"></i>`
        })
    })
})