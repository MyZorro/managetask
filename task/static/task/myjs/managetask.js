function loginPost() {
    var url = "/task/login/"
    var data = JSON.stringify({username:$("#id_username").val(),password:$("#id_password").val()})
    $.ajax({
        url : url,
        data : data,
        type : "POST",
        contentType:"application/json",
        headers:{"X-CSRFToken":$("[name='csrfmiddlewaretoken']").val()},
        cache : false,
        async : false,
        success : function(response){
            console.log(response["status"])
            if(response["status"]!=1200){
                selfAlert("账户名或密码错误");
            }
            else{
                window.location.href = "/task/edition_manage/";
            }
        }
    });
}

function selfAlert(contents){
    layer.open({
        type: 1, //Page层类型,
        area: ['290px', '180px'],
        title: '提示',
        shade: 0.6, //遮罩透明度,
        maxmin: false, //允许全屏最小化,
        anim: 0, //0-6的动画形式，-1不开启,
        content: $("#box1").text(contents),
    });
}