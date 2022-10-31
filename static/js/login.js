window.addEventListener('DOMContentLoaded', function () {
    // set();

})

function set() {
    setTimeout(() => {
        console.log(isRun);
        set();
    }, 1000);

}

let isRun = false;

function errorMessage(text) {
    if (isRun == false) {
        document.getElementById("login_error").innerText =
            text;
        isRun = true;
        setTimeout(() => {
            document.getElementById("login_error").innerText = "";
            isRun = false;
        }, 2000);
    }

}

function Login() {
    if (isRun == true) return
    let username = $("#username").val();
    let password = $("#password").val();

    $.ajax({
        type: "POST",
        url: "/user/login",
        data: {user_id: username, user_pwd: password},
        success: function (res) {
            console.log(res);
            if (res.result == "FAIL") {
                errorMessage('아이디나 비밀번호를 다시 한번 더 확인해주세요.')
            } else {
                alert("로그인이 되었습니다.");

                window.location.href = "/";
            }
        },
    });
}

