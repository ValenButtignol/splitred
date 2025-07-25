/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKEND_URL: string;
  // podés agregar más variables si necesitás
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
