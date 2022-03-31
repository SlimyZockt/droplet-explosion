<script type="ts">
    import VideoPlayer from "svelte-video-player";
    import PathStore from "../../stores/PathStore";

    $: source = "";

    PathStore.subscribe((path) => {
        source = path;
        console.log(path)
    })

</script>

{#key source}
    <VideoPlayer {source}/>
{/key}