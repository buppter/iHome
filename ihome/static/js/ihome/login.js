function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

            //调用ajax向后端发送登陆请求
        var data = {
            mobile: mobile,
            password: passwd,
        };
        var login_json = JSON.stringify(data);
        $.ajax({
            url: "/api/v1.0/sessions",
            type: "post",
            data: login_json,
            contentType: "application/json",
            headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },//请求头，将csrf_token值放入请求中，方便后端进行CSRF验证

            success: function (resp) {
                if (resp.errno == "0"){
                    //登陆成功，跳转到主页
                    location.href = "/index.html"
                }else{
                    alert(resp.errmsg);
                }

            }
        })
    });
})