import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import "./App.css";
import { socket } from "./services/websockets";
import { BodyState } from "./types/body";
import { Simulation } from "./types/simulation";

const PLAYER_ID = -1;
const SCALING_FACTOR = 0.0000000002;

const textureMap: { [key: number]: string } = {
  42: "/sunTexture.jpeg",
  43: "/earthTexture.jpeg",
  44: "/marsTexture.jpeg",
  45: "/mercuryTexture.jpeg",
  52: "/venusTexture.jpeg",
  49: "/jupiterTexture.jpeg",
  50: "/saturnTexture.jpeg",
};

const sizeMap: { [key: number]: number } = {
  42: 5,
  43: 1,
  44: 2,
  45: 2,
  49: 4,
  50: 3,
};

const App = () => {
  const [simulation, setSimulation] = useState<Simulation | null>(null);
  const [bodyStates, setBodyStates] = useState<BodyState[]>([]);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [renderer, setRenderer] = useState<THREE.WebGL1Renderer | null>(null);
  const [scene, setScene] = useState<THREE.Scene | null>(null);
  const [camera, setCamera] = useState<THREE.Camera | null>(null);
  const [spheres, setSpheres] = useState<Record<number, THREE.Mesh>>({});

  useEffect(() => {
    if (!canvasRef.current) return;

    const [width, height] = [window.innerWidth, window.innerHeight];

    // setup render, scene, and camera
    const renderer = new THREE.WebGL1Renderer({ canvas: canvasRef.current });
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 1, 1000);

    setRenderer(renderer);
    setScene(scene);
    setCamera(camera);

    // setup light
    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(0, 0, 96);

    // configure renderer
    renderer.setSize(width, height);

    // configure scene
    scene.add(pointLight);

    // configure camera
    camera.position.set(0, 0, 768);

    renderer.render(scene, camera);

    return () => renderer.dispose();
  }, [canvasRef]);

  useEffect(() => {
    const callback = (ev: MessageEvent<string>) => {
      setBodyStates(JSON.parse(ev.data));
    };

    socket.addEventListener("message", callback);

    return () => {
      socket.removeEventListener("message", callback);
    };
  }, []);

  useEffect(() => {
    if (!renderer || !scene || !camera || !canvasRef.current) return;

    console.log(spheres);

    if (Object.keys(spheres).length == 0) {
      for (const bodyState of bodyStates) {
        const geometry = new THREE.SphereGeometry(4, 32, 16);
        const material = new THREE.MeshLambertMaterial();
        const sphere = new THREE.Mesh(geometry, material);
        scene.add(sphere);
        spheres[bodyState.bodyId] = sphere;
      }

      setSpheres(spheres);
    }

    for (const bodyState of bodyStates) {
      spheres[bodyState.bodyId].position.set(
        bodyState.positionX * SCALING_FACTOR,
        bodyState.positionY * SCALING_FACTOR,
        0
      );
    }

    renderer.render(scene, camera);

    return () => renderer.dispose();
  }, [bodyStates]);

  return (
    <div>
      <canvas
        ref={canvasRef}
        style={{ position: "absolute", top: 0, left: 0 }}
      />
    </div>
  );
};

export default App;
