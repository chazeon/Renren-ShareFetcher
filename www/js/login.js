
function State() {
	this.login_state = {}
	this.post = function() {
		var post_data = $.param({"email": $("input#username").val(), "password": $("input#password").val(), "icode": $("input#icode").val()})
		$.ajax({
			url:"/login?" + post_data,
			async:false,
			success: function(data){
				result = $.parseJSON(data);
			}
		});
		return result;
	}
}

state = new State();

function View () {
	this.checkField = function (field) {
		if ($("input" + field).val() == "") {
			$("div.field" + field).addClass("error");
			return false;
		} else {
			$("div.field" + field).removeClass("error");
			return true;
		}
	}

	var checkField = this.checkField;

	this.checkForm = function () {
		var un = checkField("#username");
		var pw = checkField("#password");
		var ic = checkField("#icode");
		if (un == true && pw == true && ic == true) {
			return true;
		} else {
			return false;
		}
	}

	this.warnError = function (message) {
		$("div.field#username").before(
			'<div class="ui error message">'+
			//'<div class="header">Something went wrong.</div>'+
			'<p>'+message+'</p></div>')
	}

	this.clearError = function () {
		$("div.error.message").detach()
	}

	var clearError = this.clearError;
	var warnError = this.warnError;
	var checkForm = this.checkForm;


	this.loadForm = function() {

		//$("input#icode").popup({on: "focus"});
		$("input").keydown(function(e){
			if (e.keyCode == 13) {
				$("div.button#login").click()
			}
		})
		$("div.button#login").click(function(){
			clearError();
			if (checkForm() == true){
				login_state = state.post();
				if (login_state.code == false) {
					warnError(login_state["failDescription"])
					$("div.button#login").click(function(){
						if ($("div.button#login").attr("class").split(/ +/).index("disabled") == -1)
							$("img#icode").attr("src", "verify?rand=" + Math.random()); // to be replaced
					})
				} else {
					$("div.field").addClass("disabled");
					$("div.button#login").html("<i class='loading icon'></i>Working").addClass("disabled");
					$.get("retrive", function(data){
						$(".disabled").removeClass("disabled");
						$("div.button#login").html(data);
						setTimeout(function(){
							$("div.button#login").html("Login");
						}, 8000);
					})
				}
			} else {
				warnError("Missing field");
			}
		})
	}

}

view = new View();
view.loadForm();
