
$(function(){
    $(document).on('change', '[id$=item_summary]',function() {
        // 選択したメニューの基本金額を自動入力する
        var menu_id = $(this).val();
        var target_menu;
        for(var index=0; index<g_item_summary_list.length;index++)
        {
            if(g_item_summary_list[index].id == menu_id)
            {
                target_menu = g_item_summary_list[index];
            }
        }

        $(this).parents('table').find('[id$=-base_fee]')
            .val(target_menu.base_fee).change(); // 例外：filterに複数ヒットした場合は先のデータを優先する
    });

    $(document).on('change', '[id$=-base_fee], [id$=-discount]', function(){
        var parent_table = $(this).parents('.table');

        var base_fee_val = parseInt(getDelCommaNumber(parent_table.find('[id$=-base_fee]')));
        var discount_val = parseInt(getDelCommaNumber(parent_table.find('[id$=-discount]')));
        var subtotal_fee_val = "";

        if (!isNaN(base_fee_val) && base_fee_val !=="") {
            // 割引金額が不正または未入力の場合は割引金額を0とする
            if (isNaN(discount_val)) {
                discount_val = 0
            }
            subtotal_fee_val = base_fee_val - discount_val;
        }
        parent_table.find('[id$=-subtotal_fee]').val(subtotal_fee_val).change();
    });

    $(document).on('click', '#id_fee_sum', function(){
        var fee_sum = 0;
        var subtotal_fee = 0;
        $(document).find('[id$=-subtotal_fee]').each(function(index, element){

            subtotal_fee = parseInt(getDelCommaNumber($(element)));
            fee_sum += subtotal_fee;
        });

        $('#id_all_fee').val(fee_sum).change();
    });


    $('#add_more').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#id_rental_form').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    // var rental_menu_list;
    // $('[id$=-kind]').change(function(){
    //     var item_summary_element = $(this).parents('table').find('[id$=-item_summary]');
    //     item_summary_element.html("");
    //     item_summary_element.append(('<option value selected> 選択してください </option>'));
    //
    //     var kind_id = $(this).val();
    //     for(var index=0; index<g_item_summary_list.length;index++)
    //     {
    //         if(g_item_summary_list[index].kind_id == kind_id)
    //         {
    //             item_summary_element.append(('<option value=' + g_item_summary_list[index].id + '>' + g_item_summary_list[index].menu_name + '</option>'))
    //         }
    //     }
    // });

    // $('.btn_user_select_modal').click(function(){
    //     $('#id_user_list').html("");
    //     $('#id_user_list').append(('<tr class="contract_user_tr" id="user-new"> <td>新規登録</td></tr>'));
    //     $.ajax({
    //         'url': 'api/get_user_list',
    //         'type': 'GET',
    //         'data': {
    //             'customer_id': g_customer_number
    //         },
    //         'dataType': 'json'
    //     }).fail(function(){
    //         console.log("error");
    //     }).done(function(response) {
    //         // 利用者リストの生成処理
    //         var user_list = response.user_list;
    //         $.each(user_list,function(index,val){
    //             $('#id_user_list').append('<tr class="contract_user_tr" id="user-list-' + index +
    //                 '"><td id="id_contract_user_number">' + val.user_number + '</td> <td>' + val.first_name + val.second_name + '</td> </tr>');
    //         });
    //     });
    //
    //     var modal_user_select = $('#modal-user-select');
    //     var parent_table = $(this).parents('.table').attr('id');
    //
    //     modal_user_select.removeAttr('menu');
    //     modal_user_select.attr('menu',parent_table);
    //
    //     modal_user_select.modal('show');
    //     return false;
    // });
    //
    // $(document).on('click','#id_user_list td',function () {
    //     var tr_tab = $(this).parent();
    //     var user_number = tr_tab.find('#id_contract_user_number').text();
    //
    //     $.ajax({
    //         'url': 'api/get_user_info',
    //         'type': 'GET',
    //         'data': {
    //             'user_number': user_number
    //         },
    //         'dataType': 'json'
    //     }).fail(function(){
    //         console.log("error");
    //     }).done(function(response){
    //         var target_table_id = $('#modal-user-select').attr('menu');
    //         var target_table = $('#' + target_table_id);
    //
    //         var user_info = response.user_info;
    //         $.each(user_info,function(key,value){
    //            if(target_table.has('#id_' + key)){
    //                target_table.find('#id_' + key).val(value);
    //            }
    //         });
    //     });
    //     $('#modal-user-select').modal('hide');
    //     return false;
    // });

});

