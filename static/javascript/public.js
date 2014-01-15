$(document).ready(function() {
	// 点击跳转
	$('[url_to]').click(function() {
		self.location.href = $(this).attr('url_to');
	});

    $("button[data-url]").click(function(){
        location.href = $(this).attr("data-url");
    });

	// 退出
	$('a[name="member_logout"]').click(function() {
		$.ajax({
			type	: 'get',
			url		: $(this).attr('href'),
			success	: function(html) {
				if(0 == html.errno) {
					top.location.reload(true);
				}
				else {
					m_ksb_msg.show(html.msg);
				}
			},
			error	: function(html) {}
		});
		return false;
	});

	// 图片延迟加载
	//$("img[data-url]").imglazyload();
});


// 同时只能有一个msg弹存在 如果想弄出来多个就自己改吧
// 调用方法1
// m_ksb_msg.show(msg, top, time, width, opacity)
// @msg		string	要显示的内容	必填
// @top		number/string-可传#id .class/object-$(...)/undefined		距离顶部距离
// @ time	number/undefined	延迟关闭 单位秒 默认3秒 传0长显不关
// @width	number/undefined	背景宽度
// @opacity	bool/undefined		半透明

// 调用方法2
//m_ksb_msg.show({
//	init_msg		: 'test',	// 弹层内容
//	init_top		: 100,		// 默认距顶部距离
//	init_width		: 200,		// 默认宽度
//	init_opacity	: true,		// 默认透明度
//	init_time		: 3,		// 默认弹层关闭延迟时间
//});
var m_ksb_msg = {
	// 可外部定义变量
	init_top		: 100,		// 默认距顶部距离
	init_width		: 200,		// 默认宽度
	init_opacity	: 0.5,		// 默认透明度
	init_time		: 3,		// 默认弹层关闭延迟时间
	init_msg		: '',		// 弹层内容

	// 内部变量
	alert_id	: '',
	html		: '',
	tt			: null,

	_get_top	: function(top) {
		var t = typeof(top);
		if(t == 'number') {
			return top >= 0 ? top : m_ksb_msg._top;
		}
		if(t == 'string') {
			return (parseInt($(top).offset().top) + 30);
		}
		if(t == 'object') {
			return (parseInt(top.offset().top) + 30);
		}

		return m_ksb_msg._top;
	},

	// 初始化方法
	_init		: function(msg, top, time, width, opacity) {
		// 系统初始化
		m_ksb_msg.init_top = 100;
		m_ksb_msg.init_width = 200;
		m_ksb_msg.init_msg = '';
		m_ksb_msg.init_opacity = 0.5;
		m_ksb_msg.init_time = 3;
		m_ksb_msg.alert_id = '';
		m_ksb_msg.html = '';
		clearTimeout(m_ksb_msg.tt);
		m_ksb_msg.tt = null;

		// 关闭弹层时候的事件
		if(typeof(msg) == 'undefined') {
			return;
		}

		// 传参解析
		// 结构体解析
		if(typeof(msg) == 'object') {
			m_ksb_msg.init_msg = typeof(msg['msg']) == 'undefined' ? '' : msg['msg'];
			m_ksb_msg.init_top = typeof(msg['top']) == 'undefined' ? m_ksb_msg.init_top : m_ksb_msg._get_top(msg['top']);
			m_ksb_msg.init_time = (typeof(msg['time']) == 'number' && msg['time'] >= 0) ? parseInt(msg['time']) : m_ksb_msg.init_time;
			m_ksb_msg.init_width = typeof(msg['width']) == 'undefined' ? m_ksb_msg.init_width : parseInt(msg['width']);
			m_ksb_msg.init_opacity = ((typeof(msg['opacity']) == 'boolean' && msg['opacity'] == true) || typeof(msg['opacity']) == 'undefined') ? m_ksb_msg.init_opacity : 1;

			return;
		}
		// 直接参数
		m_ksb_msg.init_msg = typeof(msg) == 'undefined' ? '' : msg;
		m_ksb_msg.init_top = typeof(top) == 'undefined' ? m_ksb_msg.init_top : m_ksb_msg._get_top(top);
		m_ksb_msg.init_time = (typeof(time) == 'number' && time >= 0) ? parseInt(time) : m_ksb_msg.init_time;
		m_ksb_msg.init_width = typeof(width) == 'undefined' ? m_ksb_msg.init_width : parseInt(width);
		m_ksb_msg.init_opacity = ((typeof(opacity) == 'boolean' && opacity == true) || typeof(opacity) == 'undefined') ? m_ksb_msg.init_opacity : 1;
	},
	_get_id		: function() {
		if(m_ksb_msg.alert_id != '') {
			return m_ksb_msg.alert_id;
		}
		return 'm_ksb_msg_id_' + Math.ceil(Math.random() * 1000);
	},
	_setmsg		: function() {
		m_ksb_msg.alert_id = m_ksb_msg._get_id();
		m_ksb_msg.html = '<div id="' + m_ksb_msg.alert_id + '" style="width:' + $(window).width() + 'px; height:' + $(window).height() + 'px; position:absolute; left:0px; top:0px; z-index:999;">\n';
		m_ksb_msg.html += '	<div style="width:' + m_ksb_msg.init_width + 'px; height:auto; min-height:30px; line-height:30px; background:#000000; color:#FFFFFF; margin:' + m_ksb_msg.init_top + 'px auto 0px auto; text-align:center; -webkit-border-radius:2px; -moz-border-radius:2px; border-radius: 2px; font-size:12px; -moz-opacity:' + m_ksb_msg.init_opacity + '; opacity: ' + m_ksb_msg.init_opacity + ';">' + m_ksb_msg.init_msg + '</div>\n';
		m_ksb_msg.html += '</div>';
	},
	_close		: function() {
		m_ksb_msg.init_time = m_ksb_msg.init_time * 1000;
		if(m_ksb_msg.init_time == 0) {
			return;
		}
		if(m_ksb_msg.init_time > 0) {
			m_ksb_msg.tt = setTimeout('m_ksb_msg.close()', m_ksb_msg.init_time);
		}
	},
	close		: function() {
		$('#' + m_ksb_msg.alert_id).remove();
		m_ksb_msg._init();
	},
	open		: function() {
		if($('#' + m_ksb_msg.alert_id).size() > 0) {
			return;
		}
		$('body').append(m_ksb_msg.html);
	},
	show		: function(msg, top, time, width, opacity, style) {
		m_ksb_msg._init(msg, top, time, width, opacity, style);

		m_ksb_msg._setmsg();

		m_ksb_msg.open();

		$('#' + m_ksb_msg.alert_id).click(function() {
			m_ksb_msg.close();
		});
		m_ksb_msg._close();
	}
};

// 登录状态检测 前端js
function is_logined() {
    // return ($.cookie('cps') != null && $.cookie('cps') != ''
    //     && $.cookie('id') != null && $.cookie('id') != ''
    //     && $.cookie('ln') != null && $.cookie('ln') != '');
	return ($.cookie('ln') != null && $.cookie('ln') != '');
}

// 登录状态显示
function login_check() {
	if(is_logined()) {
		// todo 当前页面检测 登录状态不允许呆的一些页面 跳走

		var weibo_nick = $.cookie('wn');
		weibo_nick = (weibo_nick == '' || weibo_nick == null) ? '' : '(' + weibo_nick + ')';
		if($.cookie('ln').indexOf('(新浪微博)') >= 0) {
			weibo_nick = '';
		}

		// todo

		//alert(weibo_nick);
		$("#foot_login").hide();
        $("#foot_reg").hide();
        $("#foot_loginout").show();
        $("#foot_nickname").html($.cookie('ln') + weibo_nick).show();

//		$('.nologin').hide();
//		$('.logined').html($.cookie('ln') + weibo_nick + '，欢迎您！');
//		$('.logined').show();
//		$('.logined_show').show();
//		$('.loginout').show();
	}
}
