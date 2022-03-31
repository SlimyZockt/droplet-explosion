import type { Writable } from "svelte/store";
import { writable } from "svelte/store";

interface VideoData {
    data: {
        droplet_count: number[],
        timestamp: number[],
    }
}


const VideoDataStore: Writable<VideoData> = writable({ data: { droplet_count: [0], timestamp: [0] } });

export default VideoDataStore;