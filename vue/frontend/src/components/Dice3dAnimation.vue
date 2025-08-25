<script setup lang="ts">
import {ref, onMounted} from 'vue'
import * as THREE from 'three'
import * as CANNON from 'cannon'
import {DiceManager, DiceD6, DiceD20, DiceD12, DiceD4, DiceD8, DiceD10} from 'threejs-dice'
import type {Dice} from "@/types/dice.ts";
import {useDiceStore} from "@/store/dice.ts";
import {storeToRefs} from "pinia";

const props = defineProps<{
  rolls: Dice[],
  width?: number
  height?: number
}>()

const diceStore = useDiceStore()
const {diceColor} = storeToRefs(diceStore)


const diceContainer = ref<HTMLDivElement>()

let scene: THREE.Scene
let camera: THREE.Camera
let renderer: THREE.WebGLRenderer
let world: any = null
let dice: any[] = []
let diceValues = <any>[]
const containerWidth = ref(800)
const containerHeight = ref(600)


onMounted(async () => {
  if (!diceContainer.value) return

  containerWidth.value = diceContainer.value.clientWidth
  containerHeight.value = diceContainer.value.clientHeight

  try {

    // SCENE
    scene = new THREE.Scene();
    world = new CANNON.World();
    world.gravity.set(0, -9.82 * 32, 0);
    world.broadphase = new CANNON.NaiveBroadphase();
    world.solver.iterations = 16;


    // CAMERA
    const width = containerWidth.value, height = containerHeight.value;
    // const VIEW_ANGLE = 45, ASPECT = width / height, NEAR = 0.01, FAR = 20000;
    // const VIEW_ANGLE = 90, ASPECT = width/height, NEAR = 0.10, FAR = 20;
    // const viewSize = width; // Controls how much of the scene is visible
    // const aspect = width / height;

    camera = new THREE.OrthographicCamera(
        0 - width / 2,
        width / 2,
        height / 2,
        0 - height / 2,
        // -viewSize * aspect,
        // viewSize * aspect,
        // viewSize,
        // -viewSize,
        0.0000001,
        2000
    );

    scene.add(camera);
    // camera.position.set(0,12,0);
    camera.position.set(0, 800, 0);
    camera.lookAt(0, 0, 0);

    // RENDERER
    renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    diceContainer.value.appendChild(renderer.domElement);

    let ambient = new THREE.AmbientLight('#ffffff', 0.5);
    scene.add(ambient);

    let directionalLight = new THREE.DirectionalLight('#ffffff', 0.8);
    directionalLight.position.x = -1000;
    directionalLight.position.y = 1000;
    directionalLight.position.z = 1000;
    scene.add(directionalLight);

    let light = new THREE.SpotLight(0xefdfd5, 30.3);
    light.position.x = 200;
    light.position.z = 200;
    light.position.y = 200;
    light.target.position.set(0, 0, 0);
    light.castShadow = true;
    light.shadow.camera.near = 0.01;
    light.shadow.camera.far = 1100;
    light.shadow.mapSize.width = 1024;
    light.shadow.mapSize.height = 1024;
    scene.add(light);


    // FLOOR
    const floorMaterial = new THREE.MeshPhongMaterial({
      color: '#00aa00',
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0  // invisible
    });
    const floorGeometry = new THREE.PlaneGeometry(width, height, 10, 10);
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.receiveShadow = true;
    floor.rotation.x = Math.PI / 2;
    scene.add(floor);


    const wallMaterial = new THREE.MeshPhongMaterial({color: '#0000aa', side: THREE.DoubleSide});
    const wallGeometry = new THREE.PlaneGeometry(height, 30, 10, 10);
    const wall = new THREE.Mesh(wallGeometry, wallMaterial);
    wall.rotation.y = Math.PI / 2;
    wall.position.x = width / 2;
    scene.add(wall);
    const barrierBody = new CANNON.Body({
      mass: 0,
      shape: new CANNON.Plane(),
      material: DiceManager.barrierBodyMaterial
    });
    barrierBody.quaternion.setFromAxisAngle(new CANNON.Vec3(0, 1, 0), -Math.PI / 2);
    barrierBody.position.set(wall.position.x, wall.position.y, wall.position.z)
    world.add(barrierBody);

    const wallMaterial2 = new THREE.MeshPhongMaterial({color: '#aa00aa', side: THREE.DoubleSide});
    const wallGeometry2 = new THREE.PlaneGeometry(width, 30, 10, 10);
    const wall2 = new THREE.Mesh(wallGeometry2, wallMaterial2);
    wall2.rotation.z = Math.PI;
    wall2.position.z = height / 2;
    scene.add(wall2);
    const barrierBody2 = new CANNON.Body({
      mass: 0,
      shape: new CANNON.Plane(),
      material: DiceManager.barrierBodyMaterial
    });
    // barrierBody2.quaternion.setFromAxisAngle(new CANNON.Vec3(0, 0, 1), -Math.PI / 2);
    barrierBody2.quaternion.setFromAxisAngle(new CANNON.Vec3(0, 1, 0), -Math.PI);
    barrierBody2.position.set(wall2.position.x, wall2.position.y, wall2.position.z)
    world.add(barrierBody2);

    // Third wall (left side, negative X)
    const wallMaterial3 = new THREE.MeshPhongMaterial({color: '#00aa00', side: THREE.DoubleSide});
    const wallGeometry3 = new THREE.PlaneGeometry(height, 30, 10, 10);
    const wall3 = new THREE.Mesh(wallGeometry3, wallMaterial3);
    wall3.rotation.y = -Math.PI / 2;
    wall3.position.x = -width / 2;
    scene.add(wall3);
    const barrierBody3 = new CANNON.Body({
      mass: 0,
      shape: new CANNON.Plane(),
      material: DiceManager.barrierBodyMaterial
    });
    barrierBody3.quaternion.setFromAxisAngle(new CANNON.Vec3(0, 1, 0), Math.PI / 2);
    barrierBody3.position.set(wall3.position.x, wall3.position.y, wall3.position.z)
    world.add(barrierBody3);

    // Fourth wall (back side, negative Z)
    const wallMaterial4 = new THREE.MeshPhongMaterial({color: '#aaaa00', side: THREE.DoubleSide});
    const wallGeometry4 = new THREE.PlaneGeometry(width, 30, 10, 10);
    const wall4 = new THREE.Mesh(wallGeometry4, wallMaterial4);
    wall4.position.z = -height / 2;
    scene.add(wall4);
    const barrierBody4 = new CANNON.Body({
      mass: 0,
      shape: new CANNON.Plane(),
      material: DiceManager.barrierBodyMaterial
    });
    barrierBody4.quaternion.setFromAxisAngle(new CANNON.Vec3(0, 1, 0), 0);
    barrierBody4.position.set(wall4.position.x, wall4.position.y, wall4.position.z)
    world.add(barrierBody4);

    DiceManager.setWorld(world)

    let floorBody = new CANNON.Body({mass: 0, shape: new CANNON.Plane(), material: DiceManager.floorBodyMaterial});
    floorBody.quaternion.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), -Math.PI / 2);
    world.add(floorBody);

    requestAnimationFrame(animate);
    await buildDice()
    setTimeout(() => {
      rollDice()
    }, 500)

  } catch (error) {
    console.error('Error initializing dice animation:', error)
  }
})

