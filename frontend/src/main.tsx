import React from 'react'
import ReactDOM from 'react-dom/client'
import {Bounce, ToastContainer} from "react-toastify";
import App from './App.tsx'
import './index.css'
import './reset.css'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import "react-toastify/dist/ReactToastify.css";
import 'maplibre-gl/dist/maplibre-gl.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <>
          <App />
          <ToastContainer
              position="top-right"
              autoClose={3000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
              theme="light"
              transition={Bounce}
          />
        </>
    </React.StrictMode>,
)
