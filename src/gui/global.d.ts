/// <reference types="svelte" />

export interface VideoData {
    data: {
        droplet_count: number[];
        timestamp: number[];
        time_in_s: [];
    };
}

declare global {
    interface Window {
        pywebview: {
            token: string;
            api: {
                open_file_dialog: () => Promise<string[]>;
                start_analyse: (files: string[] ,debug: boolean) => Promise<VideoData>;
            }
        }
    }
}