function randomDiceThrow() {
  const maxPos = 10;

  for (let i = 0; i < dice.length; i++) {
    const yRand = Math.random() * 20;
    dice[i].resetBody();

    // Keep dice positions within the walled area
    dice[i].getObject().position.x = -maxPos + (i % 3) * (maxPos / 1.5);
    dice[i].getObject().position.y = 2 + Math.floor(i / 3) * 1.5;
    dice[i].getObject().position.z = -maxPos + (i % 3) * (maxPos / 1.5);

    dice[i].getObject().quaternion.x = (Math.random() * 90 - 45) * Math.PI / 180;
    dice[i].getObject().quaternion.z = (Math.random() * 90 - 45) * Math.PI / 180;
    dice[i].updateBodyFromMesh();


    const throwStrength = 24 + Math.random() * 40;
    const throwAngle = Math.random() * Math.PI * 2;
    const throwElevation = 0.3 + Math.random() * 0.4;

    const forwardVelocity = throwStrength * Math.cos(throwElevation);
    const upwardVelocity = throwStrength * Math.sin(throwElevation) + 25;

    dice[i].getObject().body.velocity.set(
        forwardVelocity * Math.cos(throwAngle) + (Math.random() - 0.5) * 3,
        upwardVelocity + yRand,
        forwardVelocity * Math.sin(throwAngle) + (Math.random() - 0.5) * 3
    );

    const spinIntensity = 8 + Math.random() * 12;
    dice[i].getObject().body.angularVelocity.set(
        (Math.random() - 0.5) * spinIntensity,
        (Math.random() - 0.5) * spinIntensity * 0.7,
        (Math.random() - 0.5) * spinIntensity
    );
  }

  DiceManager.prepareValues(diceValues);

}


function animate() {
  updatePhysics();
  render();

  requestAnimationFrame(animate);

}

function updatePhysics() {
  world.step(1.0 / 20.0);

  for (const i in dice) {
    dice[i].updateMeshFromBody();
  }
}


function render() {
  renderer.render(scene, camera);
}


const buildDice = async () => {

  dice = []
  diceValues = []

  if (!props.rolls) return
  const count = props.rolls.length


  for (let i = 0; i < count; i++) {
    let d = props.rolls[i]
    let die: any

    const color = diceColor.value ? diceColor.value : '#fff'

    const dieOpts = {size: 60.0, backColor: color, fontColor: '#000000'}
    if (d.size === 4) {
      die = new DiceD4(dieOpts)
    } else if (d.size === 6) {
      die = new DiceD6(dieOpts)
    } else if (d.size === 8) {
      die = new DiceD8(dieOpts)
    } else if (d.size === 10) {
      die = new DiceD10(dieOpts)
    } else if (d.size === 12) {
      die = new DiceD12(dieOpts)
    } else if (d.size === 20) {
      die = new DiceD20(dieOpts)
    } else {
      die = new DiceD6(dieOpts)
    }

    dice.push(die)
    diceValues.push({dice: die, value: d.value});
  }

  DiceManager.prepareValues(diceValues)

}

const rollDice = async () => {

  try {
    // Clear previous dice
    dice.forEach(die => {
      scene.remove(die.getObject())
    })

    for (let i = 0; i < dice.length; i++) {
      const die = dice[i]
      // die.getObject().castShadow = true
      scene.add(die.getObject())
    }

    randomDiceThrow();

  } catch (error) {
    console.error('Error rolling dice:', error)
  }
}

</script>

<template>
  <div class="dice-roll-animation">

    <div ref="diceContainer" class="dice-container"></div>
  </div>
</template>

<style scoped>
.dice-roll-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.dice-container {
  height: 100%;
  width: 100%;
  margin: auto;
}

</style>
