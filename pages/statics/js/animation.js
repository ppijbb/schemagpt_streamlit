const FloatPosition = parseInt($(".sideBanner").css('top'),10);

$(window).scroll(function() {
    // 현재 스크롤 위치
    var floatPosition = FloatPosition;
    var currentTop = $(window).scrollTop();
    var bannerTop = currentTop + floatPosition;
    //이동 애니메이션
    $(".sideBanner").stop().animate({
      "top" : bannerTop
    }, 500);
}).scroll();

$("#nav1").click(function(){
    var position = $("#page-33").offset();
    console.log("gen position:",position.top)
    $("html, body").stop().animate({
        scrollTop:position.top-10
    }, 500);
});

$("#nav2").click(function(){
    var position = $("#blo").offset();
    console.log("blo position:",position.top)
    $("html, body").stop().animate({
        scrollTop:position.top-70
    }, 500);
});

$("#nav3").click(function(){
    var position = $("#nut").offset();
    console.log("nut position:",position.top)
    $("html, body").stop().animate({
        scrollTop:position.top-70
    }, 500);
});

$("#nav4").click(function(){
    var position = $("#pat").offset();
    console.log("pat position:",position.top)
    $("html, body").stop().animate({
        scrollTop:position.top-70
    }, 500);
});

$("#nav5").click(function(){
    var position = $("#end").offset();
    console.log(position.top)
    $("html").stop().animate({
        scrollTop:position.top-10
    }, 500);
});


