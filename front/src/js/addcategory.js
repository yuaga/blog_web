function NewsCategory() {

}


NewsCategory.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDelCategoryEvent();
};

NewsCategory.prototype.listenAddCategoryEvent = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        blogalert.alertOneInput({
            'title': '添加分类',
            'placeholder': '请输入分类',
            'confirmCallback': function (inputValue) {
                blogajax.post({
                    'url': '/cms/add_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload();
                        } else {
                            blogalert.close();
                        }
                    }
                });
            }
        });
    });
};

NewsCategory.prototype.listenEditCategoryEvent = function () {
    var self = this;
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        blogalert.alertOneInput({
            'title': '编辑分类',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                blogajax.post({
                    'url': '/cms/edit_category/',
                    'data': {
                        'pk': pk,
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location = window.location.href;
                            // window.location.reload();
                        } else {
                            blogalert.close();
                        }
                    }
                });
            }
        });
    });
};

NewsCategory.prototype.listenDelCategoryEvent = function () {
    var self = this;
    var delBtn = $('.delete-btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        blogalert.alertConfirm({
            'title': '确认删除吗？',
            'confirmCallback': function () {
                console.log('pp');
                blogajax.post({
                    'url': '/cms/del_category/',
                    'data': {
                        'pk': pk,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location = window.location.href;
                            // window.location.reload();
                        } else {
                            blogalert.close();
                        }
                    }
                });
                // console.log('pp1');
            }
        });
    });
};

$(function () {
    var category = new NewsCategory();
    category.run();
});