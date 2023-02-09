import React from 'react';
import './index.css';
import Notification from './components/notification/notification';
import Login from './components/auth/login';
import User from './components/user/profile';
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import "./index.css";


const root = ReactDOM.createRoot(document.getElementById('root'));

const router = createBrowserRouter([
  {
    path: "notification/:id",
    element:<Notification />,
  },
  {
    path: "login/",
    element:<Login />,
  },
  {
    path: "profile/:username",
    element:<User />,
  },
]);


root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
