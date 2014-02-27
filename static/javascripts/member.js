// 我的快书包中用到的js
$(document).ready(function() {
	// 密码修改
	if($('#my_info_password_form').size() == 1) {
		$('#my_info_password_form').submit(function() {
			var password = $('#password').val(),new_password = $('#new_password').val(),re_password = $('#re_password').val();
			if(password == '' || password == null) {
				m_ksb_msg.show('旧密码不能为空');
				return false;
			}
			if(new_password == '' || new_password == null) {
				m_ksb_msg.show('新密码不能为空');
				return false;
			}
			if(re_password != new_password) {
				m_ksb_msg.show('密码修改 新密码两次输入不一致');
				return false;
			}
			
			$.ajax({
				type	: 'post',
				url		: $(this).attr('action'),
				data	: {
					password		: password,
					new_password	: new_password,
					re_password		: re_password
				},
				success	: function(html) {
					if(0 == html.errno) {
						m_ksb_msg.show('修改成功');
						self.location.href = '/my_info_password';
					}
					else {
						m_ksb_msg.show(html.msg);
					}
				},
				error	: function(html) {}
			});
			
			return false;
		});
		$('.m-login button').click(function() {
			$('#my_info_password_form').submit();
			return false;
		});
	}
	
	// 我的收藏 删除
	if($('#my_order_fav_list').size() == 1) {
		// 如果页码大于总真实页数
		if(get_page > totalpage) {
			self.location.href = self.location.href.replace('page=' + get_page, 'page=' + totalpage);
			return;
		}
		
		$('button[goods_id]').click(function() {
			
			fav_del_do($(this).attr('goods_id'));
			
			return false;
		});
	}
	
	// 收货地址添加
	if($('#my_account_address_add_form').size() == 1) {
		$('#my_account_address_add_form #mobile').blur(function() {
			if($('#my_account_address_add_form #user_mobile').val() == '') {
				$('#my_account_address_add_form #user_mobile').val($(this).val());
			}
		});
		
		// var init_city = (typeof(order_id) == 'undefined' || order_id == '' || order_id == 0) ? 0 : (typeof(shop_city) == 'undefined' ? 0 : shop_city);
		// var ao = new address_obj();
		// if(is_exp == '1') {
		// 	$('#a').show();
		// 	ao.select_init_3('a', 'b', 'city_id', init_city);
		// }
		// else {
		// 	$('#a').hide();
		// 	ao.select_init('b', 'city_id', init_city);
		// }
		
		$('#my_account_address_add_form').submit(function() {
			var receiver	= $('#receiver').val();
			var address		= $('#address').val();
			var city_id		= $('#zone').val();
			var mobile		= $('#mobile').val();
			// var user_mobile		= $('#user_mobile').val();
			// var email		= $('#email').val();
			var is_exp		= $('#is_exp').val();
			
			if(receiver == '' || receiver == null) {
				m_ksb_msg.show('收货人姓名不能为空', $('.m-login button').offset().top - 100);
				return false;
			}
			if(city_id == '' || city_id == null) {
				m_ksb_msg.show('请选择城区', $('.m-login button').offset().top - 100);
				return false;
			}
			if(address == '' || address == null) {
				m_ksb_msg.show('详细地址不能为空', $('.m-login button').offset().top - 100);
				return false;
			}
			if(mobile == '' || mobile == null) {
				m_ksb_msg.show('收货人手机号不能为空', $('.m-login button').offset().top - 100);
				return false;
			}
			// if(user_mobile == '' || user_mobile == null) {
			// 	m_ksb_msg.show('下单人手机号不能为空', $('.m-login button').offset().top - 100);
			// 	return false;
			// }
//			if(email == '' || email == null) {
//				m_ksb_msg.show('邮箱不能为空', '#email');
//				return false;
//			}
			
			$.ajax({
				url		: $(this).attr('action'),
				type	: 'post',
				data	: {
					receiver	: receiver,
					address		: address,
					city_id		: city_id,
					mobile		: mobile,
					// user_mobile		: user_mobile,
					// email		: email,
					// is_exp		: is_exp,
					state		: 0
				},
				success	: function(html) {
					if(0 == html.errno) {
						m_ksb_msg.show('添加成功');
						var to_url = '/my_account_address';
						if(typeof(order_id) != 'undefined' && order_id != '' && order_id != 0 && order_id != null) {
							to_url += '?order_id=' + order_id + '&a_id=' + html.msg;
						}
						
						self.location.href = to_url;
					}
					else {
						m_ksb_msg.show(html.msg, $('.m-login button').offset().top - 100);
					}
				},
				error	: function(html) {
					
				}
			});
			
			return false;
		});
		
		$('.m-login button').click(function() {
			$('#my_account_address_add_form').submit();
			return false;
		});
	}
	
	// 图片延迟加载
	$("img[data-url]").imglazyload();
});

// 收藏删除
function fav_del_do(goods_id) {
	if(goods_id == '') {
		return false;
	}
	
	$.ajax({
		type	: 'post',
		url		: '/fav_del_p',
		data	: {
			goods_id	: goods_id
		},
		success	: function(html) {
			if(0 == html.errno) {
				m_ksb_msg.show('删除成功');
				$('#fav_' + goods_id).remove();
				
				if($('#my_order_fav_list li').size() == 0) {
					if(nowindex < totalpage) {
						self.location.reload(true);
					}
					else {
						if(nowindex > 1) {
							self.location.href = self.location.href.replace('page=' + nowindex, 'page=' + (parseInt(nowindex) - 1));
						}
					}
				}
				
			}
			else {
				m_ksb_msg.show(html.msg);
			}
		},
		error	: function(html) {}
	});
	return false;
}
