//$('.D-NONE').find('*').attr('disabled', true);
//$('td').find('input[type="text"]').attr('value', 1);


    const test_values=[
                 //     ['테스트 데이터1',
                 //     1,2,4,116,79,132,0.83,
                 //     60.8,110.3,115,43.8,191,15.4,4.94,4.8,7.47,
                 //     4.76,20.27,20.854,0.0572,0.732655,17.13,1079.4415,26.255,87.0575,
                 //     1.0,1.0,1.0,0.0,4.0,1.0,0.0,0.0],
                        ['테스트 데이터1',
                        1,2,4,115,79,120,0.9,
                        76.5,134.9,147.0,39.2,24.0,13.4,4.31,7.0,5.25, 
                        15.50433,24.60925,7.67180,0.10010,3.39983,75.03800,1136.35250,114.83500,105.34995,  
                        1.0,1.0,1.0,0.0,1.0,1.0,0.0,0.0],
                        ['테스트 데이터2',
                        2, 1, 4, 108.00, 72.00, 116.00, 0.760000,
                        74.60, 127.40, 120.00, 38.20,  215.00,  12.40, 4.06, 4.40,  4.57,
                        16.302070, 21.769050, 19.861750, 0.600900, 1.047080, 14.363000, 489.085500, 133.289000, 63.254997,
                        0, 0, 1, 0, 1, 0, 0, 0],
                        ['테스트 데이터3',
                        1, 1, 4, 122.00, 70.00, 118.00,  0.850000,
                        46.60, 147.80, 155.00, 44.80,  231.00,  15.80, 4.82, 4.70,  4.85,
                        16.030000, 19.844000, 18.050500, 0.085800, 1.555050, 33.640003, 687.535000, 128.400010, 83.894000,
                        0, 0, 1, 0, 1, 0, 0, 0],
                        ['테스트 데이터4',
                        1, 1, 4, 116.00, 75.00, 107.00,  0.840000,
                        64.70, 76.20, 70.00, 38.10,  149.00, 12.80, 4.19, 4.00, 4.45,
                        7.022000, 7.987100, 6.680100, 0.028600, 0.591825, 6.840000, 426.235020, 11.580000, 29.523998,
                        1, 1, 1, 1, 1, 0, 0, 0]      
                    ]
    const index = [    // 참고용
                    [  // General
                        1,  2,  6, 12,
                        13, 14, 24
                    ],
                    [  // Blood
                        16, 17, 18, 19, 20,
                        23, 26, 27, 33
                    ],
                    [  // Nutrition
                        15, 21, 22, 25, 28,
                        29, 30, 31, 32
                    ],
                    [  // Pattern
                        3, 4,  5,  7,
                        8, 9, 10, 11
                    ]
                ]

    function CheckValue(e){
        let form_values = e.parentElement.parentElement;
        let count = -1;
        for(var i in form_values){
            if (form_values[i] != null&& !form_values[i].disabled && form_values[i].type =='text'){ 
                count ++;
                if ( !form_values[i].value ){
                    if(i == 0){
                        toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
                        toastr.warning(`사용자 이름이 입력되지 않았습니다.`,'빈칸이 있습니다');
                        $("html, body").stop().animate({
                            scrollTop: form_values[i].getBoundingClientRect().top
                        }, 500);
                        return;
                    }
                    else{
                        toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
                        toastr.warning(`${count} 번 째 질문이 입력되지 않았습니다.`,'빈칸이 있습니다'); 
                        $("html, body").stop().animate({
                            scrollTop: form_values[i].getBoundingClientRect().top
                        }, 500);
                        return;
                    }
                }
            }
        }
        $(".pre-loader").removeClass("D-NONE");
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
    
        gtag('config', 'UA-119386393-1');
        var width = 100,
           perfData = window.performance.timing, // The PerformanceTiming interface represents timing-related performance information for the given page.
           EstimatedTime = -(perfData.loadEventEnd - perfData.navigationStart),
           time = parseInt((EstimatedTime/1000)%60)*100;

        form_values.submit();
    }

    function onSelect(e){
        let form_values = document.forms['33Form']
        var n=0;
        for(var i in form_values){
            if(form_values[i])
                if(form_values[i].type == 'submit')
                    return;
                else if(!form_values[i].disabled && form_values[i].type=='text'){
                    if(i==0 && sessionStorage['User']) console.log(form_values[i].value) ; 
                    else form_values[i].value=test_values[e.value][n];
                    if(form_values[i].parentElement.parentElement.children[0].children[0].type == 'range')
                        form_values[i].parentElement.parentElement.children[0].children[0].value=test_values[e.value][n];
                    n++;
                }else if(form_values[i].disabled){
                    if(form_values[i].value == test_values[e.value][n-1])
                        form_values[i].checked=true;
            }
        }
    }

    function ChangeBox(e){
        for(var i in e.parentElement.children){
            try{
                if(e.parentElement.children[i] == e){
                    e.parentElement.parentElement.parentElement.children[0].children[0].children[0].value = e.id;
                    e.children[0].checked=true;
                }
                else{                      
                }
            }catch(e){console.log(e)}
        }   
    }

    function ValueChange(e){
        if(e.type=='range')    e.parentElement.parentElement.children[1].children[0].value = e.value;
        else if(e.type=='text')    e.parentElement.parentElement.children[0].children[0].value = e.value;
    }

    function to33Page(e){
        if($("#page-33").hasClass("D-NONE") && !$("#page-16").hasClass("D-NONE")){
            anime({
                targets: '#page-16',
                // Properties 
                translateX: ["-150%"],
                // Property Parameters
                duration: 1000,
                easing: 'linear',
                // Animation Parameters
            });  
            setTimeout(function(){
                $("#page-16").addClass("D-NONE");
                $("#page-33").removeClass("D-NONE");
                $("#nav-33").removeClass("D-NONE");
                anime({
                    targets: '#page-33',
                    // Properties 
                    translateX: ["0%"],
                    // Property Parameters
                    duration: 1100,
                    easing: 'linear',
                    // Animation Parameters
                 //   direction:'reverse'
                });

                },1000);
             
            }
    }

    function to16Page(e){
        if($("#page-16").hasClass("D-NONE") && !$("#page-33").hasClass("D-NONE")){
            anime({
                targets: '#page-33',
                // Properties 
                translateX: ["0%","150%"],
                // Property Parameters
                duration: 1000,
                easing: 'linear',
                // Animation Parameters
            });

            setTimeout(function() {
                $("#nav-33").addClass("D-NONE")
                $("#page-33").addClass("D-NONE");
                $("#page-16").removeClass("D-NONE");
                anime({
                    targets: '#page-16',
                    // Properties 
                    translateX: "0%",
                    // Property Parameters
                    duration: 1100,
                    easing: 'linear',
                    // Animation Parameters
                });  
            },1000); 
                          
        }
    }

    function nonlogined(){
        toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
        toastr.warning(`해당 서비스는 로그인이 필요한 서비스입니다.`,'로그인이 필요합니다');
        $("html, body").stop().animate({
            scrollTop: form_values[i].getBoundingClientRect().top
        }, 500);
        return;
    }

    function userto16(){
        if(!sessionStorage.key('User')) $("#page-16 .sidediv").addClass('D-NONE');
        $("#main-section").removeClass('D-NONE');
        $("#onlyforuser").addClass('D-NONE');
    //  $("#sideNav")[0].hidden = false;
        to16Page();
    }

    function userto33(){
        $("#main-section").removeClass('D-NONE');
        $("#onlyforuser").addClass('D-NONE');
     // $("#sideNav")[0].hidden = false;
        to33Page();  
    }

    function usertoPage(){
        window.location.href = '/userlog';
    }

if (sessionStorage.key('User')){
    $("#onlyforuser").removeClass('D-NONE');
    $("#main-section").addClass('D-NONE');
    $("input[name=username-0]")[0].value = sessionStorage['User'];
    $("input[name=username-0]")[0].setAttribute('readonly',true);
    $("input[name=username-0]")[1].value = sessionStorage['User'];
    $("input[name=username-0]")[1].setAttribute('readonly',true);
    }
else{
    $("#onlyforuser").removeClass('D-NONE');
    $("#main-section").addClass('D-NONE');
    }
