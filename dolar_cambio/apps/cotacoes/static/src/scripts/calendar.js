var i18n = {
    previousMonth: 'Mês anterior',
    nextMonth: 'Próximo mês',
    months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    weekdays: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
    weekdaysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
};


function isDiaUtil(date) {
    const day = date.day();
    return day >= 1 && day <= 5; // 1 é segunda-feira e 5 é sexta-feira
}

// Função para adicionar um número de dias úteis a uma data
function adicionarDiasUteis(date, dias) {
    let diasAdicionados = 0;
    date.subtract(1, 'day')
    while (diasAdicionados < dias) {
        date.add(1, 'day');
        if (isDiaUtil(date)) {
            diasAdicionados++;
        }
    }

    return date;
}

// Função para subtrair um número de dias úteis de uma data
function subtrairDiasUteis(date, dias) {
    let diasSubtraidos = 0;
    date.add(1, 'day')
    while (diasSubtraidos < dias) {
        date.subtract(1, 'day');
        if (isDiaUtil(date)) {
            diasSubtraidos++;
        }
    }

    return date;
}

// Função para inicializar os datepickers
function initDatePickers() {
    var dataInicioInput = document.getElementById('data_inicio');
    var dataFimInput = document.getElementById('data_fim');
    var pickerInicio = new Pikaday({
        field: dataInicioInput,
        format: 'YYYY-MM-DD', // Formato da data
        maxDate: moment().toDate(),
        i18n: i18n,
        onSelect: function(selectedDate) {
            var dataFim = adicionarDiasUteis(moment(selectedDate), 5).format("YYYY-MM-DD");
            dataInicioInput.value = moment(selectedDate).format("llll").slice(0, -9);
            dataFimInput.value = moment(dataFim).format("llll").slice(0, -9);
        }
    });

    var pickerFim = new Pikaday({
        field: dataFimInput,
        format: 'YYYY-MM-DD', // Formato da data
        maxDate: moment().toDate(),
        i18n: i18n,
        onSelect: function(selectedDate) {
            var dataInicio = subtrairDiasUteis(moment(selectedDate), 5).format("YYYY-MM-DD");
            dataFimInput.value = moment(selectedDate).format("llll").slice(0, -9);
            dataInicioInput.value = moment(dataInicio).format("llll").slice(0, -9);
        }
    });
}

function consultarDatas() {
    var dataInicio = document.getElementById('data_inicio').value;
    var dataFim = document.getElementById('data_fim').value;

    // Montar a URL com as datas selecionadas como parâmetros de consulta
    var urlConsulta = '?data_inicio=' + moment(dataInicio)._i.slice(5).split(" ").join("-") + '&data_fim=' + moment(dataFim)._i.slice(5).split(" ").join("-")

    // Redirecionar para a URL de consulta
    window.location.href = urlConsulta;
}

moment.locale('pt-br');
// Adicionar o evento de clique ao botão "Consultar"
document.getElementById('btnConsultar').addEventListener('click', consultarDatas);

// Inicializar os datepickers
initDatePickers();
