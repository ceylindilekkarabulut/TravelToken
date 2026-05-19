"use client";

import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || "";

interface Props {
  origin: [number, number];
  destination: [number, number];
}

export function RouteMap({ origin, destination }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: "mapbox://styles/mapbox/dark-v11",
      center: [
        (origin[0] + destination[0]) / 2,
        (origin[1] + destination[1]) / 2,
      ],
      zoom: 3,
    });

    new mapboxgl.Marker({ color: "#7C3AED" }).setLngLat(origin).addTo(map);
    new mapboxgl.Marker({ color: "#A78BFA" }).setLngLat(destination).addTo(map);

    return () => map.remove();
  }, [origin, destination]);

  return <div ref={containerRef} className="w-full h-64 rounded-xl overflow-hidden" />;
}
