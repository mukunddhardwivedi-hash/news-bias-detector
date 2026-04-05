const API = "https://news-bias-api-vv2o.onrender.com"
let biasChart
let sentimentChart

async function fetchNews(){
await fetch(`${API}/fetch`,{method:"POST"})
loadArticles()
}

async function loadArticles(){

const res = await fetch(`${API}/articles`)
const data = await res.json()

const container = document.getElementById("articles")

container.innerHTML=""

let biasCount={left:0,center:0,right:0}
let sentimentCount={positive:0,neutral:0,negative:0}

data.forEach(a=>{

biasCount[a.bias]++
sentimentCount[a.sentiment]++

container.innerHTML += `
<div class="card">

<a href="${a.url}" target="_blank">
${a.title}
</a>

<p>${a.summary}</p>

<small>${a.source}</small>

<br>

Bias: ${a.bias} | Sentiment: ${a.sentiment}

</div>
`
})

drawCharts(biasCount,sentimentCount)

}

function drawCharts(bias,sentiment){

if(biasChart) biasChart.destroy()

biasChart=new Chart(
document.getElementById("biasChart"),
{
type:"doughnut",
data:{
labels:["Left","Center","Right"],
datasets:[{
data:[bias.left,bias.center,bias.right]
}]
}
}
)

if(sentimentChart) sentimentChart.destroy()

sentimentChart=new Chart(
document.getElementById("sentimentChart"),
{
type:"doughnut",
data:{
labels:["Positive","Neutral","Negative"],
datasets:[{
data:[
sentiment.positive,
sentiment.neutral,
sentiment.negative
]
}]
}
}
)

}

document
.getElementById("refresh")
.addEventListener("click",fetchNews)

loadArticles()