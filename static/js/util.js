$(function() {
    $('.calender').datepicker({
        closeText: "閉じる",
        prevText: "&#x3C;前",
        nextText: "次&#x3E;",
        currentText: "今日",
        monthNames: [ "1月","2月","3月","4月","5月","6月",
            "7月","8月","9月","10月","11月","12月" ],
        monthNamesShort: [ "1月","2月","3月","4月","5月","6月",
            "7月","8月","9月","10月","11月","12月" ],
        dayNames: [ "日曜日","月曜日","火曜日","水曜日","木曜日","金曜日","土曜日" ],
        dayNamesShort: [ "日","月","火","水","木","金","土" ],
        dayNamesMin: [ "日","月","火","水","木","金","土" ],
        weekHeader: "週",
        dateFormat: "yy/mm/dd",
        firstDay: 0,
        isRTL: false,
        showMonthAfterYear: true,
        yearSuffix: "年"
    });

    $('.input_number').focusout(function(){
        replaceAddCommaNumber($(this))
    });
    $('.input_number').focusin(function(){
         replaceDelCommaNumber($(this))

    });
    $('.input_number').change(function(){
        replaceAddCommaNumber($(this))
    });

    $('form').submit(function(){
        $('.input_number').each(function(){
            replaceDelCommaNumber($(this))
        });
    })

});

function replaceAddCommaNumber(input_obj){
    var comma_number = getAddCommaNumber(input_obj);

    if(comma_number != null){
        input_obj.val(comma_number)
    }
}

function getAddCommaNumber(input_obj){
    var input_number=input_obj.val();
    var comma_number=null;

    if(!isNaN(input_number)) {
        comma_number = Number(input_number).toLocaleString();
    }

    return comma_number;
}

function replaceDelCommaNumber(input_obj){
    input_obj.val(getDelCommaNumber(input_obj));
}

function getDelCommaNumber(input_obj){
    var comma_number = input_obj.val();

    return comma_number.replace(/,/g,"")
}