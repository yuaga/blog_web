function NewsList() {
    var self = this;
    self.page = 2;  // 最先写再点击函数中，这样每次点击都是读取第二页的数据，所以要将这个数据拿出来放在主函数中。
    dateFormat = function (value) {
            var date = new Date(value);
            var year = date.getFullYear();
            var month = date.getMonth()+1;
            var day = date.getDate();
            var hours = date.getHours();
            var minutes = date.getMinutes();
            return year + '年'+ month + '月' + day +'日'+' '+hours+':'+minutes;
    }
}

NewsList.prototype.listenLoadMoreEvent = function () {
    var self = this;
    var loadBtn = $('#load-more-btn');
    loadBtn.click(function () {
        // var page = 2;
        blogajax.get({
            'url': '/news/news_list/',
            'data': {
                'p': self.page,  // 再将主函数的page传进来，这个数据会传到url中，/news_list/?p=p
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data'];  // 视图函数中返回的，将其提取出来
                    if (newses.length > 0) {     // 判断有多少条新闻，新闻没有的时候，加载按键隐藏。
                        var tpl = template("news-list", {'newses': newses});
                        var ul = $('.news-list-group');
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        loadBtn.hide();
                    }
                }
            }
        });
    });
};


NewsList.prototype.run = function () {
    var self = this;
    self.listenLoadMoreEvent();
};


$(function () {
    var newslist = new NewsList();
    newslist.run();
});