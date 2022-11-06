import { useEffect } from "react";
import * as THREE from "three";
import { OrbitControls } from "three-orbitcontrols-ts";
import "./App.css";

const App = () => {
  useEffect(() => {
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      1,
      1000
    );

    const canvasTexture = new THREE.TextureLoader().load(
      "../public/textures/backgroudTexture.jpg"
    );

    scene.background = canvasTexture;

    const canvas = document.getElementById("threeJSCanvas");
    if (!canvas) return;
    const renderer = new THREE.WebGL1Renderer({
      canvas,
      antialias: true,
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    ambientLight.castShadow = true;
    scene.add(ambientLight);

    const spotLight = new THREE.SpotLight(0xffffff, 1);
    spotLight.castShadow = true;
    spotLight.position.set(128, 128, 64);
    scene.add(spotLight);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);

    camera.position.set(0, 20, 100);
    controls.update();

    // Groups
    const solarSystemGroup = new THREE.Group();
    const earthOrbitGroup = new THREE.Group();
    const moonOrbitGroup = new THREE.Group();

    // Sun
    const sunTexture = new THREE.TextureLoader().load(
      "../public/textures/sunTexture.jpg"
    );
    const sunGeometry = new THREE.SphereGeometry(16);
    const sunMaterial = new THREE.MeshBasicMaterial({ map: sunTexture });
    const sunMesh = new THREE.Mesh(sunGeometry, sunMaterial);
    solarSystemGroup.add(sunMesh);
    scene.add(solarSystemGroup);
    // Earth

    const earthTexture = new THREE.TextureLoader().load(
      "../public/textures/earthTexture.jpg"
    );
    const earthGeometry = new THREE.SphereGeometry(4);
    const earthMaterial = new THREE.MeshBasicMaterial({ map: earthTexture });
    const earthMesh = new THREE.Mesh(earthGeometry, earthMaterial);
    earthMesh.position.x = 50;
    earthOrbitGroup.add(earthMesh);
    scene.add(earthOrbitGroup);

    // Moon

    const moonTexture = new THREE.TextureLoader().load(
      "../public/textures/moonTexture.jpg"
    );
    const moonGeometry = new THREE.SphereGeometry(2);
    const moonMaterial = new THREE.MeshBasicMaterial({ map: moonTexture });
    const moonMesh = new THREE.Mesh(moonGeometry, moonMaterial);
    moonOrbitGroup.add(moonMesh);
    moonOrbitGroup.position.x = 50;
    moonMesh.position.x = 10;
    earthOrbitGroup.add(moonOrbitGroup);

    const animate = () => {
      sunMesh.rotation.x += 0.01;
      earthOrbitGroup.rotation.y += 0.005;
      moonOrbitGroup.rotation.y += 0.05;

      controls.update();

      renderer.render(scene, camera);
      window.requestAnimationFrame(animate);
    };

    animate();
  }, []);
  return (
    <div>
      <canvas id="threeJSCanvas" />
    </div>
  );
};

export default App;
