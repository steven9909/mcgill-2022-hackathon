import { useEffect } from "react";
import * as THREE from "three";
import "./App.css";

const App = () => {
  useEffect(() => {
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
      50,
      window.innerWidth / window.innerHeight,
      1,
      1000
    );

    camera.position.z = 96;

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

    const radius = 15;
    const heightSegments = 32;
    const widthSegments = 16;
    const geometrySphere = new THREE.SphereGeometry(
      radius,
      heightSegments,
      widthSegments
    );
    const materialSphere = new THREE.MeshLambertMaterial();
    const sphereMesh = new THREE.Mesh(geometrySphere, materialSphere);
    scene.add(sphereMesh);

    const geometryBox = new THREE.BoxGeometry(20, 20, 20);
    const materialBox = new THREE.MeshNormalMaterial();
    const boxMesh = new THREE.Mesh(geometryBox, materialBox);
    scene.add(boxMesh);

    const animate = () => {
      sphereMesh.rotation.x += 0.01;
      sphereMesh.rotation.y += 0.01;

      boxMesh.rotation.x += 0.01;
      boxMesh.rotation.y += 0.01;

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
