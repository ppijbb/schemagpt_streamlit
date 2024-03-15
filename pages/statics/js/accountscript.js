includeHTML( function () {
    // if (sessionStorage.key('User')){
    //     $("#Login-Section").text("환영합니다. " + sessionStorage['User']);
    // }
    // else{
    //     $("#33BTN").addClass("disalbed");
    //     console.log($("#33BTN")[0].onclick=nonlogined);
    // }
    includeRouter( function () {
        // do something in the future
        });
    });


function withdrawfunc(e){
    if(window.confirm("정말 탈퇴하시겠습니까?")){
        console.log("탈퇴 절차를 진행합니다");
        window.location.href = '/withdraw';
    }
}
