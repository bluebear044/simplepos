function makeRandomNumber() {
	return Math.floor(Math.random()*90000) + 10000;
}

function printTime(id) {
    date = new Date;
    year = date.getFullYear();
    month = date.getMonth();
    months = new Array('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12');
    d = date.getDate();
    day = date.getDay();
    days = new Array('일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일');
    h = date.getHours();
    if(h<10) {
    	h = "0"+h;
    }
    m = date.getMinutes();
    if(m<10) {
    	m = "0"+m;
    }
    s = date.getSeconds();
    if(s<10) {
    	s = "0"+s;
    }
    result = ''+year+'년 '+months[month]+'월 '+d+'일 '+days[day]+' '+h+':'+m+':'+s;
    document.getElementById(id).innerHTML = result;
    setTimeout('printTime("'+id+'");','1000');
    return true;
}

function checkForNumber() {
  var key = event.keyCode;
  console.log("key : " + key);
  if(!(key==8||key==9||key==13||key==46||key==144||
      (key>=48&&key<=57)||key==110||key==190)) {
      event.returnValue = false;
  }
}

function commaNum(num) {
	var len, point, str;

	num = num + "";
	point = num.length % 3
	len = num.length;

	str = num.substring(0, point);
	while (point < len) {
		if (str != "") str += ",";
		str += num.substring(point, point + 3);
		point += 3;
	}
	return str;
}

var ajax = {

	post: function(form, message, async) {
		var postData = form.serializeArray();
		var formURL = form.attr("action");
		$.ajax(
		{
			async: async == undefined ? true : false,
			cache: true,
			url : formURL,
			type: "POST",
			data : postData,
			success:function(data) 
			{
				if(message != undefined) {
					drawToast(message);		
				}else {
					console.log("성공");					
				}
			},
			error: function(jqXHR, textStatus, errorThrown) 
			{
				console.log("ERROR !!");
				drawToast("오류가 발생했습니다.");
			}
		});

	}

	,get: function(form, message, async) {
		var postData = form.serializeArray();
		var formURL = form.attr("action");
		$.ajax(
		{
			async: async == undefined ? true : false,
			cache: true,
			url : formURL,
			type: "GET",
			data : postData,
			success:function(data) 
			{
				if(message != undefined) {
					drawToast(message);		
				}else {
					console.log("성공");					
				}
			},
			error: function(jqXHR, textStatus, errorThrown) 
			{
				console.log("ERROR !!");
				drawToast("오류가 발생했습니다.");
			}
		});

	}
}

//toast.js [START]
var intervalCounter = 0;

function hideToast(){
	var alert = document.getElementById("toast");
	alert.style.opacity = 0;
	clearInterval(intervalCounter);
}

function drawToast(message){
	
	var alert = document.getElementById("toast");
	
	if (alert == null){
		var toastHTML = '<div id="toast">' + message + '</div>';
		document.body.insertAdjacentHTML('beforeEnd', toastHTML);
	}
	else{
		alert.style.opacity = .9;
	}
	
	
	intervalCounter = setInterval("hideToast()", 1000);
}
//toast.js [END]