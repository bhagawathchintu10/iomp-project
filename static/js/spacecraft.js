const container = document.getElementById("simulation")
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75,700/500,0.1,1000)
const renderer = new THREE.WebGLRenderer({antialias:true})
renderer.setSize(700,500)
container.appendChild(renderer.domElement)

// lights
const ambient = new THREE.AmbientLight(0xffffff,1.2)
scene.add(ambient)
const light = new THREE.PointLight(0xffffff,2)
light.position.set(10,10,10)
scene.add(light)

// Earth
const loader = new THREE.TextureLoader()
const earthTex = loader.load("/static/textures/earth.jpg") // add your earth.jpg
const earth = new THREE.Mesh(
    new THREE.SphereGeometry(5,64,64),
    new THREE.MeshStandardMaterial({map:earthTex})
)
scene.add(earth)

// Rocket
const rocket = new THREE.Mesh(
    new THREE.ConeGeometry(0.5,2,32),
    new THREE.MeshStandardMaterial({color:0xffffff})
)
scene.add(rocket)

// Orbit
const orbit = new THREE.Mesh(
    new THREE.RingGeometry(9.9,10.1,64),
    new THREE.MeshBasicMaterial({color:0x00ffff,side:THREE.DoubleSide})
)
orbit.rotation.x = Math.PI/2
scene.add(orbit)

// camera
camera.position.set(0,25,0)
camera.lookAt(0,0,0)

let angle=0
function animate(){
    requestAnimationFrame(animate)
    earth.rotation.y +=0.002
    angle+=0.01
    rocket.position.x = 10*Math.cos(angle)
    rocket.position.z = 10*Math.sin(angle)
    rocket.rotation.y+=0.05
    renderer.render(scene,camera)
}
let charts = {
    fuel:createChart("fuel","Fuel (%)"),
    temp:createChart("temp","Temp (°C)"),
    voltage:createChart("voltage","Voltage (V)"),
    battery:createChart("battery","Battery (%)"),
    deviation:createChart("deviation","Deviation"),
    radiation:createChart("radiation","Radiation"),
    oxygen:createChart("oxygen","Oxygen (%)")
}

function createChart(id,label){
    return new Chart(document.getElementById(id),{
        type:"line",
        data:{ labels:[], datasets:[{label:label, data:[], borderColor:"cyan", fill:false, tension:0.2}] },
        options:{
            responsive:true,
            maintainAspectRatio:false,  // important for large canvas
            plugins:{ 
                legend:{ display:true, position:"top", labels:{color:"cyan", font:{size:24}} },
                title:{ display:true, text:label, color:"cyan", font:{size:28} }
            },
            scales:{ 
                x:{ ticks:{ color:"cyan", font:{size:20} } },
                y:{ ticks:{ color:"cyan", font:{size:20} } }
            }
        }
    })
}
animate()