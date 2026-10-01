function createChart(id,label,color){

return new Chart(document.getElementById(id),{

type:"line",

data:{
labels:[],
datasets:[{
label:label,
data:[],
borderColor:color
}]
}

})

}

let fuelChart=createChart("fuelChart","Fuel","lime")
let tempChart=createChart("tempChart","Temp","red")
let voltageChart=createChart("voltageChart","Voltage","yellow")
let batteryChart=createChart("batteryChart","Battery","cyan")
let deviationChart=createChart("deviationChart","Deviation","orange")
let radiationChart=createChart("radiationChart","Radiation","purple")
let oxygenChart=createChart("oxygenChart","Oxygen","blue")


function updateCharts(values){

fuelChart.data.labels.push("")
fuelChart.data.datasets[0].data.push(values[0])

tempChart.data.labels.push("")
tempChart.data.datasets[0].data.push(values[1])

voltageChart.data.labels.push("")
voltageChart.data.datasets[0].data.push(values[2])

batteryChart.data.labels.push("")
batteryChart.data.datasets[0].data.push(values[3])

deviationChart.data.labels.push("")
deviationChart.data.datasets[0].data.push(values[4])

radiationChart.data.labels.push("")
radiationChart.data.datasets[0].data.push(values[5])

oxygenChart.data.labels.push("")
oxygenChart.data.datasets[0].data.push(values[6])

fuelChart.update()
tempChart.update()
voltageChart.update()
batteryChart.update()
deviationChart.update()
radiationChart.update()
oxygenChart.update()

}


function updateTelemetry(){

fetch("/telemetry")
.then(res=>res.json())
.then(data=>{

let c=data.current

document.getElementById("fuel").innerText=c[0]
document.getElementById("temp").innerText=c[1]
document.getElementById("voltage").innerText=c[2]
document.getElementById("battery").innerText=c[3]
document.getElementById("deviation").innerText=c[4]
document.getElementById("radiation").innerText=c[5]
document.getElementById("oxygen").innerText=c[6]

updateCharts(c)

document.getElementById("status").innerText=data.status

})

}

setInterval(updateTelemetry,2000)