function WebComment() {

}


WebComment.prototype.ListenCommentBtnEvent = function () {
    var submitBtn = $('#comment-btn1');
    var comment = $("input[id='web_comment1']");
    submitBtn.click(function () {
        var commentval = comment.val();

        blogajax.post({
            'url': '/news/web_discuss/',
            'data': {
                'comment': commentval,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var web_comment = result['data'];
                    var ul = $('.web-comment-item');
                    var tpl = template("web-comment-list", {'web_comment': web_comment});
                    ul.append(tpl);
                    comment.val("");
                } else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
};


WebComment.prototype.run = function () {
    var self = this;
    self.ListenCommentBtnEvent();
};


$(function () {
    var webComment = new WebComment();
    webComment.run();
});