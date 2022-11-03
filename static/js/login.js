document.write("<script src='./specificjs.js'></script>");
function login() {
    let data = {
        "email": $('#userEmail').val(),
        "password": $('#password').val()
    }
    $.ajax({
        type: "POST",
        url: "/login",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (response) {
            alert(response['msg']);
            window.location.href="/mainpage";
        }
    });
}

function logout() {
    $.ajax({
        type: "GET",
        url: "/logout",
        data: {},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    })
}

function protect(page) {
    $.ajax({
        type: "GET",
        url: "/protected",
        data: {},
        success: function (response) {
            console.log(response);
            if (response['result'] === 'success') {
                save_video();
            } else {
                alert("로그인하세요!");
                window.location.href='/login';
            }
        }
    });
}