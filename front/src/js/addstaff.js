function AddStaff() {

}


AddStaff.prototype.listenAddGroupEvent = function () {
    var addBtn = $("#add-group-btn");
    addBtn.click(function () {
        event.preventDefault();
        var telephone = $("input[name='telephone']").val();
        var group = $("select[name='group']").val();
        blogalert.alertConfirm({
            'title': '确认添加吗？',
            'confirmCallback': function () {
                // console.log('123');
                blogajax.post({
                    'url': '/cms/staff_manage/',
                    'data': {
                        'telephone': telephone,
                        'group': group,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location = window.location.href;
                        } else {
                            blogalert.close();
                        }
                    }
                });
            }
        });
    })
};


AddStaff.prototype.run = function () {
    this.listenAddGroupEvent();
};

$(function () {
    var addStaff = new AddStaff();
    addStaff.run();
});