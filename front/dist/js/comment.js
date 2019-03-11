function NewsComment() {
    var self = this;
    dateFormat = function (value) {
        var date = new Date(value);
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        return year + '年' + month + '月' + day + '日' + ' ' + hours + ':' + minutes;
    }
}

NewsComment.prototype.listenSubmitBtn = function () {
    var submitBtn = $('#comment-submit-btn');
    var textarea = $("textarea[id='comment22']");  //先获取文本框
    submitBtn.click(function () {
        var comment_content = textarea.val();  // 获取文本框的内容
        var news_id = submitBtn.attr('data-news-id');  //将news.id绑定再按钮上。然后点击时获取属性

        blogajax.post({
            'url': '/news/news_comment/',
            'data': {
                'comment_content': comment_content,
                'news_id': news_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var comment = result['data'];  // 获取视图函数返回的序列化后的comment
                    var ul = $('.comment-item');  //获取html body中评论盒子ul的class
                    var tpl = template("comment-list", {'comment': comment});  // 将序列化的comment放入arttemplate模板中
                    ul.prepend(tpl);  //将最新评论插入到最前面
                    window.messageBox.showSuccess('评论成功！');  //评论完成后，弹出提示框
                    textarea.val("");  //评论完成后，将textarea的值清空
                } else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
};


NewsComment.prototype.run = function () {
    var self = this;
    self.listenSubmitBtn();
};


$(function () {
    var newsComment = new NewsComment();
    newsComment.run();
});