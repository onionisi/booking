$(document).ready(function() {
	// 注册
	if($('#reg_ul').size() == 1) {
		$('#reg_form_submit_btn').click(function() {
			reg_form_do();
		});
	}
});

// 注册表单提交
function reg_form_do() {
	var login_name = $('#login_name').val(), password = $('#password').val(), repassword = $('#repassword').val();
	// var phone = $('#phone').val();

	var msg_top = $('#reg_form_submit_btn').offset().top - 80;

	// 参数检测
	if(login_name == '' || login_name == null) {
		m_ksb_msg.show('登录账号不能为空', msg_top);
		return false;
	}
	if(login_name.length < 2) {
		m_ksb_msg.show('您输入的登录账号长度不够，请保持至少4个字符', msg_top);
		return false;
	}
	if(login_name.length > 20) {
		m_ksb_msg.show('您输入的登录账号太长了，请保持在20个字符以内', msg_top);
		return false;
	}
	// 用户名存在检测
	var s = {
		errno	: 1,
		msg		: 'error',
	};
	$.ajax({
		type	: 'post',
		url		: '/register',
		async	: false,
		data	: {
			login_name	: login_name
		},
		success	: function(html) {
			s = html;
		}
	});
	if(s.errno != 0) {
		m_ksb_msg.show(s.msg, msg_top);
		return false;
	}
	if(password == '' || password == null) {
		m_ksb_msg.show('密码不能为空', msg_top);
		return false;
	}
	if(password.length < 6) {
		m_ksb_msg.show('密码长度请保持在6个字符以上', msg_top);
		return false;
	}
	if(password.length > 20) {
		m_ksb_msg.show('密码密码长度不要超过20个字符，否则容易忘记', msg_top);
		return false;
	}
	if(repassword != password) {
		m_ksb_msg.show('两次密码输入不一致', msg_top);
		return false;
	}
	// if(phone == '' || phone == null) {
	// 	m_ksb_msg.show('手机号码不能为空', msg_top);
	// 	return false;
	// }
	// if(phone.length > 100) {
	// 	m_ksb_msg.show('邮件输入太长了', msg_top);
	// 	return false;
	// }
	// var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
	// if(!myreg.test(email)) {
	// var myreg = /^0?(13[0-9]|15[012356789]|18[0-9]|14[57])[0-9]{8}$/
	// if(!myreg.test(phone)) {
	// 	m_ksb_msg.show('请输入正确的手机号码', msg_top);
	// 	return false;
	// }
	$.ajax({
		type	: 'post',
		url		: '/register',
		data	: {
			login_name	: login_name,
			password	: password,
			// phone		: phone
		},
		success	: function(html) {
			if(0 == html.errno) {
				top.location = '/mine';
			}
			else {
				m_ksb_msg.show(html.msg);
			}
		},
		error	: function(html) {}
	});

	return false;
}
