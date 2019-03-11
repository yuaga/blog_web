function News() {

}

//  初始化富文本编辑器
News.prototype.initUEditor = function () {
    window.ue = UE.getEditor('container', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',  // 这是配置文件上传路径，不然图片上传功能不能使用，必须得写。
    });
};

News.prototype.listenUploadFileEvent = function () {
    var thumbnailBtn = $('#thumbnail-btn');
    // 此处不再是点击事件了，因为上传文件那个按钮我们点击的时候弹出对话框浏览器自动帮我们完成。
    thumbnailBtn.change(function () {
        //this代表当前按键，当选定文件后，文件保存再按键上，所以再按键上获取文件，上传文件时可以选多个文件，这里默认上传第一个文件
        var file = this.files[0];
        // 获取到文件之后呢，怎么办。发送给服务器，不能直接发送，将文件存储再formdata中。
        var formData = new FormData();
        formData.append('file', file); //引号中的file是与后端视图函数中的字段名保持一致
        blogajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,  // 因为上传的是文件，告诉jquery不用再处理了，不是文本字符串
            'contentType': false,  // 默认使用这个文件的形式
            'success': function (result) {
                if (result['code'] === 200) {
                    // console.log(result['data']);  // 文件上传成功后，会返回连接，存储再result中的data中
                    var url = result['data']['url'];  //从视图函数返回的result中提取url,并放到框框中
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        })

    });
};

// 发布新闻及编辑新闻
News.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        // console.log('跑到这里了');
        event.preventDefault();  //阻止表单的传统发送行为
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        var btn = $(this); //编辑新闻新增
        var id = btn.attr('data-news-id');  //编辑新闻新增
        var url='';   //编辑新闻新增
        if(id){
            url='/cms/edit_news/';
        }else{
            url='/cms/write_news/';
        }  //编辑新闻新增

        blogajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'id':id,  //这行新编辑新闻功能新增的，是传给后端视图函数的
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    blogalert.alertSuccess('发布成功', function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

News.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.listenUploadFileEvent();
    self.listenSubmitEvent();
};


$(function () {
    var news = new News();
    news.run();
});

