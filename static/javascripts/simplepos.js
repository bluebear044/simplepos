$( document ).ready(function() {
    console.log( "ready!" );

    // 현재시간 출력 -- common.js
    printTime("clock");

    // dialog event
    $( "#dialog" ).click(function() {
        $(this).dialog('close');
    });

    // 좌측상단 +버튼
    $( "#productCreate" ).click(function() {

    	$( "#newProductForm" ).show();
        $( "#productName" ).focus();
	
	});

    // 좌측상단 -버튼
    $( "#productDelete" ).click(function() {

    	var slectedElement = getSelectedElement();
		if(slectedElement != null) {
		  $("#productCode").val(slectedElement.data().code);
		  $("form[name='deleteForm']").submit();
        }

    });

    // 상품목록 아이템
    $( ".product-item" ).click(function() {

    	$( ".product-item" ).removeClass("hover");
    	$(this).addClass("hover");

    	$( "#newProductForm" ).hide();

    });

    // 상품생성 저장버튼
    $( "#newProductSave" ).click(function() {
        saveProduct();
	});

    // 엑셀다운로드
    $( "#excelDownload" ).click(function() {
        //TODO
    });

    // 판매내역
    $( "#saleStatus" ).click(function() {
        $( "#dialog" ).dialog({
            width: 900
            , height: 600
            ,resizable: false
        });
    });

    // 판매마감
    $( "#endOfSale" ).click(function() {

        if (confirm("판매마감 하시겠습니까?") == true){
            $("form[name='endOfSaleForm']").submit();
        }else{
            return;
        }
        
    });

    // 판매수량 설정
    $( "#saleQuantity" ).click(function() {

        var slectedElement = getSelectedElement();
        if(slectedElement != null) {

            var nvalue = Number($("#numberValue").html());
            if(nvalue == 0) {
                alert("판매수량을 설정하세요.");
                return;
            }

            makeSaleItem(
                slectedElement.data().code
                , slectedElement.data().name
                , nvalue
                , nvalue * Number(slectedElement.data().price)
            );

        }

    });

    // 판매가격 설정
    $( "#salePrice" ).click(function() {

        var slectedElement = getSelectedElement();
        if(slectedElement != null) {

            var nvalue = Number($("#numberValue").html());
            if(nvalue == 0) {
                alert("판매가격을 설정하세요.");
                return;
            }

            makeSaleItem(
                slectedElement.data().code
                , slectedElement.data().name
                , "1"
                , nvalue * Number(slectedElement.data().price)
            );
            
        }


    });

    // 판매완료
    $( "#saleSave" ).click(function() {

        if (confirm("판매 하시겠습니까?") == true){

            if($("#saleSum").html() == "0") {
                alert("판매 할 물건이 없습니다.");
                return;
            }

            $("form[name='saleForm']").submit();
        }else{
            return;
        }

    });

    // 키패드 이벤트
    $('[id^=keypad]').each(function() {

        var idValue = $(this).attr("id");
        idValue = idValue.replace("keypad","");

        if(isNaN(idValue)) {

            if(idValue == "BackSpace") {

                $( "#keypad" + idValue ).click(function() {
                    var numberValue = $("#numberValue").html();
                    numberValue = numberValue.substring(0, numberValue.length - 1);
                    if(numberValue == "") {
                        numberValue = 0;
                    }
                    $("#numberValue").html(numberValue);
                });

            }else if(idValue == "Clear") {

                $( "#keypad" + idValue ).click(function() {
                    $("#numberValue").html("0");
                });

            }else if(idValue == "PlusOne") {

                $( "#keypad" + idValue ).click(function() {
                    var nvalue = Number($("#numberValue").html());
                    $("#numberValue").html((nvalue+1).toString());
                });

            }else if(idValue == "MinusOne") {

                $( "#keypad" + idValue ).click(function() {
                    var nvalue = Number($("#numberValue").html());
                    if(nvalue > 0) {
                        $("#numberValue").html((nvalue-1).toString());
                    }
                });

            }

        }else {

            $( "#keypad" + idValue ).click(function() {

                var numberValue = $("#numberValue").html();
                if(numberValue == "0") {
                    numberValue = idValue;
                }else {
                    numberValue = numberValue + "" + idValue;
                }

                $("#numberValue").html(numberValue);

            });

        }
        
    });

});

function makeSaleItem(code, name, qty, price) {
    var uniqueKey = makeRandomNumber();
    var appendItemHtml = "";
    appendItemHtml += "<div id=\"" + uniqueKey + "\">";
    appendItemHtml += "<div class=\"col-sm-4 sale-item\" >" + name + " </div>";
    appendItemHtml += "<div class=\"col-sm-3 sale-item\" >" + qty + "</span>" + "개</div>";
    appendItemHtml += "<div class=\"col-sm-4 sale-item\" >₩ <span id=\"price_" + uniqueKey + "\">" + price + "</span>" + "</div>";
    appendItemHtml += "<div class=\"col-sm-1 sale-item\" id=\"remove_" + uniqueKey + "\"><span class=\"glyphicon glyphicon-remove\"></span></div>";
    
    //hidden form
    appendItemHtml += "<input type=\"hidden\" name=\"id\" value=\"" + uniqueKey + "\">";
    appendItemHtml += "<input type=\"hidden\" name=\"code_" + uniqueKey + "\" value=\"" + code + "\">";
    appendItemHtml += "<input type=\"hidden\" name=\"qty_" + uniqueKey + "\" value=\"" + qty + "\">";
    appendItemHtml += "<input type=\"hidden\" name=\"price_" + uniqueKey + "\" value=\"" + price + "\">";

    appendItemHtml += "</div>";

    $("#saleList").append(appendItemHtml);
    registerSaleItemRemoveEvent(uniqueKey);
    
    var saleSum = Number($("#saleSum").html());
    $("#saleSum").html(saleSum+=price);

    $("#numberValue").html("0");
}

function registerSaleItemRemoveEvent(uniqueKey) {

    $(document).on("click","#remove_"+uniqueKey,function(){

        //합계금액에서 빼기
        var saleSum = Number($("#saleSum").html());
        saleSum -= Number($( "#price_"+uniqueKey ).html());
        $("#saleSum").html(saleSum);
        
        $( "#"+uniqueKey ).remove();

    });

}

function getSelectedElement() {

    var slectedElement = null;
    $.each( $( ".product-item" ), function() {
        if($(this).hasClass("hover")) {
            slectedElement = $(this);
        }
    });

    if(slectedElement == null) {
        alert("상품을 선택하세요.");
    }

    return slectedElement;

}

function saveProduct() {
    if($( "#productName" ).val() == "") {
        alert("상품이름을 입력해주세요.");
        $( "#productName" ).focus();
        return;
    }

    if($( "#productPrice" ).val() == "") {
        alert("상품가격을 입력해주세요.");
        $( "#productPrice" ).focus();
        return;
    }

    if(isNaN($( "#productPrice" ).val()) == true) {
        alert("상품가격은 숫자만 입력해주세요.");
        $( "#productPrice" ).focus();
        $( "#productPrice" ).val("");
        return;
    }

    $("form[name='saveForm']").submit();

}

function runScript(e) {
    if (e.keyCode == 13) {
        saveProduct();
        return false;
    }
}