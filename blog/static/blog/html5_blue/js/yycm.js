$(document).ready(function(){
    $(".nav ul li:has(ul)").hover(function(){
        $(this).children("a").css({color:"#fff"});
        0<$(this).find("li").length&&$(this).children("ul").stop(!0,!0).slideDown(100)},function(){$(this).children("a").css({color:"#FFF"});
        $(this).children("ul").stop(!0,!0).slideUp("fast")});
        $(".toggle-search").click(function(){$(".toggle-search").toggleClass("active");
        $(".search-expand").fadeToggle(300)});
        $(".navbar-toggle").click(function(){$(".navbar-toggle").toggleClass("active");
        $(".navbar-collapse").toggle(300);
        $(".nav ul li ul").show()});
        $(".viewimg a").hover(function(){$(this).find(".shine").stop();
        $(this).find(".shine").css("background-position","-160px 0");
        $(this).find(".shine").animate({backgroundPosition:"160px"},500)},function(){});
        $(".totop").hide();
        $(window).scroll(function(){
            0<$(window).scrollTop()?$(".totop").fadeIn(200):$(".totop").fadeOut(200)});
            $(".totop").click(function(){$("html,body").animate({scrollTop:"0px"},400)
            });
});

// 评论分页
$body=(window.opera)?(document.compatMode=="CSS1Compat"?$('html'):$('body')):$('html,body');
$('.page_navi a').live('click', function(e){
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: $(this).attr('href'),
        beforeSend: function(){
            $('.page_navi').remove();
            $('.comments-container').remove();
            $('#loading-comments').slideDown(500);
        },
        dataType: "html",
        success: function(out){
            result = $(out).find('.comments-container');
            nextlink = $(out).find('.page_navi');
            $('#loading-comments').slideUp('fast');
            $('#loading-comments').after(result.fadeIn(500));
            $('.comments-container').after(nextlink);
        }
    });
});

$(function(){$("#slider").responsiveSlides({
	auto:true,
	pager:false,
	nav:true,
	speed:500,
	pauseControls:true,
	pager:true,
	manualControls:"auto",
	namespace:"slide"
	})});
