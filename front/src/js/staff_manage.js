function DelStaff() {

}


DelStaff.prototype.ListenDelEvent = function () {
    var delBtn = $('.delete-btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var telephone = currentBtn.attr('data-staff-telephone');
        blogalert.alertConfirm({
            'title': '确认删除吗？',
            'confirmCallback': function () {
                // console.log('123');
                blogajax.post({
                    'url': '/cms/del_staff/',
                    'data': {
                        'telephone': telephone,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.messageBox.showSuccess('删除成功！');
                            window.location = window.location.href;
                        } else {
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
};



DelStaff.prototype.run = function () {
    this.ListenDelEvent();
};


$(function () {
    var delStaff = new DelStaff();
    delStaff.run();
});