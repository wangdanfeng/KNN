$(function () {
        var labels=["飞机","汽车","鸟","猫","鹿","狗","青蛙","马","船","卡车"];
        var l1k1_label_acc=[]
        // 基于准备好的dom，初始化echarts实例
        var klAccChart = echarts.init($('#kl_acc')[0]);

        // 指定图表的配置项和数据
        var kl_option = {
            title: {
                text: '图像识别-L、K准确率对比'
            },
            tooltip: {},
            legend: {},
            xAxis: {
                data: ['L1-K1','L1-K5','L2-K1','L2-K5']
            },
            yAxis: {
                max: 1,
                min: 0

            }
        };
        // 基于准备好的dom，初始化echarts实例
        var labelAccChart = echarts.init($('#label_acc')[0]);

        // 指定图表的配置项和数据
        var label_option = {
            title: {
                text: '图像识别-类别准确率对比'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['L1-K1','L1-K5','L2-K1','L2-K5']
            },
            xAxis: {
                data: labels
            },
            yAxis: {}
        };


        function setOption(opt) {
            var series=[]
            if(opt.series_data){
                $(opt.series_data).each(function (i,s) {
                    series.push({
                        name: opt.legend_data?opt.legend_data[i]:'',
                        type: opt.series_type,
                        data: s
                    })
                })
            }
            return series
        }
        var rtypeS = window.location.search.split('?')[1];
        var rtype = ''
        if(rtypeS){
           rtype = rtypeS.split('=')[1]?rtypeS.split('=')[1]:''
        }

        $.ajax({
            url:'http://172.18.24.28:5001/acc',
            data:{rtype:rtype},
            type:'get',
            success:function (data) {
                if(data.code==200 && data.content.length>0){
                    var label_acc_series_data = [];
                    var acc_legend_data = [];
                    var kl_acc_series_data = [];
                    $(data.content).each(function () {
                        kl_acc_series_data.push(this.acc)
                        acc_legend_data.push(this.kl);
                        label_acc_series_data.push(this.labelAcc);
                    })
                    kl_option.series = setOption({series_type:'bar',series_data:[kl_acc_series_data]});
                    // 使用刚指定的配置项和数据显示图表。
                    klAccChart.setOption(kl_option);

                    label_option.series = setOption({legend_data:label_option.legend.data,series_type:'bar',series_data:label_acc_series_data});
                    // 使用刚指定的配置项和数据显示图表。
                    labelAccChart.setOption(label_option);
                    l1k1_label_acc = label_acc_series_data[0];

                }
            }
        });
        function loadSimilar() {
            $.ajax({
                url:'http://172.18.24.28:5001/similar',
                type:'get',
                data:{"lk":"L1-K1",rtype:rtype},
                success:function (data) {
                    var str = '';
                    var root = window.location.origin;
                    if(data.code==200,data.content){
                        for (k in data.content){

                            str += '<div class="label_pic" id="'+k+'"><div class="labelTxt">' + labels[k]+'<span>'+(Number(l1k1_label_acc[k])*100).toFixed(1)+'%</span>';
                            str += '</div><ul class="label_pic_list">';
                            $(data.content[k]).each(function (i,c) {
                                str += '<li><img src="'+root+'/static/data/img/tests/'+c.file+'" alt="">';

                                $(c.similar).each(function (j,s) {
                                    str += '<img src="'+root+'/static/data/img/trains/'+s[0]+'" title="'+labels[s[2]]+'" class="' +(s[2]==k?'color_g':'color_r')+'">'
                                })
                                str += '</li>';
                            });
                            str += '</ul></div>';

                        }
                        $('#label_pic_box').html(str);
                    }
                }
            });
        }

        timer = setInterval(function () {
            if(l1k1_label_acc.length>0){
                clearInterval(timer);
                loadSimilar();
            }
        },200)





})