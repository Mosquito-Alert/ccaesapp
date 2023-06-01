(function($){

    Highcharts.setOptions({
        lang: {
            downloadCSV: "Descargar hoja de cálculo CSV",
            viewFullscreen: "Ver a pantalla completa",
            printChart: "Imprimir gráfica",
            downloadPNG: "Descargar imagen PNG",
            downloadJPEG: "Descargar imagen JPEG",
            downloadPDF: "Descargar documento PDF",
            downloadSVG: "Descargar imagen vectorial SVG",
            downloadXLS: "Descargar hoja de cálculo XLS",
            viewData: "Ver datos",
            hideData: "Esconder datos",
        }
    });

    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },
        title: null,
        pane: {
            center: ['50%', '85%'],
            size: '100%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: false
        },
        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 2,
            title: {
                y: -150
            },
            labels: {
                y: 16
            }
        },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    var createNReportGauge = function( div_id, data, min, max ){
        // The speed gauge
        var numberReports = Highcharts.chart(div_id, Highcharts.merge(gaugeOptions, {
            yAxis: {
                min: min,
                max: max,
                title: {
                    text: 'Número de informes durante los últimos 7 días'
                }
            },

            credits: {
                enabled: false
            },

            series: [{
                name: 'N',
                data: [data],
                dataLabels: {
                    format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                        ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                           '<span style="font-size:12px;color:silver">Informes</span></div>'
                },
                tooltip: {
                    valueSuffix: ' Informes'
                }
            }]

        }));
        return numberReports;
    }

    var createFlowReportGauge = function(div_id, data, min, max){
        var reportFlow = Highcharts.chart(div_id, Highcharts.merge(gaugeOptions, {
            yAxis: {
                min: min,
                max: max,
                title: {
                    text: 'Media de número de informes por día durante los últimos 7 días'
                }
            },

            series: [{
                name: 'Reports',
                data: [data],
                dataLabels: {
                    format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                        ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                           '<span style="font-size:12px;color:silver">Informes</span></div>'
                },
                tooltip: {
                    valueSuffix: ' Informes'
                }
            }]

        }));
        return reportFlow;
    }

    var createChart = function(){
        var chart = Highcharts.chart('chart', {
            chart:{
                type: 'column'
            },
            title: {
                text: '',
                align: 'left'
            },
            /*subtitle: {
                text: 'Fuente: <a href="#" target="_blank">Mosquito Alert</a>',
                align: 'left'
            },*/

            yAxis: {
                title: {
                    text: 'Observaciones de Mosquito'
                }
            },

            xAxis: {
                categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            },

            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },

            plotOptions:{
                series:{
                    dataLabels:{
                        enabled: true
                    }
                }
            },

            series: [],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }

        });
        return chart;
    }

    var createParticipationChart = function(container,categories,data,title,series_name){
        var chart = Highcharts.chart(container, {
            chart: {
                type: 'bar'
            },
            title: {
                text: title,
                align: 'left'
            },
            /*subtitle: {
                text: 'Source: <a ' +
                    'href="https://en.wikipedia.org/wiki/List_of_continents_and_continental_subregions_by_population"' +
                    'target="_blank">Wikipedia.org</a>',
                align: 'left'
            },*/
            xAxis: {
                categories: categories,
                title: {
                    text: null
                },
                gridLineWidth: 1,
                lineWidth: 0
            },
            yAxis: {
                min: 0,
                title: {
                    text: '',
                    align: 'high'
                },
                labels: {
                    //overflow: 'justify'
                    enabled: false
                },
                gridLineWidth: 0
            },
            tooltip: {
                valueSuffix: ' informes'
            },
            plotOptions: {
                bar: {
                    borderRadius: '50%',
                    dataLabels: {
                        enabled: true
                    },
                    groupPadding: 0.1
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -40,
                y: 80,
                floating: true,
                borderWidth: 1,
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
                shadow: true
            },
            credits: {
                enabled: false
            },
            series: [{
                data: data,
                name: series_name
            }]
        });
        return chart;
    }



    var chart
    if(no_data_barchart){
         chart = createChart();
    }

    var addSeries = function(chart, data, series_name){
        chart.addSeries({
            type: 'column',
            name: series_name,
            data: data,
            //color: site_colors[ year ]
        });
    };

    var highlight_ccaa = function(chart){
        var series = chart.series;
        series[0].points.forEach(point => {
            if (point.category === ccaa_name) {
                const highlightedColor = series.index === 0 ? 'hotpink' : 'red';
                point.update({
                    color: highlightedColor
                })
            }
        })
    };

    var extract_category_data = function(all_data, category){
        var data = Array(12).fill(0);
        for(var i = 0; i < all_data.length; i++){
            var this_data = all_data[i];
            if(this_data[2]==category){
                data[this_data[1]-1]=this_data[0];
            }
        }
        return data;
    }

    var all_categories = raw_data.map(x => x[2]);
    var single_categories = [...new Set(all_categories)];

    for(var i = 0; i < single_categories.length; i++){
        var category = single_categories[i];
        var category_data = extract_category_data(raw_data, category);
        addSeries(chart, category_data, category);
    }

    var table = $('#example').DataTable({
        data: dataSet,
        columns: [
            { title: 'Provincia' },
            { title: 'Municipio' },
            { title: 'Mosquito tigre' },
            { title: 'Mosquito Tigre - Trampeo' },
            { title: 'Mosquito Tigre - MA' },
            { title: 'Mosquito común' },
            { title: 'Picaduras' }
        ],
        columnDefs: [
            {
                'targets':3,
                'sortable': true,
                'render': function(data, type){
                    if (type === 'sort' || type === 'type') {
                        return data;
                    }
                    if(data==null){
                        return '<div style="color:gray">&#9632;Sin datos</div>';
                    }else{
                        if(data == true){
                            return '<div style="color:red">&#9632;Detectado</div>';
                        }else{
                            return '<div style="color:green">&#9632;No detectado</div>';
                        }
                    }
                }
            },
            {
                'targets':4,
                'sortable': true,
                'render': function(data, type){
                    if (type === 'sort' || type === 'type') {
                        return data;
                    }
                    if(data==null){
                        return '<div style="color:gray">&#9632;Sin datos</div>';
                    }else{
                        if(data == true){
                            return '<div style="color:#FDDA0D">&#9632;Detectado</div>';
                        }else{
                            return '<div style="color:green">&#9632;No detectado</div>';
                        }
                    }
                }
            }
        ],
        'order': [[ 2, "desc" ]],
        pageLength: 10,
        language: dt_es,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ]
    });

    var cc_aa_bites = [];
    var data_bites = [];
    for(var i = 0; i < participation_data.bite.length; i++){
        cc_aa_bites.push(participation_data.bite[i][0]);
        data_bites.push(participation_data.bite[i][1]);
    }
    var chart_bites = createParticipationChart('p_bites',cc_aa_bites,data_bites,'Número de informes de picadura por Comunidad Autónoma','picaduras');

    var cc_aa_mosquito = [];
    var data_mosquito = [];
    for(var i = 0; i < participation_data.mosquito.length; i++){
        cc_aa_mosquito.push(participation_data.mosquito[i][0]);
        data_mosquito.push(participation_data.mosquito[i][1]);
    }
    var chart_mosquitos = createParticipationChart('p_mosquitos',cc_aa_mosquito,data_mosquito,'Número de informes de mosquito por Comunidad Autónoma','mosquitos');

    var cc_aa_site = [];
    var data_site = [];
    for(var i = 0; i < participation_data.site.length; i++){
        cc_aa_site.push(participation_data.site[i][0]);
        data_site.push(participation_data.site[i][1]);
    }
    var chart_sites = createParticipationChart('p_sites',cc_aa_site,data_site,'Número de lugares de cría por Comunidad Autónoma','lugares de cría');

    highlight_ccaa(chart_bites);
    highlight_ccaa(chart_mosquitos);
    highlight_ccaa(chart_sites);

    createNReportGauge('container-number-ccaa',n_7_days_ccaa,0,200);
    createFlowReportGauge('container-flow-ccaa',avg_7_days_ccaa,0,30);
    createNReportGauge('container-number-world',n_7_days_world,0,2000);
    createFlowReportGauge('container-flow-world',avg_7_days_world,0,200);


})(jQuery);


