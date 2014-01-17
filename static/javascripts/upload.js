$(document).ready(function() {
    if($('#upload_ul').size() == 1) {
        $('#upload_form_submit_btn').click(function() {
            upload_form_do();
            // UploadFile();
        });
    }
});

function UploadFile() {

    var fileObj = document.getElementById("pic").files[0]; // 获取文件对象
    var FileController = "/admin";                    // 接收上传文件的后台地址

    // FormData 对象
    var form = new FormData();
    form.append("author", "hooyes");
    // 可以增加表单数据
    form.append("pic", fileObj);
    // 文件对象

    // XMLHttpRequest 对象
    var xhr = new XMLHttpRequest();
    xhr.open("post", FileController, true);
    xhr.onload = function ()
    {
        alert("上传完成!");
    };
    xhr.send(form);
}

// 表单提交
function upload_form_do() {
    var catalog = $('#catalog').val(), name = $('#name').val(), subname = $('#subname').val();
    var price = $('#price').val(), discount = $('#discount').val();
    var pic = document.getElementById("pic").files[0]; // 获取文件对象

    var MAXSIZE = 4 * 1024 * 1024;
    var msg_top = $('#upload_form_submit_btn').offset().top - 80;

    // 参数检测
    if(catalog == '' || catalog == null) {
        m_ksb_msg.show('类型不能为空', msg_top);
        return false;
    }
    if(name == '' || name == null) {
        m_ksb_msg.show('名称不能为空', msg_top);
        return false;
    }
    if(price == '' || price == null) {
        m_ksb_msg.show('价格不能为空', msg_top);
        return false;
    }
    if(pic == '' || pic == null) {
        m_ksb_msg.show('图片不能为空', msg_top);
        return false;
    }

    var form = new FormData();
    form.append("catalog", catalog);
    form.append("name", name);
    form.append("subname", subname);
    form.append("price", price);
    form.append("discount", discount);
    form.append("pic", pic);

    var xhr = new XMLHttpRequest();
    xhr.open("post", "/admin", true);
    xhr.onload = function (html)
    {
        m_ksb_msg.show(html.msg);
    };
    xhr.send(form);
	// $.ajax({
	// 	type	: 'post',
	// 	url		: '/admin',
	// 	data	: form,
	// 	success	: function(html) {
			// m_ksb_msg.show(html.msg);
			// if(0 == html.errno) {
			// 	if(typeof(referer) == 'undefined') {
			// 		login_check();
			// 	}
			// 	else {
			// 		top.location.href = referer;
			// 	}
			// 	m_ksb_msg.show(html.msg);
			// }
			// else {
			// 	m_ksb_msg.show(html.msg);
			// }
		// },
		// error	: function(html) {}
	// });

    // $('#editform').submit();
    // function callback(res){
    //     alert(res);
    // }
    // var frm = $("#frm");
    // frm.load(function(){
    //     var wnd = this.contents;
    //     var str = $(wnd.document.body).html();
    //     callback(str);
    // });
    return false;
}
