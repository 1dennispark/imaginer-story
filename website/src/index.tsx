import './index.css';
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import RootPage from "./app/root";
import * as ReactDOM from "react-dom/client";
import React from 'react';
import CharacterPage from "./app/character";
import SynopsisPage from "./app/synopsis";

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootPage />,
  },
  {
    path: '/character',
    element: <CharacterPage />,
  },
  {
    path: '/synopsis',
    element: <SynopsisPage />,
  },
]);

// @ts-ignore
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);