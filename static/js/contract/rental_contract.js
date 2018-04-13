
$(function(){
    var rental_menu_list;
    $('[id$=kind]').change(function(){
        var item_summary_element = $(this).parents('table').find('[id$=item_summary]');
        item_summary_element.html("");
        item_summary_element.append(('<option value selected> 選択してください </option>'));

        for(var index=0; index<g_item_summary_list.length;index++)
        {
            if(g_item_summary_list[index].kind__kind_id == $(this).val())
            {
                item_summary_element.append(('<option value=' + g_item_summary_list[index].id + '>' + g_item_summary_list[index].menu_name + '</option>'))
            }
        }
    });

    $('[id$=item_summary]').change(function() {
        var item_id = $(this).val();
        var rental_item = g_item_summary_list.filter(function (item, index) {
            if (item.id == item_id ) return true;
        });

        $(this).parents('table').find('[id$=base_fee]')
            .val(rental_item[0].base_fee).change(); // 例外：filterに複数ヒットした場合は先のデータを優先する
    });

    $('#id_base_fee , #id_discount').change(function(){
        var base_fee = parseInt(getDelCommaNumber($('#id_base_fee')));
        var discount = parseInt(getDelCommaNumber($('#id_discount')));

        if (isNaN(base_fee)) {
            $('#id_total_fee').val(null)
        }
        else {
            // 割引金額が不正または未入力の場合は割引金額を0とする
            if(isNaN(discount)){
                discount = 0
            }
            $('#id_total_fee').val(base_fee - discount).change();
        }
    });

    $('.btn_user_select_modal').click(function(){
        $('#id_user_list').html("");
        $('#id_user_list').append(('<tr class="contract_user_tr" id="user-new"> <td>新規登録</td></tr>'));
        $.ajax({
            'url': 'api/get_user_list',
            'type': 'GET',
            'data': {
                'customer_id': g_customer_number
            },
            'dataType': 'json'
        }).fail(function(){
            console.log("error");
        }).done(function(response) {
            // 利用者リストの生成処理
            var user_list = response.user_list;
            $.each(user_list,function(index,val){
                $('#id_user_list').append('<tr class="contract_user_tr" id="user-list-' + index +
                    '"><td id="id_contract_user_number">' + val.user_number + '</td> <td>' + val.first_name + val.second_name + '</td> </tr>');
            });
        });

        var modal_user_select = $('#modal-user-select');
        var parent_table = $(this).parents('.table').attr('id');

        modal_user_select.removeAttr('menu');
        modal_user_select.attr('menu',parent_table);

        modal_user_select.modal('show');
        return false;
    });

    $(document).on('click','#id_user_list td',function () {
        var tr_tab = $(this).parent();
        var user_number = tr_tab.find('#id_contract_user_number').text();

        $.ajax({
            'url': 'api/get_user_info',
            'type': 'GET',
            'data': {
                'user_number': user_number
            },
            'dataType': 'json'
        }).fail(function(){
            console.log("error");
        }).done(function(response){
            var target_table_id = $('#modal-user-select').attr('menu');
            var target_table = $('#' + target_table_id);

            var user_info = response.user_info;
            $.each(user_info,function(key,value){
               if(target_table.has('#id_' + key)){
                   target_table.find('#id_' + key).val(value);
               }
            });

            // target_table.find('#id_user_number').val(user_number);
            // target_table.find('#id_first_name').val(user_info.first_name);
            // target_table.find('#id_second_name').val(user_info.second_name);
            // target_table.find('#id_first_name_kana').val(user_info.first_name_kana);
            // target_table.find('#id_second_name_kana').val(user_info.second_name_kana);
            // target_table.find('#id_age').val(user_info.age);
            // target_table.find('#id_height').val(user_info.height);
            // target_table.find('#id_wight').val(user_info.wight);
            // target_table.find('#id_foot').val(user_info.foot);
        });
        $('#modal-user-select').modal('hide');
        return false;
    });

    $('#add_more').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#id_rental_form').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

});

