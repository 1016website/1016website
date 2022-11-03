document.write("<script src='./login.js'></script>");
$(document).ready(function () {
    show_video();
});

function show_video() {
        $.ajax({
        type: "GET",
        url: "/show",
        data: {},
        success: function (response) {
            let rows = response['videos']
            for (let i = 0; i < rows.length; i++) {
                let image = rows[i]['image']
                let comment = rows[i]['comment']
                let star = rows[i]['star']
                let desc = rows[i]['desc']
                let title = rows[i]['title']
                let url = rows[i]['url']
                let language = rows[i]['language']

                let shortTitle = title.substring(0, title.length - 10);
                let star_image = '⭐'.repeat(star)

                if(window.location.pathname==language) {
                        let temp_html = `<div class="col">
                                                <div class="card">
                                                  <img onclick="location.href='${url}'" src="${image}" class="card-img-top" alt="...">
                                                  <div class="card-body">
                                                    <h5 class="card-title">${shortTitle}</h5>
                                                    <p class="card-text">${desc}</p>
                                                    <p>추천도 : <span id = star_image>${star_image}</span> </p>
                                                    <p class="youtubecomment">${comment}</p>
                                                  </div>
                                                </div>
                                              </div>`
                    $('#cards').append(temp_html)
                }
            }
        }
    });
}

function save_video() {
    let language = window.location.pathname;

    let url = $('#url').val()
    let star = $('#star').val()
    let comment = $('#comment').val()

    $.ajax({
        type: "POST",
        url: "/save",
        data: {url_give: url, star_give: star, comment_give: comment, language_give: language, language_give : language},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

function open_box() {
    $('#post-box').show()
}

function close_box() {
    $('#post-box').hide()
}