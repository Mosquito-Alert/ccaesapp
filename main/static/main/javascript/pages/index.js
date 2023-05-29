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
            { title: 'Picaduras' },
            { title: 'Mosquito tigre' },
            { title: 'Mosquito fiebre amarilla' },
            { title: 'Mosquito común' },
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


})(jQuery);


