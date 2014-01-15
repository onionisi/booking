$(document).ready(function() {
	// 登录
	if($('#login_ul').size() == 1) {
		$('#login_form_submit_btn').click(function() {
			login_form_do();
		});
	}
});

// 登录表单提交
function login_form_do() {
	var login_name = $('#login_name').val(), password = $('#password').val(), type = $('#type').val(), autologin = 1;

	// 参数检测
	if(login_name == '' || login_name == null) {
		m_ksb_msg.show('登录账号不能为空', $('#login_name'));
		return false;
	}
	if(login_name.length < 2 || login_name.length > 20) {
		m_ksb_msg.show('登录账号不合规范', $('#login_name'));
		return false;
	}
	if(password == '' || password == null) {
		m_ksb_msg.show('密码不能为空', $('#password'));
		return false;
	}
	if(password.length < 6 || password.length > 20) {
		m_ksb_msg.show('密码不合规范', $('#password'));
		return false;
	}

	$.ajax({
		type	: 'post',
		url		: '/login',
		data	: {
			login_name	: login_name,
			password	: password,
			type		: type,
			autologin	: autologin
		},
		success	: function(html) {
			if(0 == html.errno) {
				if(typeof(referer) == 'undefined') {
					login_check();
				}
				else {
					top.location.href = referer;
				}
				m_ksb_msg.show(html.msg);
			}
			else {
				m_ksb_msg.show(html.msg);
			}
		},
		error	: function(html) {}
	});

	return false;
}
