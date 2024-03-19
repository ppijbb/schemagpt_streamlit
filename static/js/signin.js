try{
        if(logon){
            sessionStorage['User'] = logon;
            if (sessionStorage['User'] !== undefined){
                console.log("Login User:"+sessionStorage['User']);
                $("#menu-section")[0].setAttribute('include-html','views/topbar-login.html');
                try{
                    $("#onlyforuser")[0].setAttribute('include-html','views/onlyforuser.html');
                }
                catch(error){ //console.log(error);}
            }
                }
            else{
                console.log("No Login");
                $("#onlyforuser")[0].setAttribute('include-html','views/onlyforuser.html');
                }
        }
    }
catch(error){
        console.log(error);
        sessionStorage.clear();
        console.log("No Login session is clear");
        $("#onlyforuser")[0].setAttribute('include-html','views/onlyforuser.html');
    }

includeHTML(function () {
    if (sessionStorage['User'] !== undefined){
        $("#Login-Section").text("환영합니다. " + sessionStorage['User']);       
        
    }
    else{
        $("#33BTN").addClass("disabled");
        $("#Userlog").addClass("disabled");
        $("#33BTN")[0].onclick=nonlogined;
        $("#Userlog")[0].onclick=nonlogined;
    }
    includeRouter( function () {
        // do something in the future
        });
    });


// ID, PW 입력에 빈칸 있는지 여부 & sessionStorage 로 ID넘기기
function signin(e){
    var formData = $("#signin_form");
    console.log(formData);
    if(formData[0][2].value == ''){
        console.log('ID빔');
        return;
    }
    else if(formData[0][3].value == '') {
        console.log("PW빔");
        return;
    }
    else{
        console.log(formData[0]);
        console.log("User Data: ",formData[0][0].value, formData[0][1].value);
        //sessionStorage.setItem("User", formData[0][1].value);
        formData[0].submit();
    }
}

function logoutFunction(){
    sessionStorage.clear();
    window.location.href = '/logout';
}