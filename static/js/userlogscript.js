    function to33Page(e){
        if($("#page-33").hasClass("D-NONE") && !$("#page-16").hasClass("D-NONE")){
            anime({
                targets: '#page-16',
                // Properties 
                translateX: "-1000%",
                // Property Parameters
                duration: 1000,
                easing: 'easeInOutCubic',
                // Animation Parameters
            });  
            setTimeout(function(){
                $("#page-16").addClass("D-NONE");

                anime({
                    targets: '#page-33',
                    // Properties 
                    translateX: ["0%"],
                    // Property Parameters
                    duration: 1000,
                    easing: 'easeInOutCubic',
                    // Animation Parameters
                    // direction:'reverse'
                });
                $("#page-33").removeClass("D-NONE");

                },1300);
            }
    }

    function to16Page(e){
        if($("#page-16").hasClass("D-NONE") && !$("#page-33").hasClass("D-NONE")){
            anime({
                targets: '#page-33',
                // Properties 
                translateX: ["0%","1000%"],
                // Property Parameters
                duration: 1000,
                easing: 'easeInOutCubic',
                // Animation Parameters
            });

            setTimeout(function() {
                $("#page-33").addClass("D-NONE");
                $("#page-16").removeClass("D-NONE");
                anime({
                    targets: '#page-16',
                    // Properties 
                    translateX: "0%",
                    // Property Parameters
                    duration: 1000,
                    easing: 'easeInOutCubic',
                    // Animation Parameters
                });  
            },1300);
        }
    }

    function userto16(){
        // $("#main-section").removeClass('D-NONE');
        // $("#onlyforuser").addClass('D-NONE');
        // $("#sideNav")[0].hidden = false;
        to16Page();
    }

    function userto33(){
        // $("#main-section").removeClass('D-NONE');
        // $("#onlyforuser").addClass('D-NONE');
        // $("#sideNav")[0].hidden = false;
        to33Page();
    }

    function usertoPage(){
        window.location.href = '/userlog';
    }

    function toscorebtn(e){
        $(".Gchart1").removeClass('D-NONE');
        $(".Gchart2").addClass('D-NONE');
        $("#toscorebtn").addClass("focus");
        $("#torawbtn").removeClass("focus");
    }
    function torawbtn(e){
        $(".Gchart1").addClass('D-NONE');
        $(".Gchart2").removeClass('D-NONE');
        $("#toscorebtn").removeClass("focus");
        $("#torawbtn").addClass("focus");
    }

includeHTML( function () {
    // if (sessionStorage.key('User')){
    //     $("#Login-Section").text("환영합니다. " + sessionStorage['User']);
    // }
    // else{
    //     $("#33BTN").addClass("disabled");
    //     console.log($("#33BTN")[0].onclick=nonlogined);
    // }
    includeRouter( function () {
        // do something in the future
        });
    });