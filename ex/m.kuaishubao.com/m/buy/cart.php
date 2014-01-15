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
<script type="text/javascript" src="../../js/float_number.js"></script>
</head>
<body>

<div class="g-doc"><div class='w'>
<header class="g-hd">
    <div class="m-hd">
        <section>
            <a href="javascript:history.go(-1);"><span class="return">返回</span></a>
        </section>
        <section>
            <h1 class="title">我的购物车</h1>
        </section>
        <section></section>
    </div>
</header>


  <div class="g-bd">
    <!-- 购物车 -->
    <div id="yescart">
    <div class='u-boxlist-w300' style="margin-top: 20px;">
      <ul>
                </ul>
    </div>
      <form id="corder" action="http://m.kuaishubao.com/buy/order.php" method="post">
          <input type="hidden" name="from" value="m">
          <input type="hidden" name="oder" value="">
    <div class='m-cart'>
        <div id="Cart-Chaozhi">
        </div>
      <div class='u-box f-mt10 price-box'>
        当前购物车内商品总金额：<i class='u-price-red' id="total">￥0</i> <br>
        包含：订单 <i class='u-price-red' id="c_total">0</i> + 特价换购 <i class='u-price-red' id="s_total">0</i>
      </div>
              <button id="corder_btn" class='u-btn-orange u-btn-fullwd u-txt-white18 f-mt10'>去结算</button>
    </div>
        </form>
    </div>
  <div id="nocart" style="display: none;">
      <div class="m-cart-empty">
          <p>购物车内暂时没有商品<br> 您可以去首页挑选喜欢的商品</p>
          <button id="nocorder_btn" class='u-btn-orange u-btn-fullwd u-txt-white18 f-mt10'>返回首页</button>
      </div>
  </div>
</div>
<div style="height: 50px;"></div>
<div class="m-btngroup f-clr">
    <a href="../member/login.php" class="u-btnbox u-btn-reg" id="foot_login">登录</a>
    <a href="../member/reg.php" class="u-btnbox u-btn-login" id="foot_reg">注册</a>
    <a href="../member/my.php" class="u-btnbox u-btn-reg" style="display: none;width: 180px;overflow: hidden;" id="foot_nickname"></a>
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
            <a href="../member/my.php"><li class="ksb">我的快书包</li></a>
            <a href="cart.php"><li class="cart">购物车<i id="cart_num">0</i></li></a>
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
</div> </div>
<script>
    try{
        var mycart = {"gcart":[],"mcart":[]};
    }catch(e){
        var mycart = {};
    }
    var time_hand = null;
    var c_total = 0;
    var s_total = 0;
    var total = 0;
    var c_mfirst = 0;

    function count_money()
    {
        //$("#Loading").hide();
        c_total = 0;
        $("li[goods]").each(function(){
            g = $(this).attr("goods");
            m = $("input[goods_id="+g+"]").val() * $(this).attr("price");
            c_total += parseInt(m);
            m = returnFloat2(m.div(100));
            //$("#g_"+g).html("￥"+m);
        });
        /*
         $("li[meals]").each(function(){
         g = $(this).attr("meals");
         m = $("#meal_num_"+g).val() * $(this).attr("price");
         c_total += parseInt(m);
         m = returnFloat2(m.div(100));
         $("#m_"+g).html("￥"+m);
         make_meal_goods_num(g);
         });
         */
        show_total();
        find_hg();
        if(!is_have_goods()){
            $("#corder_btn").hide();
            $("#yescart").hide();
            $("#nocart").show();
        } else {
            $("#corder_btn").show();
            $("#yescart").show();
            $("#nocart").hide();
        }
    }
    function is_have_goods()
    {
        for(i in mycart)
        {
            if(!$.isEmptyObject(mycart[i])){
                return true
            }
        }
        return false;
    }
    function find_hg()
    {
        if(c_total <= 0 || !is_logined())
        {
            $("#Cart-Chaozhi").html('');
            $("#Cart-Chaozhi").hide();
            return;
        }
        $url = "/buy/cart_hg.php?from=m&shop_id=bj&price="+c_total;
        $.get($url, function(data){
            //alert('ok');
            if (data != '' && data.isok == 1) {
                $("#Cart-Chaozhi").html(data.hg);
                $("#Cart-Chaozhi").show();
            } else {
                $("#Cart-Chaozhi").html('');
                $("#Cart-Chaozhi").hide();
            }
        },'json');
    }
    function add_cart(gid, num, type){
        type = typeof(type) == "undefined" ? 1 : type;

        if (type == 1){
            mycart['gcart'][gid] = num;
            if (num == 0){delete  mycart['gcart'][gid];}
        } else {
            mycart['mcart'][gid] = num;
            if (num == 0){delete  mycart['mcart'][gid];}
        }

        $url = "/buy/cart_add.php?goods_id="+gid+"&num="+num+"&type="+type+"&random="+Math.floor(Math.random() * ( 1000 + 1));
        $.get($url, function(){
            show_cartnum();
        },'json');
    }
    function show_total(){
        $("#c_total").html(returnFloat2(c_total.div(100)));
        $("#s_total").html(returnFloat2(s_total.div(100)));
        total = c_total + s_total;
        $("#total").html("￥"+returnFloat2(total.div(100)));
    }
    function chk_buynum(v, s){
        var p=new RegExp("[0-9]{1,}");
        b = p.exec(v);
        console.log((parseInt(b) < parseInt(s)));
        if (parseInt(b) < parseInt(s) || (v != '' && isNaN(parseInt(b))))
        {
            return s;
        }else{
            return b;
        }
    }
    $("input[goods_id]").focus(function(){
        $(this).attr("prevalue", $(this).val());
    });
    $("input[goods_id]").focusout(function(){
        t = this;
        v = chk_buynum($(t).val(), $(t).attr("start_unit"));
        if (b != null && $(t).val() != v){
            $(t).val(v);
        }else if(b == null){
            $(t).val($(t).attr("start_unit"));
        }
        if (v != $(t).attr("prevalue") && v != '' && !isNaN(parseInt(v)))
        {
            $(t).attr("prevalue", v);
            //有变化，ajax调用
            add_cart($(t).attr("goods_id"), $(t).val(), 1);
            count_money();
        }
    });
    function remove_goods(goods_id){
        $("li[goods="+goods_id+"]").animate({
                    "height": 0
                }, 500, "linear", function() {
                    $("li[goods="+goods_id+"]").remove();
                    add_cart(goods_id, 0, 1);
                    count_money();
                }
        );
    }

    $(document).ready(function(){
        count_money();
    });

    if ($.support.touch){
        $("button[goods_id]").click(function(){
            remove_goods($(this).attr("goods_id"));
        });
    }else{
        $("button[goods_id]").click(function(){
            remove_goods($(this).attr("goods_id"));
        });
    }
    function commit_order_b()
    {
        if (!is_have_goods()) {
            return false;
        }
        /*
         if(!is_logined()){
         return ksb_dialog.login_show(function(){count_money();});
         }
         */
        $("input[name=oder]").val(JSON.stringify(mycart));
        //alert($("input[name=oder]").val());
        $("#corder").submit();
        return false;
    }

    $("#corder_btn").click(function(){
        commit_order_b();
    })
    $("#nocorder_btn").click(function(){
        location.href = "/bj"
    })
</script>
</body>
</html>