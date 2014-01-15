$(document).ready(function() {
	if($('#upload_ul').size() == 1) {
		$('#upload_form_submit_btn').click(function() {
			upload_form_do();
		});
	}
});

// 表单提交
function upload_form_do() {
	var catalog = $('#catalog').val(), name = $('#name').val(), subname = $('#subname').val(), price = $('#price').val(), discount = $('#discount').val();
    // var pic = $('#pic').files[0];
    var form = new FormData();

    form.append("catalog", catalog);
    form.append("name", name);
    form.append("subname", subname);
    form.append("price", price);
    form.append("discount", discount);
    // form.append("pic", pic);

	var msg_top = $('#upload_form_submit_btn').offset().top - 80;

	// 参数检测
	// if(login_name == '' || login_name == null) {
	// 	m_ksb_msg.show('登录账号不能为空', msg_top);
	// 	return false;
	// }
	// var myreg = /^0?(13[0-9]|15[012356789]|18[0-9]|14[57])[0-9]{8}$/
	// if(!myreg.test(phone)) {
	// 	m_ksb_msg.show('请输入正确的手机号码', msg_top);
	// 	return false;
	// }
	$.ajax({
		type	: 'post',
		url		: '/admin',
		data	: form,

		success	: function(html) {
			m_ksb_msg.show(html.msg);
			// if(0 == html.errno) {
			// 	top.location = '/mine';
			// }
			// else {
			// 	m_ksb_msg.show(html.msg);
			// }
		},
		error	: function(html) {}
	});

	return false;
}
