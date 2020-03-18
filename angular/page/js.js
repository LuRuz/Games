var data = { "numberDays" : 31, "start" : 4 , "mes" : "Enero"} 
//Leer json con los datos de como situar los dias

function lee_json() {
    for (i=data.start ; i<data.numberDays ; i++ ){
        document.getElementById(i).innerHTML = (i-data.start+1);
    }

    document.getElementById('mes').innerHTML = data.mes;
}
