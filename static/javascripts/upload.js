$(document).ready(function() {
    if($('#upload_ul').size() == 1) {
        $('#upload_form_submit_btn').click(function() {
            upload_form_do();
        });
    }
});

// 表单提交
function upload_form_do() {
    var catalog = $('#catalog').val(), name = $('#name').val(), subname = $('#subname').val();
    var price = $('#price').val(), discount = $('#discount').val();
    var pic = document.getElementById("pic").files[0]; // 获取文件对象

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
    // if(pic == '' || pic == null) {
    //     m_ksb_msg.show('图片不能为空', msg_top);
    //     return false;
    // }

    var form = new FormData();
    form.append("catalog", catalog);
    form.append("name", name);
    form.append("subname", subname);
    form.append("price", price);
    form.append("discount", discount);
    form.append("pic", pic);

    var xhr = new XMLHttpRequest();
    xhr.open("post", "/admin", true);
    xhr.onload = function ()
    {
        m_ksb_msg.show('上传成功，请继续', msg_top);
    };
    xhr.send(form);
	// $.ajax({
	// 	type	: 'post',
	// 	url		: '/admin',
	// 	data	: form,
	// 	success	: function(html) {
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

    // iframe style too
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

function validate_edit_logo(a){
    var file = $('file').value;
    if(!/.(gif|jpg|jpeg|png|gif|jpg|png)$/.test(file)){
        alert("图片类型必须是.gif,jpeg,jpg,png中的一种")
            if(a==1){
                return false;
            }
    }else{
        var image = new image();
        image.src = file;
        var height = image.height;
        var width = image.width;
        var filesize = image.filesize;
        $('beforeend').src=file;
        $('div_regi_right').setstyle('display', 'block');
        if(width>80 && height>80 && filesize>102400){
            alert('请上传80*80像素 或者大小小于100k的图片');
            if(a==1){
                return false;
            }
        }
        if(a==1){
            return true;
        }
    }
}
