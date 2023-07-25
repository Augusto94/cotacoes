// Função para gerar o gráfico de barras com base na moeda selecionada

function generateChart(selectedMoeda) {
    var dataInicioInput = document.getElementById('data_inicio');
    var dataFimInput = document.getElementById('data_fim');

    dataInicioInput.value = moment(data_inicio).toString().slice(0, 15);
    dataFimInput.value = moment(data_fim).toString().slice(0, 15);

    var chartData = data.filter(item => item.moeda === selectedMoeda);
    var dates = [...new Set(chartData.map(item => item.data))];

    var categories = dates.map(date => date);
    var seriesData = dates.map(date => {
        var dataForDate = chartData.filter(item => item.data === date);
        var totalValue = dataForDate.reduce((sum, item) => sum + item.valor, 0);
        return totalValue;
    });

    Highcharts.chart('chart-container', {
        chart: {
            type: 'line' // Mudamos para 'line' para ter um gráfico de linhas
        },
        title: {
            text: 'Cotação do Dólar US$'
        },
        xAxis: {
            categories: categories
        },
        yAxis: {
            title: {
                text: 'Valor'
            },
            tickInterval: 0.05
        },
        series: [{
            name: selectedMoeda,
            data: seriesData
        }]
    });
}

// Função para atualizar o gráfico quando a moeda selecionada mudar
document.getElementById('moeda').addEventListener('change', function() {
    var selectedMoeda = this.value;
    generateChart(selectedMoeda);
});

// Gerar o gráfico inicialmente usando a primeira moeda (Real)
generateChart('Real');
