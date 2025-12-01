'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three-stdlib';
import * as WebIFC from 'web-ifc';
import IfcPropertyPanel, { IfcProperty } from './IfcPropertyPanel';
import IfcObjectTree, { IfcTreeNode } from './IfcObjectTree';
import { MeasurementManager, Measurement } from './MeasurementTool';
import SectionPlaneControls, { SectionPlane } from './SectionPlaneControls';
import { extractIfcElements, exportToCSV, exportToExcel } from '@/lib/ifcExport';

interface IfcViewerProps {
  ifc_url: string;
}

type ViewMode = '3d' | 'plan' | 'section' | 'elevation';
type CameraType = 'perspective' | 'orthographic';

interface SavedView {
  id: string;
  name: string;
  position: THREE.Vector3;
  target: THREE.Vector3;
  cameraType: CameraType;
}

export default function IfcViewer({ ifc_url }: IfcViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('3d');
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingStage, setLoadingStage] = useState<string>('Initializing');
  const [geometryCount, setGeometryCount] = useState<number>(0);
  const [fileSizeBytes, setFileSizeBytes] = useState<number | null>(null);
  const [loadStartMs, setLoadStartMs] = useState<number>(Date.now());
  const [isOrthographic, setIsOrthographic] = useState(false);
  const [showProperties, setShowProperties] = useState(false);
  const [showObjectTree, setShowObjectTree] = useState(false);
  const [showSectionPlanes, setShowSectionPlanes] = useState(false);
  const [isMeasuring, setIsMeasuring] = useState(false);
  const [selectedProperties, setSelectedProperties] = useState<IfcProperty[]>([]);
  const [selectedObjectName, setSelectedObjectName] = useState<string>('');
  const [objectTree, setObjectTree] = useState<IfcTreeNode | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<number | undefined>();
  const [sectionPlanes, setSectionPlanes] = useState<SectionPlane[]>([]);
  const [savedViews, setSavedViews] = useState<SavedView[]>([]);
  const [selectedFloor, setSelectedFloor] = useState<string | null>(null);
  const [floors, setFloors] = useState<Array<{ id: string; name: string; elevation: number }>>([]);
  const [retryCount, setRetryCount] = useState(0);
  const [maxRetries] = useState(3);
  const [showGrid, setShowGrid] = useState(true);
  const [showAxes, setShowAxes] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  
  // Refs to store three.js objects
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.Camera | null>(null);
  const perspectiveCameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const orthographicCameraRef = useRef<THREE.OrthographicCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const handleResizeRef = useRef<(() => void) | null>(null);
  const modelBoundsRef = useRef<THREE.Box3 | null>(null);
  const modelCenterRef = useRef<THREE.Vector3 | null>(null);
  const ifcApiRef = useRef<WebIFC.IfcAPI | null>(null);
  const modelIDRef = useRef<number | null>(null);
  const ifcMeshesRef = useRef<THREE.Mesh[]>([]);
  const measurementManagerRef = useRef<MeasurementManager | null>(null);
  const raycasterRef = useRef<THREE.Raycaster | null>(null);
  const mouseRef = useRef<THREE.Vector2>(new THREE.Vector2());
  const selectedMeshRef = useRef<THREE.Mesh | null>(null);
  const clippingPlanesRef = useRef<THREE.Plane[]>([]);
  const gridHelperRef = useRef<THREE.GridHelper | null>(null);
  const axesHelperRef = useRef<THREE.AxesHelper | null>(null);

  // Load IFC spatial structure and build object tree
  const buildObjectTree = useCallback(async (ifcApi: WebIFC.IfcAPI, modelID: number): Promise<IfcTreeNode | null> => {
    try {
      // Get spatial structure
      const spatialStructure = (ifcApi as any).GetSpatialStructure(modelID);
      
      const buildNode = (item: any, idCounter: { count: number }): IfcTreeNode | null => {
        if (!item) return null;
        
        const nodeId = idCounter.count++;
        const name = item.name || item.type || 'Unnamed';
        const type = item.type || 'Unknown';
        
        const node: IfcTreeNode = {
          id: nodeId,
          name,
          type,
          expressID: item.expressID,
        };

        if (item.children && item.children.length > 0) {
          node.children = item.children
            .map((child: any) => buildNode(child, idCounter))
            .filter((n: IfcTreeNode | null): n is IfcTreeNode => n !== null);
        }

        return node;
      };

      const idCounter = { count: 0 };
      const root = buildNode(spatialStructure, idCounter);
      return root;
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.warn('Failed to build object tree');
      }
      return null;
    }
  }, []);

  // Get IFC properties for an object
  const getObjectProperties = useCallback(async (
    ifcApi: WebIFC.IfcAPI,
    modelID: number,
    expressID: number
  ): Promise<{ properties: IfcProperty[]; name: string }> => {
    try {
      const properties: IfcProperty[] = [];
      let objectName = 'Unknown';

      // Get the line (object)
      const line = ifcApi.GetLine(modelID, expressID);
      if (line) {
        // Extract basic properties
        if (line.Name) {
          objectName = String(line.Name.value || line.Name);
          properties.push({ name: 'Name', value: objectName, type: 'String' });
        }
        if (line.GlobalId) {
          properties.push({ name: 'GlobalId', value: String(line.GlobalId.value || line.GlobalId), type: 'String' });
        }
        if (line.OwnerHistory) {
          properties.push({ name: 'OwnerHistory', value: String(line.OwnerHistory), type: 'Reference' });
        }

        // Get property sets
        try {
          const propertySets = (ifcApi as any).GetPropertySets(modelID, expressID, true);
          if (propertySets) {
            for (let i = 0; i < propertySets.length; i++) {
              const ps = propertySets[i];
              if (ps && ps.Properties) {
                for (let j = 0; j < ps.Properties.length; j++) {
                  const prop = ps.Properties[j];
                  if (prop && prop.Name && prop.NominalValue) {
                    properties.push({
                      name: prop.Name.value || String(prop.Name),
                      value: prop.NominalValue.value || String(prop.NominalValue),
                      type: prop.NominalValue.type || 'Unknown',
                    });
                  }
                }
              }
            }
          }
        } catch (err) {
          if (process.env.NODE_ENV === 'development') {
            console.warn('Failed to get property sets');
          }
        }

        // Add type information
        if (line.type) {
          properties.push({ name: 'Type', value: String(line.type), type: 'String' });
        }
      }

      return { properties, name: objectName };
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.warn('Failed to get object properties');
      }
      return { properties: [], name: 'Unknown' };
    }
  }, []);

  // Handle object selection via raycasting
  const handleObjectClick = useCallback(async (
    event: MouseEvent,
    ifcApi: WebIFC.IfcAPI | null,
    modelID: number | null
  ) => {
    if (!containerRef.current || !ifcApi || modelID === null || !raycasterRef.current) return;

    if (isMeasuring && measurementManagerRef.current) {
      const handled = measurementManagerRef.current.handleClick(
        event,
        cameraRef.current!,
        ifcMeshesRef.current,
        containerRef.current
      );
      if (handled) return;
    }

    const rect = containerRef.current.getBoundingClientRect();
    mouseRef.current.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouseRef.current.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycasterRef.current.setFromCamera(mouseRef.current, cameraRef.current!);
    const intersects = raycasterRef.current.intersectObjects(ifcMeshesRef.current, true);

    if (intersects.length > 0) {
      const intersect = intersects[0];
      const mesh = intersect.object as THREE.Mesh;

      // Reset previous selection
      if (selectedMeshRef.current) {
        const material = selectedMeshRef.current.material as THREE.MeshStandardMaterial;
        if (material.emissive) {
          material.emissive.setHex(0x000000);
        }
      }

      // Highlight selected mesh
      selectedMeshRef.current = mesh;
      const material = mesh.material as THREE.MeshStandardMaterial;
      if (material.emissive) {
        material.emissive.setHex(0x00ff00);
        material.emissiveIntensity = 0.3;
      }

      // Get expressID from mesh userData or find it
      let expressID: number | null = mesh.userData.expressID || null;
      
      if (!expressID && intersect.faceIndex !== undefined) {
        // Try to find expressID from geometry
        // This is a fallback - in a real implementation, you'd store expressID when creating meshes
        const flatMesh = ifcApi.LoadAllGeometry(modelID);
        if (flatMesh.size() > 0) {
          // Get first available expressID as fallback
          const firstGeometry = flatMesh.get(0);
          expressID = firstGeometry?.expressID || null;
        }
      }

      if (expressID) {
        const { properties, name } = await getObjectProperties(ifcApi, modelID, expressID);
        setSelectedProperties(properties);
        setSelectedObjectName(name);
        setShowProperties(true);
      }
    }
  }, [isMeasuring, getObjectProperties]);

  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    let ifcApi: WebIFC.IfcAPI | null = null;
    let modelID: number | null = null;

    const initViewer = async () => {
      try {
        // Set up Three.js scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf0f0f0);
        sceneRef.current = scene;

        // Set up perspective camera
        const perspectiveCamera = new THREE.PerspectiveCamera(
          75,
          container.clientWidth / container.clientHeight,
          0.1,
          1000
        );
        perspectiveCamera.position.set(10, 10, 10);
        perspectiveCamera.lookAt(0, 0, 0);
        perspectiveCameraRef.current = perspectiveCamera;

        // Set up orthographic camera
        const size = 10;
        const orthographicCamera = new THREE.OrthographicCamera(
          -size * (container.clientWidth / container.clientHeight),
          size * (container.clientWidth / container.clientHeight),
          size,
          -size,
          0.1,
          1000
        );
        orthographicCamera.position.set(10, 10, 10);
        orthographicCamera.lookAt(0, 0, 0);
        orthographicCameraRef.current = orthographicCamera;

        cameraRef.current = perspectiveCamera;

        // Set up renderer
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.localClippingEnabled = true; // Enable clipping planes
        container.appendChild(renderer.domElement);
        rendererRef.current = renderer;

        // Set up lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight1.position.set(10, 10, 10);
        scene.add(directionalLight1);

        const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
        directionalLight2.position.set(-10, -10, -10);
        scene.add(directionalLight2);

        // Set up controls
        const controls = new OrbitControls(perspectiveCamera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controlsRef.current = controls;

        // Set up grid
        const gridHelper = new THREE.GridHelper(50, 50, 0x888888, 0xcccccc);
        scene.add(gridHelper);
        gridHelperRef.current = gridHelper;

        // Set up axes
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
        axesHelperRef.current = axesHelper;

        // Set up raycaster
        const raycaster = new THREE.Raycaster();
        raycasterRef.current = raycaster;

        // Set up measurement manager
        const measurementManager = new MeasurementManager(scene);
        measurementManagerRef.current = measurementManager;

        // Animation loop
        const animate = () => {
          animationFrameRef.current = requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, cameraRef.current!);
        };
        animate();

        // Handle window resize
        const handleResize = () => {
          if (!container || !cameraRef.current || !renderer) return;
          
          const width = container.clientWidth;
          const height = container.clientHeight;

          if (cameraRef.current instanceof THREE.PerspectiveCamera) {
            cameraRef.current.aspect = width / height;
            cameraRef.current.updateProjectionMatrix();
          } else if (cameraRef.current instanceof THREE.OrthographicCamera) {
            const size = 10;
            cameraRef.current.left = -size * (width / height);
            cameraRef.current.right = size * (width / height);
            cameraRef.current.top = size;
            cameraRef.current.bottom = -size;
            cameraRef.current.updateProjectionMatrix();
          }

          renderer.setSize(width, height);
        };
        handleResizeRef.current = handleResize;
        window.addEventListener('resize', handleResize);

        // Mouse move handler for measurement preview
        const handleMouseMove = (e: MouseEvent) => {
          if (isMeasuring && measurementManagerRef.current && containerRef.current) {
            measurementManagerRef.current.handleMouseMove(
              e,
              cameraRef.current!,
              ifcMeshesRef.current,
              containerRef.current
            );
          }
        };
        container.addEventListener('mousemove', handleMouseMove);

        // Click handler
        const handleClick = (e: MouseEvent) => {
          handleObjectClick(e, ifcApi, modelID);
        };
        container.addEventListener('click', handleClick);

        // Initialize web-ifc
        ifcApi = new WebIFC.IfcAPI();
        await ifcApi.Init();
        ifcApiRef.current = ifcApi;

        // Load IFC file with progress tracking
        setLoadStartMs(Date.now());
        setLoadingStage('Fetching IFC file');
        setLoadingProgress(10);
        const response = await fetch(ifc_url);
        if (!response.ok) {
          throw new Error(`Failed to fetch IFC file: ${response.statusText}`);
        }
        const contentLength = response.headers.get('content-length');
        if (contentLength) {
          const bytes = parseInt(contentLength, 10);
          if (!Number.isNaN(bytes)) setFileSizeBytes(bytes);
        }

        setLoadingStage('Parsing IFC data');
        setLoadingProgress(30);
        const arrayBuffer = await response.arrayBuffer();
        const uint8Array = new Uint8Array(arrayBuffer);
        
        setLoadingStage('Opening IFC model');
        setLoadingProgress(50);
        modelID = ifcApi.OpenModel(uint8Array);
        modelIDRef.current = modelID;

        // Get all geometry with progress tracking
        setLoadingStage('Loading geometry');
        setLoadingProgress(60);
        const ifcMeshes = await loadIfcGeometry(ifcApi, modelID, scene);
        ifcMeshesRef.current = ifcMeshes;
        setGeometryCount(ifcMeshes.length);
        setLoadingStage('Building object tree');
        setLoadingProgress(80);

        // Build object tree
        const tree = await buildObjectTree(ifcApi, modelID);
        setObjectTree(tree);

        // Extract floors (IfcStorey)
        // Note: IfcStorey entity type ID varies by IFC schema version
        // Using spatial structure instead which is more reliable
        try {
          const spatialStructure = (ifcApi as any).GetSpatialStructure(modelID);
          const floorList: Array<{ id: string; name: string; elevation: number }> = [];
          
          // Traverse spatial structure to find storeys
          const extractStoreys = (item: any) => {
            if (!item) return;
            
            // Check if this is a storey (type usually includes "Storey" or "Floor")
            const type = item.type?.toLowerCase() || '';
            const name = item.name || 'Unnamed';
            
            if (type.includes('storey') || type.includes('floor') || name.toLowerCase().includes('floor')) {
              const elevation = item.elevation || item.Elevation?.value || 0;
              floorList.push({
                id: String(item.expressID || item.id || floorList.length),
                name: String(name),
                elevation: Number(elevation),
              });
            }
            
            // Recursively check children
            if (item.children && Array.isArray(item.children)) {
              item.children.forEach(extractStoreys);
            }
          };
          
          extractStoreys(spatialStructure);
          
          if (floorList.length > 0) {
            floorList.sort((a, b) => a.elevation - b.elevation);
            setFloors(floorList);
          }
        } catch (err) {
          if (process.env.NODE_ENV === 'development') {
            console.warn('Failed to extract floors from spatial structure');
          }
          // Silently fail - floor extraction is optional
        }

        setLoadingStage('Finalizing view');
        setLoadingProgress(90);

        // Fit camera to model and store bounds
        if (ifcMeshes.length > 0) {
          const { bounds, center } = fitCameraToModel(
            perspectiveCamera,
            controls,
            ifcMeshes
          );
          modelBoundsRef.current = bounds;
          modelCenterRef.current = center;
        } else {
          const defaultBounds = new THREE.Box3().setFromCenterAndSize(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(10, 10, 10)
          );
          modelBoundsRef.current = defaultBounds;
          modelCenterRef.current = new THREE.Vector3(0, 0, 0);
        }

        setLoading(false);
        setLoadingStage('Completed');

        // Cleanup handlers
        return () => {
          container.removeEventListener('mousemove', handleMouseMove);
          container.removeEventListener('click', handleClick);
        };
      } catch (err: any) {
        if (process.env.NODE_ENV === 'development') {
          console.error('IFC viewer error');
        }
        // Never expose internal error details to users
        const errorMessage = 'Failed to load 3D model';
        let detailedMessage = errorMessage;
        
        // Provide specific error messages for common failure scenarios
        if (errorMessage.includes('fetch') || errorMessage.includes('network')) {
          detailedMessage = 'Network error: Unable to fetch IFC file. Please check your connection and try again.';
        } else if (errorMessage.includes('parse') || errorMessage.includes('IFC')) {
          detailedMessage = 'IFC parsing error: The file may be corrupted or in an unsupported format.';
        } else if (errorMessage.includes('memory') || errorMessage.includes('allocation')) {
          detailedMessage = 'Memory error: The model is too large for your device. Try a smaller file.';
        }
        
        setError(detailedMessage);
        setLoading(false);
      }
    };

    initViewer();

    // Keyboard shortcuts
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ignore if typing in input/textarea
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
        return;
      }

      switch (event.key) {
        case '1':
          event.preventDefault();
          setViewMode('3d');
          switchCameraForViewMode('3d');
          if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
            applyViewMode('3d', cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
          }
          break;
        case '2':
          event.preventDefault();
          setViewMode('plan');
          switchCameraForViewMode('plan');
          if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
            applyViewMode('plan', cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
          }
          break;
        case '3':
          event.preventDefault();
          setViewMode('section');
          switchCameraForViewMode('section');
          if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
            applyViewMode('section', cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
          }
          break;
        case '4':
          event.preventDefault();
          setViewMode('elevation');
          switchCameraForViewMode('elevation');
          if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
            applyViewMode('elevation', cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
          }
          break;
        case 'r':
        case 'R':
          event.preventDefault();
          if (cameraRef.current && controlsRef.current && ifcMeshesRef.current.length > 0) {
            switchCameraForViewMode(viewMode);
            const { bounds, center } = fitCameraToModel(cameraRef.current, controlsRef.current, ifcMeshesRef.current);
            modelBoundsRef.current = bounds;
            modelCenterRef.current = center;
            applyViewMode(viewMode, cameraRef.current, controlsRef.current, bounds, center);
          }
          break;
        case 'g':
        case 'G':
          event.preventDefault();
          setShowGrid(prev => !prev);
          break;
        case 'a':
        case 'A':
          event.preventDefault();
          setShowAxes(prev => !prev);
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    // Cleanup
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      // Stop animation loop
      if (animationFrameRef.current !== null) {
        cancelAnimationFrame(animationFrameRef.current);
      }

      // Dispose controls
      if (controlsRef.current) {
        controlsRef.current.dispose();
      }

      // Dispose renderer
      if (rendererRef.current) {
        rendererRef.current.dispose();
        if (container && rendererRef.current.domElement.parentNode === container) {
          container.removeChild(rendererRef.current.domElement);
        }
      }

      // Dispose measurement manager
      if (measurementManagerRef.current) {
        measurementManagerRef.current.dispose();
      }

      // Close IFC model
      if (ifcApiRef.current && modelIDRef.current !== null) {
        ifcApiRef.current.CloseModel(modelIDRef.current);
      }

      // Clean up scene
      if (sceneRef.current) {
        sceneRef.current.traverse((object) => {
          if (object instanceof THREE.Mesh) {
            object.geometry.dispose();
            if (Array.isArray(object.material)) {
              object.material.forEach((material) => material.dispose());
            } else {
              object.material.dispose();
            }
          }
        });
      }

      // Remove resize listener
      if (handleResizeRef.current) {
        window.removeEventListener('resize', handleResizeRef.current);
        handleResizeRef.current = null;
      }
    };
  }, [ifc_url, buildObjectTree, handleObjectClick, isMeasuring]);

  // Toggle orthographic camera
  const toggleOrthographic = useCallback(() => {
    if (!perspectiveCameraRef.current || !orthographicCameraRef.current || !controlsRef.current) return;

    const wasOrthographic = isOrthographic;
    setIsOrthographic(!wasOrthographic);

    if (wasOrthographic) {
      // Switch to perspective
      const ortho = orthographicCameraRef.current;
      const persp = perspectiveCameraRef.current;

      persp.position.copy(ortho.position);
      persp.rotation.copy(ortho.rotation);
      persp.updateProjectionMatrix();

      cameraRef.current = persp;
      controlsRef.current.object = persp;
    } else {
      // Switch to orthographic
      const persp = perspectiveCameraRef.current;
      const ortho = orthographicCameraRef.current;

      ortho.position.copy(persp.position);
      ortho.rotation.copy(persp.rotation);

      const container = containerRef.current;
      if (container) {
        const size = 10;
        ortho.left = -size * (container.clientWidth / container.clientHeight);
        ortho.right = size * (container.clientWidth / container.clientHeight);
        ortho.top = size;
        ortho.bottom = -size;
      }
      ortho.updateProjectionMatrix();

      cameraRef.current = ortho;
      controlsRef.current.object = ortho;
    }
  }, [isOrthographic]);

  // Handle section plane changes
  const handleSectionPlaneChange = useCallback((plane: SectionPlane) => {
    if (!sceneRef.current) return;

    setSectionPlanes((prevPlanes) => {
      const planeIndex = prevPlanes.findIndex((p) => p.id === plane.id);
      const updatedPlanes = planeIndex >= 0
        ? prevPlanes.map((p) => (p.id === plane.id ? plane : p))
        : [...prevPlanes, plane];

      // Update clipping planes
      const enabledPlanes = updatedPlanes.filter((p) => p.enabled);
      clippingPlanesRef.current = enabledPlanes.map((p) => {
        const normal = new THREE.Vector3();
        if (p.axis === 'x') normal.set(1, 0, 0);
        else if (p.axis === 'y') normal.set(0, 1, 0);
        else normal.set(0, 0, 1);
        return new THREE.Plane(normal, p.position);
      });

      // Apply to all meshes
      ifcMeshesRef.current.forEach((mesh) => {
        const material = mesh.material as THREE.MeshStandardMaterial;
        material.clippingPlanes = clippingPlanesRef.current;
      });

      return updatedPlanes;
    });
  }, []);

  const handleSectionPlaneAdd = useCallback((axis: 'x' | 'y' | 'z') => {
    const newPlane: SectionPlane = {
      id: `plane-${Date.now()}`,
      axis,
      position: 0,
      enabled: true,
    };
    handleSectionPlaneChange(newPlane);
  }, [handleSectionPlaneChange]);

  const handleSectionPlaneRemove = useCallback((id: string) => {
    setSectionPlanes((prevPlanes) => {
      const filtered = prevPlanes.filter((p) => p.id !== id);
      
      // Update clipping planes
      const enabledPlanes = filtered.filter((p) => p.enabled);
      clippingPlanesRef.current = enabledPlanes.map((p) => {
        const normal = new THREE.Vector3();
        if (p.axis === 'x') normal.set(1, 0, 0);
        else if (p.axis === 'y') normal.set(0, 1, 0);
        else normal.set(0, 0, 1);
        return new THREE.Plane(normal, p.position);
      });

      // Apply to all meshes
      ifcMeshesRef.current.forEach((mesh) => {
        const material = mesh.material as THREE.MeshStandardMaterial;
        material.clippingPlanes = clippingPlanesRef.current;
      });

      return filtered;
    });
  }, []);

  // Toggle grid visibility
  useEffect(() => {
    if (gridHelperRef.current) {
      gridHelperRef.current.visible = showGrid;
    }
  }, [showGrid]);

  // Toggle axes visibility
  useEffect(() => {
    if (axesHelperRef.current) {
      axesHelperRef.current.visible = showAxes;
    }
  }, [showAxes]);

  // Fullscreen support
  const toggleFullscreen = useCallback(() => {
    if (!containerRef.current) return;

    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => {
        setIsFullscreen(true);
        // Update renderer size after fullscreen
        if (rendererRef.current && cameraRef.current) {
          const width = containerRef.current!.clientWidth;
          const height = containerRef.current!.clientHeight;
          rendererRef.current.setSize(width, height);
          if (cameraRef.current instanceof THREE.PerspectiveCamera) {
            cameraRef.current.aspect = width / height;
            cameraRef.current.updateProjectionMatrix();
          } else if (cameraRef.current instanceof THREE.OrthographicCamera) {
            const size = 10;
            cameraRef.current.left = -size * (width / height);
            cameraRef.current.right = size * (width / height);
            cameraRef.current.top = size;
            cameraRef.current.bottom = -size;
            cameraRef.current.updateProjectionMatrix();
          }
        }
      }).catch((err) => {
        if (process.env.NODE_ENV === 'development') {
          console.error('Error attempting to enable fullscreen');
        }
      });
    } else {
      document.exitFullscreen().then(() => {
        setIsFullscreen(false);
        // Update renderer size after exiting fullscreen
        if (rendererRef.current && cameraRef.current && containerRef.current) {
          const width = containerRef.current.clientWidth;
          const height = containerRef.current.clientHeight;
          rendererRef.current.setSize(width, height);
          if (cameraRef.current instanceof THREE.PerspectiveCamera) {
            cameraRef.current.aspect = width / height;
            cameraRef.current.updateProjectionMatrix();
          } else if (cameraRef.current instanceof THREE.OrthographicCamera) {
            const size = 10;
            cameraRef.current.left = -size * (width / height);
            cameraRef.current.right = size * (width / height);
            cameraRef.current.top = size;
            cameraRef.current.bottom = -size;
            cameraRef.current.updateProjectionMatrix();
          }
        }
      }).catch((err) => {
        if (process.env.NODE_ENV === 'development') {
          console.error('Error attempting to exit fullscreen');
        }
      });
    }
  }, []);

  // Listen for fullscreen changes
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  // Switch camera based on view mode
  const switchCameraForViewMode = useCallback((mode: ViewMode) => {
    if (!perspectiveCameraRef.current || !orthographicCameraRef.current || !controlsRef.current || !rendererRef.current || !containerRef.current || !cameraRef.current) {
      return;
    }

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Use orthographic for 2D views, perspective for 3D
    if (mode === 'plan' || mode === 'section' || mode === 'elevation') {
      // Switch to orthographic camera
      if (cameraRef.current !== orthographicCameraRef.current) {
        // Copy position and target from current camera
        const currentPos = cameraRef.current.position.clone();
        const currentTarget = controlsRef.current.target.clone();
        
        // Update orthographic camera size based on model bounds
        if (modelBoundsRef.current) {
          const size = modelBoundsRef.current.getSize(new THREE.Vector3());
          const maxDim = Math.max(size.x, size.y, size.z);
          const orthoSize = maxDim * 1.2;
          
          orthographicCameraRef.current.left = -orthoSize * (width / height);
          orthographicCameraRef.current.right = orthoSize * (width / height);
          orthographicCameraRef.current.top = orthoSize;
          orthographicCameraRef.current.bottom = -orthoSize;
        }
        
        orthographicCameraRef.current.position.copy(currentPos);
        orthographicCameraRef.current.updateProjectionMatrix();
        
        // Update controls to use orthographic camera
        controlsRef.current.object = orthographicCameraRef.current;
        controlsRef.current.target.copy(currentTarget);
        controlsRef.current.update();
        
        cameraRef.current = orthographicCameraRef.current;
        setIsOrthographic(true);
      }
    } else {
      // Switch to perspective camera for 3D view
      if (cameraRef.current !== perspectiveCameraRef.current) {
        // Copy position and target from current camera
        const currentPos = cameraRef.current.position.clone();
        const currentTarget = controlsRef.current.target.clone();
        
        perspectiveCameraRef.current.aspect = width / height;
        perspectiveCameraRef.current.position.copy(currentPos);
        perspectiveCameraRef.current.updateProjectionMatrix();
        
        // Update controls to use perspective camera
        controlsRef.current.object = perspectiveCameraRef.current;
        controlsRef.current.target.copy(currentTarget);
        controlsRef.current.update();
        
        cameraRef.current = perspectiveCameraRef.current;
        setIsOrthographic(false);
      }
    }
  }, []);

  // Save current view
  const saveCurrentView = useCallback(() => {
    if (!cameraRef.current || !controlsRef.current) return;

    const viewName = prompt('Enter view name:');
    if (!viewName) return;

    const savedView: SavedView = {
      id: `view-${Date.now()}`,
      name: viewName,
      position: cameraRef.current.position.clone(),
      target: controlsRef.current.target.clone(),
      cameraType: isOrthographic ? 'orthographic' : 'perspective',
    };

    setSavedViews([...savedViews, savedView]);
  }, [savedViews, isOrthographic]);

  // Restore saved view
  const restoreView = useCallback((view: SavedView) => {
    if (!cameraRef.current || !controlsRef.current) return;

    if (view.cameraType === 'orthographic' && !isOrthographic) {
      toggleOrthographic();
    } else if (view.cameraType === 'perspective' && isOrthographic) {
      toggleOrthographic();
    }

    setTimeout(() => {
      if (cameraRef.current && controlsRef.current) {
        cameraRef.current.position.copy(view.position);
        controlsRef.current.target.copy(view.target);
        controlsRef.current.update();
        if (cameraRef.current instanceof THREE.PerspectiveCamera || cameraRef.current instanceof THREE.OrthographicCamera) {
          cameraRef.current.updateProjectionMatrix();
        }
      }
    }, 100);
  }, [isOrthographic, toggleOrthographic]);

  // Handle floor selection
  const handleFloorSelect = useCallback((floorId: string | null) => {
    setSelectedFloor(floorId);
    if (!floorId || !modelCenterRef.current || !cameraRef.current || !controlsRef.current) return;

    const floor = floors.find((f) => f.id === floorId);
    if (!floor) return;

    const center = modelCenterRef.current.clone();
    center.y = floor.elevation;

    const size = modelBoundsRef.current?.getSize(new THREE.Vector3());
    if (size) {
      const distance = Math.max(size.x, size.z) * 1.5;
      cameraRef.current.position.set(center.x, center.y + distance, center.z);
      cameraRef.current.lookAt(center);
      controlsRef.current.target.copy(center);
      controlsRef.current.update();
      if (cameraRef.current instanceof THREE.PerspectiveCamera || cameraRef.current instanceof THREE.OrthographicCamera) {
        cameraRef.current.updateProjectionMatrix();
      }
    }
  }, [floors]);

  // Focus on selected object by expressID
  const focusOnObject = useCallback((expressID: number | undefined) => {
    if (!expressID || !cameraRef.current || !controlsRef.current || !ifcMeshesRef.current.length) {
      return;
    }

    // Find all meshes with matching expressID
    const matchingMeshes = ifcMeshesRef.current.filter(
      (mesh) => mesh.userData.expressID === expressID
    );

    if (matchingMeshes.length === 0) {
      return;
    }

    // Calculate bounding box of selected object(s)
    const box = new THREE.Box3();
    matchingMeshes.forEach((mesh) => {
      const meshBox = new THREE.Box3().setFromObject(mesh);
      box.union(meshBox);
    });

    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);

    // Calculate target camera position and distance
    let targetPosition: THREE.Vector3;
    let cameraDistance: number;

    if (cameraRef.current instanceof THREE.PerspectiveCamera) {
      const fov = cameraRef.current.fov * (Math.PI / 180);
      cameraDistance = maxDim / 2 / Math.tan(fov / 2);
      cameraDistance *= 1.5; // Add some padding
      const direction = new THREE.Vector3(1, 1, 1).normalize();
      targetPosition = center.clone().add(direction.multiplyScalar(cameraDistance));
    } else if (cameraRef.current instanceof THREE.OrthographicCamera) {
      cameraDistance = maxDim * 1.5;
      const direction = new THREE.Vector3(1, 1, 1).normalize();
      targetPosition = center.clone().add(direction.multiplyScalar(cameraDistance));
    } else {
      return;
    }

    // Store initial values for animation
    const startPosition = cameraRef.current.position.clone();
    const startTarget = controlsRef.current.target.clone();
    const endPosition = targetPosition;
    const endTarget = center;

    // Animation duration in milliseconds
    const duration = 1000;
    const startTime = Date.now();

    // Easing function (ease-in-out)
    const easeInOutCubic = (t: number): number => {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    };

    // Animation loop
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeInOutCubic(progress);

      // Interpolate position and target
      cameraRef.current!.position.lerpVectors(startPosition, endPosition, easedProgress);
      controlsRef.current!.target.lerpVectors(startTarget, endTarget, easedProgress);
      controlsRef.current!.update();

      if (cameraRef.current instanceof THREE.PerspectiveCamera || cameraRef.current instanceof THREE.OrthographicCamera) {
        cameraRef.current.updateProjectionMatrix();
      }

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  }, []);

  return (
    <div className="relative w-full h-full min-h-[600px]">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 z-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading 3D model...</p>
            {loadingProgress > 0 && (
              <div className="mt-4 w-64 mx-auto">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-600 transition-all duration-300"
                    style={{ width: `${loadingProgress}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">{loadingProgress}%</div>
              </div>
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 z-50">
          <div className="text-center p-8 max-w-md">
            <div className="text-6xl mb-4">⚠️</div>
            <p className="text-red-600 font-semibold mb-2">Failed to load model</p>
            <p className="text-gray-600 text-sm mb-4">{error}</p>
            {retryCount < maxRetries ? (
              <div className="space-y-3">
                <button
                  onClick={async () => {
                    setError(null);
                    setLoading(true);
                    setRetryCount(prev => prev + 1);
                    
                    // Exponential backoff: wait 2^retryCount seconds
                    const delay = Math.pow(2, retryCount) * 1000;
                    await new Promise(resolve => setTimeout(resolve, delay));
                    
                    // Reload the viewer
                    window.location.reload();
                  }}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
                >
                  Retry {retryCount > 0 && `(Attempt ${retryCount + 1}/${maxRetries})`}
                </button>
                <p className="text-xs text-gray-500">
                  Troubleshooting: Check your internet connection, verify the file URL is accessible, or try downloading the file manually.
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-sm text-gray-600">Maximum retry attempts reached.</p>
                <div className="flex gap-2 justify-center">
                  <button
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium"
                  >
                    Reload Page
                  </button>
                  <a
                    href={ifc_url}
                    download
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium inline-block"
                  >
                    Download File
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <div ref={containerRef} className="w-full h-full" />
      
      {loading && !error && (
        <div className="absolute inset-0 z-40 flex items-center justify-center bg-white/70 backdrop-blur-sm">
          <div className="w-full max-w-md p-6 bg-white rounded-xl shadow-lg border border-gray-200">
            <div className="mb-4">
              <div className="h-3 w-full rounded bg-gray-200 overflow-hidden">
                <div
                  className="h-3 rounded bg-primary-600 transition-all"
                  style={{ width: `${Math.min(loadingProgress, 100)}%` }}
                />
              </div>
              <div className="mt-2 flex justify-between text-xs text-gray-600">
                <span>{loadingStage}</span>
                <span>{loadingProgress}%</span>
              </div>
            </div>
            <div className="space-y-1 text-xs text-gray-600">
              {fileSizeBytes !== null && (
                <div>File size: {(fileSizeBytes / (1024 * 1024)).toFixed(2)} MB</div>
              )}
              {geometryCount > 0 && <div>Geometries loaded: {geometryCount}</div>}
              <div>
                ETA:{' '}
                {(() => {
                  const elapsed = Date.now() - loadStartMs;
                  const p = Math.max(loadingProgress, 1) / 100;
                  const total = elapsed / p;
                  const remaining = Math.max(total - elapsed, 0);
                  const sec = Math.ceil(remaining / 1000);
                  return isFinite(sec) ? `${sec}s` : '…';
                })()}
              </div>
            </div>
            <div className="mt-4">
              <div className="animate-pulse flex space-x-4">
                <div className="rounded bg-gray-200 h-20 w-20" />
                <div className="flex-1 space-y-3 py-1">
                  <div className="h-4 bg-gray-200 rounded w-5/6" />
                  <div className="h-4 bg-gray-200 rounded w-3/4" />
                  <div className="h-4 bg-gray-200 rounded w-2/3" />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Toolbar */}
      {!loading && !error && (
        <div className="absolute top-4 right-4 flex flex-col gap-2 z-40">
          {/* View Mode Buttons */}
          <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-2 flex gap-2 flex-wrap">
            <button
              onClick={() => {
                const newMode: ViewMode = '3d';
                setViewMode(newMode);
                switchCameraForViewMode(newMode);
                if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
                  applyViewMode(newMode, cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
                }
              }}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                viewMode === '3d'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="3D View"
            >
              3D
            </button>
            <button
              onClick={() => {
                const newMode: ViewMode = 'plan';
                setViewMode(newMode);
                switchCameraForViewMode(newMode);
                if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
                  applyViewMode(newMode, cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
                }
              }}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                viewMode === 'plan'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Plan View"
            >
              Plan
            </button>
            <button
              onClick={() => {
                const newMode: ViewMode = 'section';
                setViewMode(newMode);
                switchCameraForViewMode(newMode);
                if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
                  applyViewMode(newMode, cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
                }
              }}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                viewMode === 'section'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Section View"
            >
              Section
            </button>
            <button
              onClick={() => {
                const newMode: ViewMode = 'elevation';
                setViewMode(newMode);
                switchCameraForViewMode(newMode);
                if (cameraRef.current && controlsRef.current && modelBoundsRef.current && modelCenterRef.current) {
                  applyViewMode(newMode, cameraRef.current, controlsRef.current, modelBoundsRef.current, modelCenterRef.current);
                }
              }}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                viewMode === 'elevation'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Elevation View"
            >
              Elevation
            </button>
          </div>
          
          {/* Tool Buttons */}
          <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-2 flex flex-col gap-2">
            <button
              onClick={() => setShowGrid(!showGrid)}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showGrid
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Toggle Grid (G)"
            >
              Grid
            </button>
            <button
              onClick={() => setShowAxes(!showAxes)}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showAxes
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Toggle Axes (A)"
            >
              Axes
            </button>
            <button
              onClick={() => setShowProperties(!showProperties)}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showProperties
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Show Properties Panel"
            >
              Properties
            </button>
            <button
              onClick={() => setShowObjectTree(!showObjectTree)}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showObjectTree
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Show Object Tree"
            >
              Object Tree
            </button>
            <button
              onClick={() => {
                const newMeasuring = !isMeasuring;
                setIsMeasuring(newMeasuring);
                if (measurementManagerRef.current) {
                  if (newMeasuring) {
                    measurementManagerRef.current.startMeasurement();
                  } else {
                    measurementManagerRef.current.stopMeasurement();
                  }
                }
              }}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                isMeasuring
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Measurement Tool"
            >
              Measure
            </button>
            <button
              onClick={() => setShowSectionPlanes(!showSectionPlanes)}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showSectionPlanes
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Section Planes"
            >
              Sections
            </button>
            <button
              onClick={toggleOrthographic}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                isOrthographic
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Toggle Orthographic View"
            >
              Ortho
            </button>
            <button
              onClick={saveCurrentView}
              className="px-3 py-1.5 rounded text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
              title="Save Current View"
            >
              Save View
            </button>
            <button
              onClick={toggleFullscreen}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                isFullscreen
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title="Toggle Fullscreen"
            >
              {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
            </button>
            <button
              onClick={async () => {
                if (ifcApiRef.current && modelIDRef.current !== null) {
                  try {
                    const elements = await extractIfcElements(ifcApiRef.current, modelIDRef.current);
                    if (elements.length > 0) {
                      exportToExcel(elements, 'ifc_model_export.xlsx');
                    } else {
                      alert('No elements found to export');
                    }
                  } catch (error) {
                    if (process.env.NODE_ENV === 'development') {
                      console.error('Export failed');
                    }
                    alert('Failed to export data. Please try again.');
                  }
                }
              }}
              className="px-3 py-1.5 rounded text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
              title="Export to Excel/CSV"
            >
              Export
            </button>
          <button
            onClick={() => {
              if (cameraRef.current && controlsRef.current && ifcMeshesRef.current.length > 0) {
                // Ensure correct camera for current view mode
                switchCameraForViewMode(viewMode);
                // Recalculate bounds from stored meshes
                const { bounds, center } = fitCameraToModel(
                  cameraRef.current!,
                  controlsRef.current,
                  ifcMeshesRef.current
                );
                modelBoundsRef.current = bounds;
                modelCenterRef.current = center;
                applyViewMode(viewMode, cameraRef.current!, controlsRef.current, bounds, center);
              } else if (modelBoundsRef.current && modelCenterRef.current) {
                // Ensure correct camera for current view mode
                switchCameraForViewMode(viewMode);
                // Fallback to stored bounds if meshes not available
                applyViewMode(viewMode, cameraRef.current!, controlsRef.current!, modelBoundsRef.current, modelCenterRef.current);
              }
            }}
              className="px-3 py-1.5 rounded text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
              title="Reset View"
          >
              Reset
          </button>
        </div>

          {/* Saved Views */}
          {savedViews.length > 0 && (
            <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-2">
              <div className="text-xs font-semibold text-gray-600 mb-2">Saved Views</div>
              <div className="flex flex-col gap-1">
                {savedViews.map((view) => (
                  <button
                    key={view.id}
                    onClick={() => restoreView(view)}
                    className="px-2 py-1 text-xs text-left bg-gray-100 text-gray-700 hover:bg-gray-200 rounded transition-colors"
                  >
                    {view.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Floor Selector */}
          {floors.length > 0 && (
            <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-2">
              <div className="text-xs font-semibold text-gray-600 mb-2">Floors</div>
              <select
                value={selectedFloor || ''}
                onChange={(e) => handleFloorSelect(e.target.value || null)}
                className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">All Floors</option>
                {floors.map((floor) => (
                  <option key={floor.id} value={floor.id}>
                    {floor.name} ({floor.elevation.toFixed(2)}m)
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}

      {/* Property Panel */}
      {showProperties && (
        <IfcPropertyPanel
          properties={selectedProperties}
          selectedObjectName={selectedObjectName}
          onClose={() => setShowProperties(false)}
        />
      )}

      {/* Object Tree */}
      {showObjectTree && (
        <IfcObjectTree
          tree={objectTree}
          onSelectNode={(node) => {
            setSelectedNodeId(node.id);
            if (node.expressID) {
              focusOnObject(node.expressID);
            }
          }}
          selectedNodeId={selectedNodeId}
          onClose={() => setShowObjectTree(false)}
        />
      )}

      {/* Section Plane Controls */}
      {showSectionPlanes && (
        <SectionPlaneControls
          planes={sectionPlanes}
          onPlaneChange={handleSectionPlaneChange}
          onPlaneRemove={handleSectionPlaneRemove}
          onPlaneAdd={handleSectionPlaneAdd}
          onClose={() => setShowSectionPlanes(false)}
        />
      )}

      {/* Controls hint */}
      {!loading && !error && (
        <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 text-xs text-gray-600 shadow-lg z-40 max-w-xs">
          <div className="font-semibold mb-1">Controls:</div>
          <div>Left click + drag: Rotate</div>
          <div>Right click + drag: Pan</div>
          <div>Scroll: Zoom</div>
          <div className="mt-2 font-semibold">Keyboard Shortcuts:</div>
          <div>1-4: View modes (3D, Plan, Section, Elevation)</div>
          <div>R: Reset view</div>
          <div>G: Toggle grid</div>
          <div>A: Toggle axes</div>
          {isMeasuring && <div className="mt-2 text-primary-600 font-semibold">Click two points to measure</div>}
        </div>
      )}
    </div>
  );
}

/**
 * Load IFC geometry and convert to Three.js meshes
 */
async function loadIfcGeometry(
  ifcApi: WebIFC.IfcAPI,
  modelID: number,
  scene: THREE.Scene
): Promise<THREE.Mesh[]> {
  const meshes: THREE.Mesh[] = [];

  try {
    const flatMesh = ifcApi.LoadAllGeometry(modelID);
    
    for (let i = 0; i < flatMesh.size(); i++) {
      const placedGeometry = flatMesh.get(i);
      
      try {
        const geometry = ifcApi.GetGeometry(modelID, placedGeometry.expressID);
        if (!geometry) continue;

        const verts = ifcApi.GetVertexArray(
          geometry.GetVertexData(),
          geometry.GetVertexDataSize()
        );
        const indices = ifcApi.GetIndexArray(
          geometry.GetIndexData(),
          geometry.GetIndexDataSize()
        );

        const bufferGeometry = new THREE.BufferGeometry();
        const positionAttribute = new THREE.Float32BufferAttribute(verts, 3);
        bufferGeometry.setAttribute('position', positionAttribute);
        bufferGeometry.setIndex(Array.from(indices));
        bufferGeometry.computeVertexNormals();

        const color = new THREE.Color().setHSL(Math.random(), 0.5, 0.6);
        const material = new THREE.MeshStandardMaterial({
          color: color,
          side: THREE.DoubleSide,
          flatShading: false,
        });

        const mesh = new THREE.Mesh(bufferGeometry, material);
        mesh.userData.expressID = placedGeometry.expressID; // Store expressID for property lookup
        
        // Performance optimization: Enable frustum culling
        mesh.frustumCulled = true;
        
        scene.add(mesh);
        meshes.push(mesh);
      } catch (err) {
        if (process.env.NODE_ENV === 'development') {
          console.warn('Failed to process geometry');
        }
      }
    }
  } catch (err) {
    if (process.env.NODE_ENV === 'development') {
      console.error('Failed to load geometry');
    }
  }

  // Note: LOD (Level of Detail) can be added in the future for very large models
  // by creating simplified versions of meshes and switching based on camera distance

  return meshes;
}

/**
 * Fit camera to model bounds
 */
function fitCameraToModel(
  camera: THREE.Camera,
  controls: OrbitControls,
  meshes: THREE.Mesh[]
): { bounds: THREE.Box3; center: THREE.Vector3 } {
  const box = new THREE.Box3();
  
  if (meshes.length > 0) {
    meshes.forEach((mesh) => {
      const meshBox = new THREE.Box3().setFromObject(mesh);
      box.union(meshBox);
    });
  } else {
    box.setFromCenterAndSize(new THREE.Vector3(0, 0, 0), new THREE.Vector3(10, 10, 10));
  }

  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z);
  
  if (camera instanceof THREE.PerspectiveCamera) {
  const fov = camera.fov * (Math.PI / 180);
  let cameraDistance = maxDim / 2 / Math.tan(fov / 2);
    cameraDistance *= 1.5;

  const direction = new THREE.Vector3(1, 1, 1).normalize();
  camera.position.copy(center).add(direction.multiplyScalar(cameraDistance));
  camera.lookAt(center);
  } else if (camera instanceof THREE.OrthographicCamera) {
    const cameraDistance = maxDim * 1.5;
    const direction = new THREE.Vector3(1, 1, 1).normalize();
    camera.position.copy(center).add(direction.multiplyScalar(cameraDistance));
    camera.lookAt(center);
  }

  if (camera instanceof THREE.PerspectiveCamera || camera instanceof THREE.OrthographicCamera) {
  camera.updateProjectionMatrix();
  }
  controls.target.copy(center);
  controls.update();

  return { bounds: box, center };
}

/**
 * Apply view mode (Plan, Section, Elevation, 3D)
 */
function applyViewMode(
  mode: ViewMode,
  camera: THREE.Camera,
  controls: OrbitControls,
  bounds: THREE.Box3,
  center: THREE.Vector3
): void {
  const size = bounds.getSize(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z);

  let cameraDistance: number;
  if (camera instanceof THREE.PerspectiveCamera) {
  const fov = camera.fov * (Math.PI / 180);
    cameraDistance = (maxDim / 2 / Math.tan(fov / 2)) * 1.5;
  } else {
    cameraDistance = maxDim * 1.5;
  }

  switch (mode) {
    case 'plan':
      // True top-down orthographic view (looking down Y-axis)
      camera.position.set(center.x, center.y + cameraDistance, center.z);
      camera.lookAt(center);
      controls.enableRotate = false; // Disable rotation for true orthographic plan view
      break;

    case 'section':
      // Side view (Y-Z plane) - looking along X-axis
      camera.position.set(center.x + cameraDistance, center.y, center.z);
      camera.lookAt(center);
      controls.enableRotate = false; // Disable rotation for true orthographic section view
      break;

    case 'elevation':
      // Front view (X-Z plane) - looking along Y-axis
      camera.position.set(center.x, center.y, center.z + cameraDistance);
      camera.lookAt(center);
      controls.enableRotate = false; // Disable rotation for true orthographic elevation view
      break;

    case '3d':
    default:
      // Isometric perspective view
      const direction = new THREE.Vector3(1, 1, 1).normalize();
      camera.position.copy(center).add(direction.multiplyScalar(cameraDistance));
      camera.lookAt(center);
      controls.enableRotate = true; // Enable rotation for 3D view
      break;
  }

  if (camera instanceof THREE.PerspectiveCamera || camera instanceof THREE.OrthographicCamera) {
  camera.updateProjectionMatrix();
  }
  controls.target.copy(center);
  controls.update();
}
