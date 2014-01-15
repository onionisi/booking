<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>快书包触屏版</title>
<meta name="keywords" content=""/>
<meta name="description" content=""/>
<meta name="viewport" content="initial-scale=1.0,user-scalable=no,maximum-scale=1,width=device-width" />
<meta content="initial-scale=1.0,user-scalable=no,maximum-scale=1" media="(device-height: 568px)" name="viewport">
<meta content="yes" name="apple-mobile-web-app-capable">
<meta content="black" name="apple-mobile-web-app-status-bar-style">
<meta content="telephone=no" name="format-detection">

<link rel="shortcut icon" href="../../favicon.ico"/>
<link rel="apple-touch-icon" href="../../img/m/touchicon.png"/>
<link rel="apple-touch-icon-precomposed" href="../../img/m/touchicon.png"/>
<link rel="stylesheet" href="../../css/m/main-min.css"/>
<link rel="stylesheet" type="text/css" href="../../css/m/gmu-min.css" />

<script type="text/javascript" src="../../js/m/zepto-min.js"></script>
<script language="javascript" src="../../js/m/m.zepto.cookie.js"></script>
<script language="javascript" src="../../js/m/public.js?t=2"></script>
<script type="text/javascript" src="../../js/m/gmu-min.js"></script>
<!--
<script type="text/javascript" src="/js/m/main-min.js"></script>
-->
<script language="javascript" src="../../js/m/member/login.js?v=1"></script>
<script language="javascript">
var referer = 'http://m.kuaishubao.com/m/member/my.php';
</script>
</head>
<body>

<div class="g-doc">
	<div class='w'>
		<header class="g-hd">
    <div class="m-hd">
        <section>
            <a href="javascript:history.go(-1);"><span class="return">返回</span></a>
        </section>
        <section>
            <h1 class="title">登录快书包</h1>
        </section>
        <section></section>
    </div>
</header>

		
		<div class='u-box m-ipt-group2'>
			<input type="hidden" name="type" id="type" value="">
			<ul id="login_ul">
				<li class='first'>
					<input type="text" placeholder='登录账号' name="login_name" id="login_name" value="">
				</li>
				<li>
					<input type="password" placeholder='密码' name="password" id="password" value="">
				</li>
			</ul>
		</div>
		<div class='m-login'>
			<button class='u-btn-blue u-btn-fullwd u-txt-white18' id="login_form_submit_btn">登录</button>
			<div class='f-mt20 login-weibo'>
				<p class='f-lh2em'>使用合作网站账号登录快书包：</p>
				<button class='u-btn-red u-btn-fullwd u-txt-white18' url_to="/member/other_login.php?from=1&client=1&src=http%3A%2F%2Fm.kuaishubao.com%2Fm%2Fmember%2Fmy.php">用微博账号登录</button>
			</div>
			
			<div class='reg-div'>
				<div>还不是会员？<button class='u-btnbox40' url_to="/m/member/reg.php?src=http%3A%2F%2Fm.kuaishubao.com%2Fm%2Fmember%2Fmy.php">立即注册</button></div>
			</div>
			
		</div>
		
		<div style="height: 50px;"></div>
<div class="m-btngroup f-clr">
    <a href="login.php" class="u-btnbox u-btn-reg" id="foot_login">登录</a>
    <a href="reg.php" class="u-btnbox u-btn-login" id="foot_reg">注册</a>
    <a href="my.php" class="u-btnbox u-btn-reg" style="display: none;width: 180px;overflow: hidden;" id="foot_nickname"></a>
    <a href="../../member/logout_p.php" name="member_logout" class="u-btnbox u-btn-login" style="display: none;" id="foot_loginout">退出</a>
    
</div>
        <script>
            login_check();
        </script>
<div class="g-ft">
    <div class="u-box m-ft">
        <div>
            <a href="../../bj" class="help">返回首页</a>
            <a href="http://www.kuaishubao.com/index.php?from_m=m" class="about">切换PC版</a>
        </div>
        
    </div>
</div>

<div class="m-toolbar" id="fixbtn_all" style="width: 320px; position: fixed;bottom: 0px;z-index: 1000;">
    <div class="fixbtn" id="fixbtn"></div>
    <div style="height:0px;overflow: hidden;" id="fixbtn_div">
        <ul class="f-clr off0" id="fixbtn_ul">
            <a href="../../bj"><li class="home">首页</li></a>
            <a href="my.php"><li class="ksb">我的快书包</li></a>
            <a href="../buy/cart.php"><li class="cart">购物车<i id="cart_num">0</i></li></a>
            <a href="../class.php"><li class="cls">商品分类</li></a>
        </ul>
    </div>
</div>


<script>
    fix_state = false
    function fixbtn_show(now){
        //alert(fix_state)
        if ( fix_state){
            hi = 0;
        }else{
            hi = $("#fixbtn_ul").height();
        }
        t = 300;
        $("#fixbtn_div").animate({
            "height": hi
        }, t, "linear", function() {
            if ( fix_state){
                fix_state = false;
            }else{
                fix_state = true;
            }
        });
    }
    $("#fixbtn").click(function(){fixbtn_show();});

    function show_cartnum(){
        b = ($.cookie('cartn') == null || $.cookie('cartn') == '') ? 0 : $.cookie('cartn');
        var p=new RegExp("[0-9]{1,}");
        b = parseInt(p.exec(b));

        $("#cart_num").toggle(b > 0);
        if (b > 0){
            $("#cart_num").show()
        }else{
            $("#cart_num").hide()
        }
        if (b > 9) {
            $("#cart_num").html('N');
        } else {
            $("#cart_num").html(b);
        }
    }
    $(document).ready(function(){
        show_cartnum();
    })
</script>

<!-- Piwik -->
<script type="text/javascript">
    var _paq = _paq || [];
    _paq.push(["trackPageView"]);
    _paq.push(["enableLinkTracking"]);

    (function() {
        var u=(("https:" == document.location.protocol) ? "https" : "http") + "://piwik.internal.kuaishubao.com/";
        _paq.push(["setTrackerUrl", u+"piwik.php"]);
        _paq.push(["setSiteId", "10"]);
        var d=document, g=d.createElement("script"), s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
        g.defer=true; g.async=true; g.src=u+"piwik.js"; s.parentNode.insertBefore(g,s);
    })();
</script>
<!-- End Piwik Code -->
	</div>
</div>
</body>
</html>