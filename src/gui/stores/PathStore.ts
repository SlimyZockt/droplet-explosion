import type { Writable } from "svelte/store";
import { writable } from "svelte/store";

const PathStore: Writable<string> = writable("");

declare global {
    interface Window {
        electron: any,
        loadPyodide: any;
    }

    interface VideoData {
        data: {
            droplet_count: number[];
            time_in_s: number[];
        };
    }
}

export default PathStore;