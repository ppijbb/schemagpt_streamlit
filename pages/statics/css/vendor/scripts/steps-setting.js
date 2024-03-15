$(".tab-wizard").steps({
	headerTag: "h5",
	bodyTag: "section",
	transitionEffect: "fade",
	titleTemplate: '<span class="step">#index#</span> #title#',
	labels: {
		finish: "Submit"
	},
	onStepChanged: function (event, currentIndex, priorIndex) {
		$('.steps .current').prevAll().addClass('disabled');
	},
	onFinished: function (event, currentIndex) {
		$('#success-modal').modal('show');
	}
});

$(".tab-wizard2").steps({
	headerTag: "h5",
	bodyTag: "section",
	transitionEffect: "fade",
	titleTemplate: '<span class="step">#index#</span> <span class="info">#title#</span>',
	labels: {
		finish: "제출",
		next: "다음",
		previous: "이전",
	},
	onInit:function(event,currentIndex,priorIndex){
		let pdw = window.location.href.split('/')
		if(pdw[pdw.length-1] =='account'){
			$('form[name=account-form]').find('input[name=id]')[0].value = sessionStorage['User'];
			$('form[name=account-form]').find('input[name=id]')[0].setAttribute('readonly',true);
			$('form[name=account-form]').find('input[name=id]')[0].value = sessionStorage['User'];
			$('form[name=account-form]').append("<input id='withdraw' type='button' value='회원탈퇴' onclick={withdrawfunc(this)}>")
		return true;
		}
	},
	onStepChanging:function(event, currentIndex,priorIndex){
		let pdw = window.location.href.split('/')
		var regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
		if(pdw[pdw.length-1] =='account'){
			$('form[name=account-form]').find('input[name=id]')[0].value = sessionStorage['User'];
			return true;
		}
		else{
			if( $('form[name=register-form]').find('input[name=email]')[0].value == (''|undefined)){
				toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
				toastr.warning(`이메일을 입력하지 않으셨습니다.`,'이메일 미입력');
				return false;
			}
			else if( $('form[name=register-form]').find('input[name=email]').val().match(regExp) == null){
				toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
				toastr.warning(`옳바른 이메일을 입력해주십시오.`,'이메일 형식');
				return false;
			}
			else if( $('form[name=register-form]').find('input[name=id]')[0].value == (''|undefined)){
				toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
				toastr.warning(`아이디를 입력하지 않으셨습니다.`,'아이디 미입력');
				return false;
			}
			else if( $('form[name=register-form]').find('input[name=password]')[0].value == (''|undefined)  &&
			$('form[name=register-form]').find('input[name=password2]')[0].value ==(''|undefined)){
				toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
				toastr.warning(`비밀번호를 입력하지 않으셨습니다.`,'비밀번호 미입력');
				return false;
			}
			else if($('form[name=register-form]').find('input[name=password]')[0].value !== 
			$('form[name=register-form]').find('input[name=password2]')[0].value)
			{
				toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
				toastr.warning(`입력하신 비밀번호가 일치하지 않습니다.`,'비밀번호 불일치');
				return false;
			}
			else{
				$('.steps .current').prevAll().addClass('disabled');
				return true
			}
		}
	},

	onStepChanged: function(event, currentIndex, priorIndex) {

	},
	onFinished: function(event, currentIndex) {
		if($('.custom-control-input')[0].checked){
			$('#success-modal-btn').trigger('click');
			console.log(document.forms['.form-control'][i].value);	
		}
		else {
			console.log("not checked");
			toastr.options={closeButton:true, showMethod:'slideDown',tiemOut:3000};
        	toastr.warning(`약관에 동의하셔야 가입이 진행됩니다.`,'약관 미동의');
        	return;
		}
	}
});