interface ImportMetaEnv {
    readonly VITE_API_HOST: string;
    readonly VITE_MODE: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}